import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Configure style
        try:
            style = ttk.Style()
            style.theme_use('clam')
        except:
            pass  # Use default theme if clam is not available
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Password Generator", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Password length
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="10")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(length_frame, from_=4, to=50, 
                                orient=tk.HORIZONTAL, variable=self.length_var,
                                command=self.update_length_label)
        length_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.length_label = ttk.Label(length_frame, text="12", font=('Arial', 10, 'bold'))
        self.length_label.grid(row=0, column=1)
        
        length_frame.columnconfigure(0, weight=1)
        
        # Character options
        options_frame = ttk.LabelFrame(main_frame, text="Character Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="✓ Uppercase Letters (A-Z)", 
                       variable=self.uppercase_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="✓ Lowercase Letters (a-z)", 
                       variable=self.lowercase_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="✓ Numbers (0-9)", 
                       variable=self.numbers_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="✓ Special Characters (!@#$%^&*)", 
                       variable=self.symbols_var).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options", padding="10")
        advanced_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        self.no_duplicate_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(advanced_frame, text="Exclude ambiguous characters (0, O, l, I, 1)", 
                       variable=self.exclude_ambiguous_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(advanced_frame, text="No duplicate characters", 
                       variable=self.no_duplicate_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="🎲 Generate Password", 
                                 command=self.generate_password)
        generate_btn.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Password display
        password_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        password_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.password_var = tk.StringVar(value="Click 'Generate Password' to create a password")
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                  font=('Courier', 11), state='readonly', width=40)
        password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        copy_btn = ttk.Button(password_frame, text="📋 Copy", command=self.copy_password)
        copy_btn.grid(row=0, column=1)
        
        password_frame.columnconfigure(0, weight=1)
        
        # Strength indicator
        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", padding="10")
        strength_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.strength_var = tk.StringVar(value="Generate a password to see its strength")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var, 
                                       font=('Arial', 10, 'bold'))
        self.strength_label.grid(row=0, column=0)
        
        self.strength_bar = ttk.Progressbar(strength_frame, length=350, mode='determinate')
        self.strength_bar.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
        
        strength_frame.columnconfigure(0, weight=1)
        
        # Batch generation
        batch_frame = ttk.LabelFrame(main_frame, text="Batch Generation", padding="10")
        batch_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        batch_inner_frame = ttk.Frame(batch_frame)
        batch_inner_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(batch_inner_frame, text="Number of passwords:").grid(row=0, column=0, padx=(0, 10))
        self.batch_count_var = tk.IntVar(value=5)
        batch_spinbox = ttk.Spinbox(batch_inner_frame, from_=1, to=20, width=8, 
                                   textvariable=self.batch_count_var)
        batch_spinbox.grid(row=0, column=1, padx=(0, 10))
        
        batch_btn = ttk.Button(batch_inner_frame, text="🔢 Generate Multiple", 
                              command=self.generate_multiple_passwords)
        batch_btn.grid(row=0, column=2)
        
        batch_frame.columnconfigure(0, weight=1)
        
        # Configure main frame
        main_frame.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
    
    def update_length_label(self, value):
        """Update the length label when scale changes"""
        self.length_label.config(text=str(int(float(value))))
    
    def get_character_set(self):
        """Build character set based on selected options"""
        chars = ""
        
        if self.uppercase_var.get():
            chars += string.ascii_uppercase
        if self.lowercase_var.get():
            chars += string.ascii_lowercase
        if self.numbers_var.get():
            chars += string.digits
        if self.symbols_var.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Remove ambiguous characters if selected
        if self.exclude_ambiguous_var.get():
            ambiguous = "0Ol1I"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        return chars
    
    def generate_password(self):
        """Generate a single password"""
        try:
            chars = self.get_character_set()
            
            if not chars:
                messagebox.showerror("Error", "Please select at least one character type!")
                return
            
            length = int(self.length_var.get())
            
            if self.no_duplicate_var.get() and length > len(chars):
                messagebox.showerror("Error", 
                                   f"Cannot generate {length} character password without duplicates.\n"
                                   f"Maximum length with current settings: {len(chars)}")
                return
            
            if self.no_duplicate_var.get():
                password = ''.join(random.sample(chars, length))
            else:
                password = ''.join(random.choice(chars) for _ in range(length))
            
            self.password_var.set(password)
            self.update_strength_indicator(password)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating password: {str(e)}")
    
    def update_strength_indicator(self, password):
        """Update password strength indicator"""
        try:
            score = 0
            feedback = []
            
            # Length check
            if len(password) >= 16:
                score += 30
            elif len(password) >= 12:
                score += 25
            elif len(password) >= 8:
                score += 15
            else:
                feedback.append("Use at least 8 characters")
            
            # Character variety
            if any(c.isupper() for c in password):
                score += 20
            else:
                feedback.append("Add uppercase letters")
                
            if any(c.islower() for c in password):
                score += 20
            else:
                feedback.append("Add lowercase letters")
                
            if any(c.isdigit() for c in password):
                score += 15
            else:
                feedback.append("Add numbers")
                
            if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                score += 15
            else:
                feedback.append("Add special characters")
            
            # Update progress bar and label
            self.strength_bar['value'] = min(score, 100)
            
            if score >= 80:
                strength_text = "🟢 Very Strong"
            elif score >= 60:
                strength_text = "🔵 Strong"
            elif score >= 40:
                strength_text = "🟡 Medium"
            else:
                strength_text = "🔴 Weak"
            
            self.strength_var.set(f"{strength_text} (Score: {min(score, 100)}/100)")
            
        except Exception as e:
            self.strength_var.set("Error calculating strength")
    
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_var.get()
        if password and password != "Click 'Generate Password' to create a password":
            try:
                # Try using tkinter's clipboard first
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()  # Ensure clipboard is updated
                messagebox.showinfo("✅ Success", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy password: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No password to copy! Generate a password first.")
    
    def generate_multiple_passwords(self):
        """Generate multiple passwords and display in new window"""
        try:
            chars = self.get_character_set()
            
            if not chars:
                messagebox.showerror("Error", "Please select at least one character type!")
                return
            
            count = int(self.batch_count_var.get())
            length = int(self.length_var.get())
            
            if self.no_duplicate_var.get() and length > len(chars):
                messagebox.showerror("Error", 
                                   f"Cannot generate {length} character passwords without duplicates.\n"
                                   f"Maximum length with current settings: {len(chars)}")
                return
            
            passwords = []
            for i in range(count):
                if self.no_duplicate_var.get():
                    password = ''.join(random.sample(chars, min(length, len(chars))))
                else:
                    password = ''.join(random.choice(chars) for _ in range(length))
                passwords.append(password)
            
            # Create new window to display passwords
            batch_window = tk.Toplevel(self.root)
            batch_window.title(f"Generated {count} Passwords")
            batch_window.geometry("650x450")
            batch_window.resizable(True, True)
            
            # Header frame
            header_frame = ttk.Frame(batch_window)
            header_frame.pack(fill=tk.X, padx=10, pady=10)
            
            ttk.Label(header_frame, text=f"🔐 Generated {count} Passwords", 
                     font=('Arial', 14, 'bold')).pack()
            
            # Text widget with scrollbar
            text_frame = ttk.Frame(batch_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            text_widget = tk.Text(text_frame, font=('Courier', 10), wrap=tk.NONE)
            v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_widget.xview)
            
            text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            
            text_frame.grid_rowconfigure(0, weight=1)
            text_frame.grid_columnconfigure(0, weight=1)
            
            # Insert passwords
            for i, password in enumerate(passwords, 1):
                text_widget.insert(tk.END, f"{i:2d}. {password}\n")
            
            text_widget.config(state=tk.DISABLED)
            
            # Button frame
            button_frame = ttk.Frame(batch_window)
            button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            copy_all_btn = ttk.Button(button_frame, text="📋 Copy All Passwords",
                                     command=lambda: self.copy_all_passwords(passwords))
            copy_all_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            close_btn = ttk.Button(button_frame, text="❌ Close", 
                                  command=batch_window.destroy)
            close_btn.pack(side=tk.RIGHT)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating passwords: {str(e)}")
    
    def copy_all_passwords(self, passwords):
        """Copy all generated passwords to clipboard"""
        try:
            all_passwords = '\n'.join(f"{i:2d}. {pwd}" for i, pwd in enumerate(passwords, 1))
            self.root.clipboard_clear()
            self.root.clipboard_append(all_passwords)
            self.root.update()
            messagebox.showinfo("✅ Success", f"All {len(passwords)} passwords copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy passwords: {str(e)}")

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        
        # Center the window on screen
        root.eval('tk::PlaceWindow . center')
        
        # Set minimum size
        root.minsize(500, 650)
        
        app = PasswordGenerator(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        messagebox.showerror("Startup Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()