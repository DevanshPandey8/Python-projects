#!/usr/bin/env python3
"""
Aiden - Your AI Assistant with proper input handling
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import queue
import sys
import os
from datetime import datetime
import webbrowser

# Import the Aiden AI assistant functions
from ai_assistant import process_user_input, add_to_history, conversation_history

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Aiden - Your AI Assistant")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3a3a3a',
            'accent': '#00d4ff',
            'accent_hover': '#00b8e6',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'user_color': '#4fc3f7',
            'bot_color': '#81c784',
            'system_color': '#ffb74d',
            'error_color': '#f44336',
            'success_color': '#4caf50'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # Animation variables
        self.typing_animation = False
        self.typing_dots = 0
        
        # Create the UI
        self.create_ui()
        
        # Initialize chat
        self.initialize_chat()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start checking for queued messages
        self.check_queue()
        
        # Ensure input is ready
        self.root.after(100, self.ensure_input_ready)
    
    def create_ui(self):
        """Create the main UI"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Chat area
        self.create_chat_area()
        
        # Input area
        self.create_input_area()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        self.title_label = tk.Label(header_frame,
                                   text="🤖 Aiden - Your AI Assistant",
                                   font=('Segoe UI', 24, 'bold'),
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['accent'])
        self.title_label.pack(side=tk.LEFT)
        
        # Status
        self.status_label = tk.Label(header_frame,
                                    text="Ready",
                                    font=('Segoe UI', 12),
                                    bg=self.colors['bg_primary'],
                                    fg=self.colors['success_color'])
        self.status_label.pack(side=tk.RIGHT, padx=20)
    
    def create_chat_area(self):
        """Create the chat display area"""
        chat_container = tk.Frame(self.main_container, 
                                 bg=self.colors['bg_secondary'],
                                 relief='flat', bd=2)
        chat_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            state=tk.DISABLED,
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=20
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags
        self.chat_display.tag_configure('user', 
                                       foreground=self.colors['user_color'],
                                       font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('bot',
                                       foreground=self.colors['bot_color'],
                                       font=('Segoe UI', 11))
        self.chat_display.tag_configure('system',
                                       foreground=self.colors['system_color'],
                                       font=('Segoe UI', 11, 'italic'))
        self.chat_display.tag_configure('error',
                                       foreground=self.colors['error_color'],
                                       font=('Segoe UI', 11, 'bold'))
    
    def create_input_area(self):
        """Create the input area with proper focus handling"""
        input_container = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        input_container.pack(fill=tk.X, pady=(0, 20))
        
        # Input frame
        input_frame = tk.Frame(input_container, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Input field with proper configuration
        self.input_field = tk.Entry(input_frame,
                                   font=('Segoe UI', 12),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   bd=0,
                                   highlightthickness=2,
                                   highlightcolor=self.colors['accent'],
                                   insertbackground=self.colors['text_primary'],
                                   selectbackground=self.colors['accent'],
                                   selectforeground=self.colors['bg_primary'])
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=15)
        
        # Bind events
        self.input_field.bind('<Return>', self.send_message)
        self.input_field.bind('<KeyPress>', self.on_key_press)
        self.input_field.bind('<FocusIn>', self.on_focus_in)
        self.input_field.bind('<FocusOut>', self.on_focus_out)
        
        # Send button
        self.send_button = tk.Button(input_frame,
                                    text="Send ➤",
                                    command=self.send_message,
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['accent'],
                                    fg=self.colors['text_primary'],
                                    bd=0,
                                    relief='flat',
                                    padx=20,
                                    pady=10,
                                    cursor='hand2')
        self.send_button.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Character count
        self.char_count_label = tk.Label(input_container,
                                        text="0 characters",
                                        font=('Segoe UI', 9),
                                        bg=self.colors['bg_primary'],
                                        fg=self.colors['text_secondary'])
        self.char_count_label.pack(anchor=tk.E, padx=5)
    
    def create_action_buttons(self):
        """Create action buttons"""
        buttons_frame = tk.Frame(self.main_container, bg=self.colors['bg_primary'])
        buttons_frame.pack(fill=tk.X)
        
        # Help button
        help_btn = tk.Button(buttons_frame,
                            text="❓ Help",
                            command=self.show_help,
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['bg_tertiary'],
                            fg=self.colors['text_primary'],
                            bd=0,
                            relief='flat',
                            padx=15,
                            pady=8,
                            cursor='hand2')
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(buttons_frame,
                             text="🗑️ Clear",
                             command=self.clear_chat,
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             bd=0,
                             relief='flat',
                             padx=15,
                             pady=8,
                             cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_btn = tk.Button(buttons_frame,
                            text="✕ Exit",
                            command=self.on_closing,
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['error_color'],
                            fg=self.colors['text_primary'],
                            bd=0,
                            relief='flat',
                            padx=15,
                            pady=8,
                            cursor='hand2')
        exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def ensure_input_ready(self):
        """Ensure input field is ready for user interaction"""
        try:
            # Focus on the input field
            self.input_field.focus_set()
            
            # Update status
            self.status_label.config(text="Ready - Type your message")
            
            print("✅ Input field is ready!")
            
        except Exception as e:
            print(f"❌ Error in ensure_input_ready: {e}")
            self.status_label.config(text="Input field error - please restart")
    
    def on_key_press(self, event):
        """Handle key press events"""
        print(f"Key pressed: {event.keysym} | Current text: '{self.input_field.get()}'")
        
        # Update character count
        self.root.after(1, self.update_char_count)
    
    def on_focus_in(self, event):
        """Handle focus in events"""
        print("✅ Input field focused")
        self.status_label.config(text="Type your message...")
    
    def on_focus_out(self, event):
        """Handle focus out events"""
        print("Input field lost focus")
    
    def update_char_count(self):
        """Update character count display"""
        count = len(self.input_field.get())
        self.char_count_label.config(text=f"{count} characters")
    
    def initialize_chat(self):
        """Initialize chat with welcome message"""
        welcome_msg = """✨ Welcome to Aiden - Your AI Assistant! ✨

🎨 Modern Dark Theme Interface
🤖 Powered by Google Gemini AI
✨ Enhanced User Experience

🌟 Features:
• Natural language conversations
• Weather updates and forecasts
• Cryptocurrency and stock prices
• Mathematical calculations
• Password generation
• Creative writing assistance
• And much more!

💡 How to use:
• Type your question in the input field below
• Press Enter or click Send to submit
• Use natural language - I understand context!

How can I help you today?"""
        
        self.add_message("🤖 Aiden", welcome_msg, 'system')
    
    def add_message(self, sender, message, tag='bot'):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Add message with timestamp
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {sender}:\n{message}\n")
        
        # Apply tag for styling
        if tag in ['user', 'bot', 'system', 'error']:
            # Get current content and find the last occurrence of the sender
            content = self.chat_display.get(1.0, tk.END)
            lines = content.split('\n')
            
            # Find the line with the sender and apply tag
            for i in range(len(lines)-1, -1, -1):
                if lines[i].startswith(f"[{timestamp}] {sender}:"):
                    # Calculate line position
                    line_num = i + 1
                    start_pos = f"{line_num}.0"
                    end_pos = f"{line_num}.end"
                    self.chat_display.tag_add(tag, start_pos, end_pos)
                    break
        
        # Add separator line for better readability
        self.chat_display.insert(tk.END, "─" * 50 + "\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Update the UI
        self.root.update_idletasks()
    
    def send_message(self, event=None):
        """Send user message and get bot response"""
        print("🚀 send_message called")
        
        message = self.input_field.get().strip()
        print(f"Message: '{message}'")
        
        if not message:
            print("Empty message, focusing input field")
            self.input_field.focus_set()
            return
        
        # Clear input field
        self.input_field.delete(0, tk.END)
        self.update_char_count()
        
        # Add user message to display
        self.add_message("👤 You", message, 'user')
        
        # Handle exit command
        if message.lower() == 'exit':
            self.on_closing()
            return
        
        # Update status
        self.status_label.config(text="🤔 Thinking...")
        self.send_button.config(state=tk.DISABLED)
        
        # Add typing indicator
        self.show_typing_indicator()
        
        # Process message in separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def show_typing_indicator(self):
        """Show typing indicator animation"""
        self.typing_animation = True
        self.typing_dots = 0
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n🤖 Aiden is typing")
        
        # Animate typing dots
        def animate_dots():
            if self.typing_animation:
                dots = "." * ((self.typing_dots % 3) + 1)
                # Remove previous dots and add new ones
                current_content = self.chat_display.get(tk.END + f"-{3}c", tk.END)
                if current_content.strip() in [".", "..", "..."]:
                    self.chat_display.delete(tk.END + f"-{len(current_content.strip())}c", tk.END)
                self.chat_display.insert(tk.END, dots)
                self.chat_display.see(tk.END)
                self.typing_dots += 1
                self.root.after(500, animate_dots)
        
        animate_dots()
        self.chat_display.config(state=tk.DISABLED)
    
    def remove_typing_indicator(self):
        """Remove typing indicator"""
        self.typing_animation = False
        self.chat_display.config(state=tk.NORMAL)
        
        # Remove the typing indicator line
        content = self.chat_display.get(1.0, tk.END)
        lines = content.split('\n')
        
        # Find and remove the typing line
        for i, line in enumerate(lines):
            if "is typing" in line:
                # Calculate position and remove the line
                line_start = f"{i+1}.0"
                line_end = f"{i+2}.0"
                self.chat_display.delete(line_start, line_end)
                break
        
        self.chat_display.config(state=tk.DISABLED)
    
    def process_message(self, message):
        """Process user message in background thread"""
        try:
            # Get response from AI assistant
            response = process_user_input(message)
            
            # Add to conversation history
            add_to_history(message, response)
            
            # Queue the response for GUI update
            self.message_queue.put(('bot_response', response))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.message_queue.put(('error', error_msg))
    
    def check_queue(self):
        """Check for queued messages and update GUI"""
        try:
            while True:
                message_type, content = self.message_queue.get_nowait()
                
                # Remove typing indicator
                self.remove_typing_indicator()
                
                if message_type == 'bot_response':
                    self.add_message("🤖 Aiden", content, 'bot')
                elif message_type == 'error':
                    self.add_message("❌ Error", content, 'error')
                
                # Re-enable send button and update status
                self.send_button.config(state=tk.NORMAL)
                self.status_label.config(text="Ready - Type your message")
                
                # Focus back on input field
                self.input_field.focus_set()
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Clear conversation history
        conversation_history.clear()
        
        # Add welcome message again
        self.add_message("🤖 Aiden", "✨ Chat cleared! Ready for a fresh start.", 'system')
        
        # Focus on input field
        self.input_field.focus_set()
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🤖 Aiden - Your AI Assistant

🌟 Features:
• Ask me anything using natural language
• Get weather updates, crypto prices, stock info
• Perform calculations and get current time
• Generate passwords and get jokes
• Creative writing assistance

💡 Tips:
• Type your question in the input field below
• Press Enter or click Send to submit
• Use 'clear' to clear the chat
• Type 'exit' to close the application

Ready to help with all your questions!"""
        
        messagebox.showinfo("Help", help_text)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "👋 Do you want to exit Aiden?"):
            self.root.destroy()

def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
