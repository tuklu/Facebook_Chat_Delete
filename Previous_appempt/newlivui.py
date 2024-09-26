import customtkinter as ctk
from PIL import Image

class LoginPage(ctk.CTk):
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
        self.bg_photo = ctk.CTkImage(self.bg_image, size=(window_width, window_height))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Directly place login form elements without a frame
        input_width = int(400 * scale)
        input_x = int(1234 * scale)
        input_y = int(506 * scale)

        # Add transparent entries with placeholder text
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        # Username entry (transparent background)
        self.username_entry = ctk.CTkEntry(self, textvariable=self.username_var, placeholder_text="Enter your username", width=input_width, corner_radius=5, fg_color="transparent",text_color="#4158D0", border_color="blue", border_width=2)
        self.username_entry.place(x=input_x, y=input_y)

        # Password entry (transparent background)
        self.password_entry = ctk.CTkEntry(self, textvariable=self.password_var, placeholder_text="Enter your Password", show="*", width=input_width, fg_color="transparent")
        self.password_entry.place(x=input_x, y=input_y + int(85 * scale))  # Added breathing space


        # Button image size
        button_width = input_width
        button_height = int(55 * scale)  # Set a fixed height for consistency

        # Load and create the button image
        try:
            button_image = ctk.CTkImage(light_image=Image.open("button.png"), size=(button_width, button_height))
        except Exception as e:
            print(f"Error loading image: {e}")
            button_image = None  # Fallback in case of error

        # Create the button
        delete_button = ctk.CTkButton(
            self,
            text="Delete all chats",  # Text to be displayed over the image
            image=button_image,
            command=self.delete_chats,
            width=button_width,
            height=button_height,
            compound="center",  # Place the text centered over the image
            bg_color="transparent" if button_image else "blue"  # Set background color conditionally
        )

        # Ensure the button displays correctly
        delete_button.place(x=input_x, y=input_y + int(180 * scale))  # Added more breathing space



    def delete_chats(self):
        # Implement the delete chats functionality here
        print("Deleting all chats...")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # You can change to "dark" if needed
    ctk.set_default_color_theme("blue")  # Default color theme
    app = LoginPage()
    app.mainloop()
