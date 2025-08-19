import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import csv
import time
import threading

# Credentials
username1 = 'example@email.com'
password1 = '$your-password%'
name = 'User'

# Database setup
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    website TEXT NOT NULL,
    usernameTEXT TEXT NOT NULL,
    password TEXT NOT NULL)''')
conn.commit()

# Color scheme inspired by Microsoft Authenticator
COLORS = {
    'primary': '#0078d4',      # Microsoft blue
    'primary_dark': '#106ebe',  # Darker blue for hover
    'secondary': '#f3f2f1',     # Light gray background
    'card_bg': '#ffffff',       # White card background
    'text_primary': '#323130',  # Dark gray text
    'text_secondary': '#605e5c', # Medium gray text
    'border': '#edebe9',        # Light border
    'success': '#107c10',       # Green
    'error': '#d13438',         # Red
    'accent': '#e1dfdd'         # Light accent
}

class ModernFrame(tk.Frame):
    """Custom frame with modern styling"""
    def __init__(self, parent, bg_color=COLORS['card_bg'], **kwargs):
        super().__init__(parent, bg=bg_color, relief='flat', bd=0, **kwargs)

class ModernButton(tk.Button):
    """Custom button with modern styling"""
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        if style == 'primary':
            bg_color = COLORS['primary']
            fg_color = 'white'
            hover_color = COLORS['primary_dark']
        elif style == 'secondary':
            bg_color = COLORS['secondary']
            fg_color = COLORS['text_primary']
            hover_color = COLORS['accent']
        elif style == 'danger':
            bg_color = COLORS['error']
            fg_color = 'white'
            hover_color = '#b71c1c'
        else:
            bg_color = COLORS['card_bg']
            fg_color = COLORS['text_primary']
            hover_color = COLORS['accent']
        
        super().__init__(
            parent, 
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=('Segoe UI', 10),
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            **kwargs
        )
        
        # Hover effects
        self.bind('<Enter>', lambda e: self.config(bg=hover_color))
        self.bind('<Leave>', lambda e: self.config(bg=bg_color))

class ModernEntry(tk.Entry):
    """Custom entry with modern styling"""
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary'],
            highlightbackground=COLORS['border'],
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = COLORS['text_secondary']
        self.default_fg_color = COLORS['text_primary']
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_color)
            self.bind('<FocusIn>', self.clear_placeholder)
            self.bind('<FocusOut>', self.add_placeholder)

    def clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg_color)

    def add_placeholder(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

class ModernLabel(tk.Label):
    """Custom label with modern styling"""
    def __init__(self, parent, text, style='primary', **kwargs):
        if style == 'primary':
            fg_color = COLORS['text_primary']
            font = ('Segoe UI', 10)
        elif style == 'secondary':
            fg_color = COLORS['text_secondary']
            font = ('Segoe UI', 9)
        elif style == 'header':
            fg_color = COLORS['text_primary']
            font = ('Segoe UI', 16, 'bold')
        elif style == 'subheader':
            fg_color = COLORS['text_primary']
            font = ('Segoe UI', 12, 'bold')
        else:
            fg_color = COLORS['text_primary']
            font = ('Segoe UI', 10)
        
        super().__init__(
            parent,
            text=text,
            fg=fg_color,
            bg=parent.cget('bg'),
            font=font,
            **kwargs
        )

class PasswordCard(ModernFrame):
    """Card component for displaying password entries"""
    def __init__(self, parent, website, username, password_id, on_delete=None):
        super().__init__(parent, bg_color=COLORS['card_bg'])
        
        self.password_id = password_id
        self.on_delete = on_delete
        
        # Configure card styling
        self.config(relief='solid', bd=1, highlightbackground=COLORS['border'])
        
        # Main content frame
        content_frame = ModernFrame(self, bg_color=COLORS['card_bg'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Website name (primary text)
        website_label = ModernLabel(content_frame, website, style='subheader')
        website_label.pack(anchor='w')
        
        # Username (secondary text)
        username_label = ModernLabel(content_frame, username, style='secondary')
        username_label.pack(anchor='w', pady=(2, 8))
        
        # Action buttons frame
        button_frame = ModernFrame(content_frame, bg_color=COLORS['card_bg'])
        button_frame.pack(fill='x')
        
        # Delete button (right aligned)
        delete_btn = ModernButton(button_frame, "Delete", 
                                 command=self.delete_password, 
                                 style='danger')
        delete_btn.pack(side='right')
        
        # Copy button (right aligned)
        copy_btn = ModernButton(button_frame, "Copy", 
                               command=self.copy_password, 
                               style='secondary')
        copy_btn.pack(side='right', padx=(0, 10))
        
        # Hover effects for the card
        self.bind('<Enter>', lambda e: self.config(bg=COLORS['secondary']))
        self.bind('<Leave>', lambda e: self.config(bg=COLORS['card_bg']))
        
        # Bind hover to all child widgets
        for child in self.winfo_children():
            self.bind_hover_to_children(child)
    
    def bind_hover_to_children(self, widget):
        """Recursively bind hover effects to all child widgets"""
        widget.bind('<Enter>', lambda e: self.config(bg=COLORS['secondary']))
        widget.bind('<Leave>', lambda e: self.config(bg=COLORS['card_bg']))
        for child in widget.winfo_children():
            self.bind_hover_to_children(child)
    
    def delete_password(self):
        if self.on_delete:
            self.on_delete(self.password_id)
    
    def copy_password(self):
        # Get password from database
        c.execute("SELECT password FROM passwords WHERE id=?", (self.password_id,))
        result = c.fetchone()
        if result:
            self.clipboard_clear()
            self.clipboard_append(result[0])
            messagebox.showinfo("Copied", "Password copied to clipboard!")

# Main App Class

class PasswordManagerApp(tk.Tk):
    AUTOLOCK_SECONDS = 120  # 2 minutes

    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("480x700")
        self.resizable(False, False)
        self.configure(bg=COLORS['secondary'])
        self.user_name = ""
        self.last_activity = time.time()
        self.locked = False

        # Configure style
        self.configure_styles()

        container = ModernFrame(self, bg_color=COLORS['secondary'])
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

        # Accessibility: bind Tab for navigation
        self.bind_all('<Tab>', self.focus_next_widget)
        self.bind_all('<Shift-Tab>', self.focus_prev_widget)

        # Auto-lock: monitor activity
        self.bind_all('<Any-KeyPress>', self.reset_activity)
        self.bind_all('<Any-Button>', self.reset_activity)
        self.after(1000, self.check_inactivity)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_prev_widget(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def reset_activity(self, event=None):
        self.last_activity = time.time()
        if self.locked:
            # If locked, ignore activity until unlocked
            return

    def check_inactivity(self):
        if not self.locked and (time.time() - self.last_activity > self.AUTOLOCK_SECONDS):
            self.lock_app()
        self.after(1000, self.check_inactivity)

    def lock_app(self):
        self.locked = True
        # Show lock screen
        LockScreen(self)

    def unlock_app(self):
        self.locked = False
        self.last_activity = time.time()
        self.show_frame(HomePage)

    def configure_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure scrollbar style
        style.configure('Modern.Vertical.TScrollbar',
                       background=COLORS['secondary'],
                       troughcolor=COLORS['accent'],
                       borderwidth=0,
                       arrowcolor=COLORS['text_secondary'],
                       darkcolor=COLORS['secondary'],
                       lightcolor=COLORS['secondary'])

    def show_frame(self, page):
        frame = self.frames[page]
        if page == HomePage:
            frame.update_welcome(self.user_name)
        frame.tkraise()

# Login Page
class LoginPage(ModernFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg_color=COLORS['secondary'])
        self.controller = controller

        # Center the login card
        login_card = ModernFrame(self, bg_color=COLORS['card_bg'])
        login_card.pack(expand=True, fill='both', padx=40, pady=80)
        
        # Header
        header_label = ModernLabel(login_card, "Password Manager", style='header')
        header_label.pack(pady=(40, 10))
        
        subtitle_label = ModernLabel(login_card, "Sign in to your account", style='secondary')
        subtitle_label.pack(pady=(0, 30))

        # Input fields
        input_frame = ModernFrame(login_card, bg_color=COLORS['card_bg'])
        input_frame.pack(padx=40, pady=20, fill='x')
        
        # Username
        ModernLabel(input_frame, "Email", style='primary').pack(anchor='w', pady=(0, 5))
        self.username_entry = ModernEntry(input_frame, placeholder="Enter your email")
        self.username_entry.pack(fill='x', pady=(0, 15))

        # Password
        ModernLabel(input_frame, "Password", style='primary').pack(anchor='w', pady=(0, 5))
        self.password_entry = ModernEntry(input_frame, placeholder="Enter your password", show="*")
        self.password_entry.pack(fill='x', pady=(0, 15))

        # Name
        ModernLabel(input_frame, "Display Name", style='primary').pack(anchor='w', pady=(0, 5))
        self.name_entry = ModernEntry(input_frame, placeholder="Enter your name")
        self.name_entry.pack(fill='x', pady=(0, 25))

        # Login button
        login_btn = ModernButton(input_frame, "Sign In", command=self.login, style='primary')
        login_btn.pack(fill='x', pady=(0, 40))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        
        # Clear placeholder values
        if username == self.username_entry.placeholder:
            username = ""
        if password == self.password_entry.placeholder:
            password = ""
        if name == self.name_entry.placeholder:
            name = ""
        
        if username == username1 and password == password1:
            self.controller.user_name = name if name else "User"
            self.controller.show_frame(HomePage)
        else:
            messagebox.showerror("Sign In Failed", "Invalid credentials. Please try again.")

# Home Page
class HomePage(ModernFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg_color=COLORS['secondary'])
        self.controller = controller

        # Header section
        header_frame = ModernFrame(self, bg_color=COLORS['card_bg'])
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        
        # Top bar with welcome and logout
        top_bar = ModernFrame(header_frame, bg_color=COLORS['card_bg'])
        top_bar.pack(fill='x', padx=20, pady=15)
        
        self.welcome_label = ModernLabel(top_bar, "", style='header')
        self.welcome_label.pack(side='left')
        
        logout_btn = ModernButton(top_bar, "Sign Out", 
                                 command=lambda: controller.show_frame(LoginPage),
                                 style='secondary')
        logout_btn.pack(side='right')

        # Search section
        search_frame = ModernFrame(header_frame, bg_color=COLORS['card_bg'])
        search_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ModernLabel(search_frame, "Search passwords", style='primary').pack(anchor='w', pady=(0, 5))
        self.search_entry = ModernEntry(search_frame, placeholder="Search by website...")
        self.search_entry.pack(fill='x', pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_passwords())

        # Add password button section
        add_button_frame = ModernFrame(self, bg_color=COLORS['card_bg'])
        add_button_frame.pack(fill='x', padx=20, pady=(10, 0))
        
        button_section = ModernFrame(add_button_frame, bg_color=COLORS['card_bg'])
        button_section.pack(fill='x', padx=20, pady=15)
        
        # Add password button
        add_btn = ModernButton(button_section, "+ Add Password", 
                              command=self.show_add_form, style='primary')
        add_btn.pack(side='left')
        
        # Export button
        export_btn = ModernButton(button_section, "Export CSV", 
                                 command=self.export_passwords, style='secondary')
        export_btn.pack(side='right')
        
        # Add password form (initially hidden)
        self.add_frame = ModernFrame(self, bg_color=COLORS['card_bg'])
        self.add_frame.pack(fill='x', padx=20, pady=(10, 0))
        self.add_frame.pack_forget()  # Hide initially
        
        add_header = ModernFrame(self.add_frame, bg_color=COLORS['card_bg'])
        add_header.pack(fill='x', padx=20, pady=(15, 10))
        
        ModernLabel(add_header, "Add New Password", style='subheader').pack(anchor='w')
        
        # Input fields for new password
        input_frame = ModernFrame(self.add_frame, bg_color=COLORS['card_bg'])
        input_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Website input
        ModernLabel(input_frame, "Website", style='primary').pack(anchor='w', pady=(0, 5))
        self.website_entry = ModernEntry(input_frame, placeholder="e.g., facebook.com")
        self.website_entry.pack(fill='x', pady=(0, 10))
        
        # Username input
        ModernLabel(input_frame, "Username", style='primary').pack(anchor='w', pady=(0, 5))
        self.username_entry = ModernEntry(input_frame, placeholder="Enter username or email")
        self.username_entry.pack(fill='x', pady=(0, 10))
        
        # Password input
        ModernLabel(input_frame, "Password", style='primary').pack(anchor='w', pady=(0, 5))
        self.password_entry = ModernEntry(input_frame, placeholder="Enter password", show="*")
        self.password_entry.pack(fill='x', pady=(0, 15))
        
        # Form action buttons
        form_button_frame = ModernFrame(input_frame, bg_color=COLORS['card_bg'])
        form_button_frame.pack(fill='x', pady=(0, 10))
        
        save_btn = ModernButton(form_button_frame, "Save Password", 
                               command=self.add_password, style='primary')
        save_btn.pack(side='left')
        
        cancel_btn = ModernButton(form_button_frame, "Cancel", 
                                 command=self.hide_add_form, style='secondary')
        cancel_btn.pack(side='left', padx=(10, 0))

        # Passwords list section
        list_frame = ModernFrame(self, bg_color=COLORS['secondary'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        ModernLabel(list_frame, "Your Passwords", style='subheader').pack(anchor='w', pady=(0, 10))
        
        # Scrollable frame for password cards
        self.create_scrollable_frame(list_frame)
        
        self.refresh_passwords()

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame for password cards"""
        # Canvas and scrollbar
        canvas = tk.Canvas(parent, bg=COLORS['secondary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview, 
                                 style='Modern.Vertical.TScrollbar')
        self.scrollable_frame = ModernFrame(canvas, bg_color=COLORS['secondary'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def show_add_form(self):
        """Show the add password form"""
        self.add_frame.pack(fill='x', padx=20, pady=(10, 0), after=self.search_entry.master.master)
        
    def hide_add_form(self):
        """Hide the add password form and clear fields"""
        self.add_frame.pack_forget()
        # Clear entries
        for entry in [self.website_entry, self.username_entry, self.password_entry]:
            entry.delete(0, tk.END)
            entry.add_placeholder(None)
        self.welcome_label.config(text=f"Welcome, {name}")
        self.refresh_passwords()

    def update_welcome(self, name):
        self.welcome_label.config(text=f"Welcome, {name}")
        self.refresh_passwords()

    def get_entry_value(self, entry):
        """Get actual value from entry, ignoring placeholder"""
        value = entry.get()
        return "" if value == entry.placeholder else value

    def add_password(self):
        website = self.get_entry_value(self.website_entry)
        username = self.get_entry_value(self.username_entry)
        password = self.get_entry_value(self.password_entry)

        if website and username and password:
            c.execute("INSERT INTO passwords (website, usernameTEXT, password) VALUES (?, ?, ?)",
                      (website, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Password added successfully!")
            
            # Clear entries and hide form
            self.hide_add_form()
            self.refresh_passwords()
        else:
            messagebox.showwarning("Missing Information", "Please fill in all fields")

    def delete_password(self, password_id):
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?")
        if result:
            c.execute("DELETE FROM passwords WHERE id=?", (password_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Password deleted successfully")
            self.refresh_passwords()

    def export_passwords(self):
        c.execute("SELECT website, usernameTEXT, password FROM passwords ORDER BY website ASC")
        rows = c.fetchall()
        
        if not rows:
            messagebox.showinfo("No Data", "No passwords to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Passwords"
        )
        
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Website', 'Username', 'Password'])
                writer.writerows(rows)
            messagebox.showinfo("Export Complete", f"Passwords exported to {file_path}")

    def refresh_passwords(self):
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get search term
        search_term = self.get_entry_value(self.search_entry).lower()
        
        # Get passwords from database
        c.execute("SELECT id, website, usernameTEXT FROM passwords")
        rows = c.fetchall()
        
        if not rows:
            no_data_label = ModernLabel(self.scrollable_frame, 
                                       "No passwords saved yet", 
                                       style='secondary')
            no_data_label.pack(pady=20)
            return
        
        # Sort by website alphabetically
        rows.sort(key=lambda x: x[1].lower())
        
        # Filter by search term
        filtered_rows = [row for row in rows if search_term in row[1].lower()]
        
        if not filtered_rows:
            no_results_label = ModernLabel(self.scrollable_frame, 
                                         "No passwords match your search", 
                                         style='secondary')
            no_results_label.pack(pady=20)
            return
        
        # Group passwords by first letter
        current_letter = None
        
        for row in filtered_rows:
            website_first_letter = row[1][0].upper()
            
            # Add letter divider if this is a new letter
            if current_letter != website_first_letter:
                current_letter = website_first_letter
                
                # Letter divider frame
                letter_frame = ModernFrame(self.scrollable_frame, bg_color=COLORS['secondary'])
                letter_frame.pack(fill='x', pady=(15, 5))
                
                # Letter label
                letter_label = ModernLabel(letter_frame, current_letter, style='subheader')
                letter_label.config(fg=COLORS['primary'])
                letter_label.pack(anchor='w', padx=10, pady=5)
                
                # Separator line
                separator = tk.Frame(letter_frame, height=1, bg=COLORS['border'])
                separator.pack(fill='x', padx=10)
            
            # Create password card
            card = PasswordCard(self.scrollable_frame, row[1], row[2], row[0], 
                              on_delete=self.delete_password)
            card.pack(fill='x', pady=2)

# Run the app
# Run the app

# Accessibility: Simple tooltip for widgets
class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Lock screen popup
class LockScreen(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Session Locked")
        self.geometry("350x200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close
        self.configure(bg=COLORS['secondary'])

        ModernLabel(self, "Session Locked", style='header').pack(pady=(30, 10))
        ModernLabel(self, "Please re-enter your password to unlock.", style='secondary').pack(pady=(0, 20))

        self.pw_entry = ModernEntry(self, placeholder="Password", show="*")
        self.pw_entry.pack(pady=(0, 10), padx=40, fill='x')
        self.pw_entry.focus_set()
        unlock_btn = ModernButton(self, "Unlock", command=self.try_unlock, style='primary')
        unlock_btn.pack(pady=(0, 10))
        ToolTip(unlock_btn, "Unlock the app")

        self.bind('<Return>', lambda e: self.try_unlock())

    def try_unlock(self):
        if self.pw_entry.get() == password1:
            self.destroy()
            self.app.unlock_app()
        else:
            messagebox.showerror("Unlock Failed", "Incorrect password.")

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
