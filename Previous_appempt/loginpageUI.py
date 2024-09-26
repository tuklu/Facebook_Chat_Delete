import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # No need for ImageResampling

class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['foreground']
        
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        
        self.put_placeholder()
        
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color
            
    def foc_in(self, *args):
        if self['foreground'] == self.placeholder_color:
            self.delete('0', 'end')
            self['foreground'] = self.default_fg_color
        
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Get screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Original reference size (1916x1186) for 3200x2000 resolution
        original_width = 1916
        original_height = 1186
        original_screen_width = 3200
        original_screen_height = 2000
        
        # Calculate scaling factor based on the screen resolution
        scale_w = screen_width / original_screen_width
        scale_h = screen_height / original_screen_height
        scale = min(scale_w, scale_h)  # Maintain the aspect ratio
        
        # Calculate new window size
        window_width = int(original_width * scale)
        window_height = int(original_height * scale)
        
        # Center the window on the screen
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        
        # Remove the window title bar
        # self.overrideredirect(True)
        
        # Set the window size and position
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
        # Load and set the background image
        self.bg_image = Image.open("styled_background.png")  # Replace with your image filename
        self.bg_image = self.bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a frame for the login form (keep relative position)
        login_frame_width = int(400 * scale)
        login_frame_height = int(215 * scale)
        login_frame_x = int(1234 * scale)
        login_frame_y = int(506 * scale)
        
        self.login_frame = ttk.Frame(self, style='TFrame')
        self.login_frame.place(x=login_frame_x, y=login_frame_y, width=login_frame_width, height=login_frame_height)
        
        # Create and place login form elements
        # ttk.Label(self.login_frame, text="Login", font=("Noto Sans", int(20 * scale))).pack(pady=int(10 * scale))
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        PlaceholderEntry(self.login_frame, "Username", textvariable=self.username_var).pack(pady=int(10 * scale), padx=int(20 * scale), fill='x')
        PlaceholderEntry(self.login_frame, "Password", textvariable=self.password_var, show="*").pack(pady=int(10 * scale), padx=int(20 * scale), fill='x')
        
        ttk.Button(self.login_frame, text="Delete all chats", command=self.delete_chats).pack(pady=int(20 * scale))

    def delete_chats(self):
        # Implement the delete chats functionality here
        print("Deleting all chats...")

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
