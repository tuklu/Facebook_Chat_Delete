import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class PlaceholderLineEdit(QtWidgets.QLineEdit):
    def __init__(self, placeholder, border_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder
        self.border_color = border_color
        self.setPlaceholderText(self.placeholder)

        # Default style for not focused
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(116, 129, 130, 0.1); /* Not focused transparency */
                color: grey;  /* Placeholder color */
                border: 2px solid {self.border_color}; /* Full border */
                padding: 5px;
            }}
        """)

    def focusInEvent(self, event):
        # When focused
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(116, 129, 130, 0.4); /* Focused transparency */
                color: black;  /* Text color when focused */
                border: none; /* Remove full border */
                border-bottom: 2px solid {self.border_color}; /* Only bottom border */
                padding: 5px;
            }}
        """)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # When focus is lost and input is empty (restore placeholder and initial style)
        if not self.text():
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: rgba(116, 129, 130, 0.1); /* Not focused transparency */
                    color: grey;  /* Placeholder color */
                    border: 2px solid {self.border_color}; /* Full border */
                    padding: 5px;
                }}
            """)
        else:
            # Keep the style for entered text (with full border when not focused)
            self.setStyleSheet(f"""
                QLineEdit {{
                    background-color: rgba(116, 129, 130, 0.1); /* Not focused transparency */
                    color: black;  /* Entered text color */
                    border: 2px solid {self.border_color}; /* Full border */
                    padding: 5px;
                }}
            """)
        super().focusOutEvent(event)


class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Remove title bar and make window non-resizable
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1916, 1186)  # Replace with desired fixed size

        # Get screen size
        screen_width = self.screen().size().width()
        screen_height = self.screen().size().height()

        # Original reference size for 3200x2000 resolution
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

        # Set window properties
        self.setGeometry(position_x, position_y, window_width, window_height)

        # Load background image
        self.bg_image = QtGui.QImage("styled_background.png")  # Replace with your image filename
        self.bg_image = self.bg_image.scaled(window_width, window_height, QtCore.Qt.KeepAspectRatio)

        # Create a QLabel for the background
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(0, 0, window_width, window_height)
        self.bg_label.setPixmap(QtGui.QPixmap.fromImage(self.bg_image))
        self.bg_label.setScaledContents(True)

        # Create and place login form elements directly on the main widget
        login_frame_x = int(1234 * scale)
        login_frame_y = int(506 * scale)

        self.username_input = PlaceholderLineEdit("Username", "#AA40CF", self)
        self.username_input.setGeometry(login_frame_x, login_frame_y, int(400 * scale), 55)
        self.username_input.raise_()  # Ensure it's above the background

        self.password_input = PlaceholderLineEdit("Password", "#487AFA", self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setGeometry(login_frame_x, login_frame_y + 85, int(400 * scale), 55)
        self.password_input.raise_()  # Ensure it's above the background

        # Add the eye icon to toggle password visibility
        self.eye_button = QtWidgets.QPushButton(self)
        self.eye_button.setIcon(QtGui.QIcon("hidden.png"))  # Start with closed eye icon
        self.eye_button.setGeometry(login_frame_x + int(400 * scale) - 40, login_frame_y + 95, 25, 25)
        self.eye_button.setCheckable(True)
        self.eye_button.setFlat(True)
        self.eye_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: none;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        # Delete button
        self.delete_button = QtWidgets.QPushButton("Delete all chats", self)
        self.delete_button.setGeometry(login_frame_x, login_frame_y + 180, int(400 * scale), 65)
        self.delete_button.clicked.connect(self.delete_chats)
        self.delete_button.raise_()
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #628EFF,
                    stop: 0.53 #8740CD,
                    stop: 1 #580475);
                color: #BCD3E4;
                border: none;
                border-radius: 5px;
                font-size: 28px;
                font-family: "Nano Sans", sans-serif;
                font-weight: 600;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #7BB6FF,
                    stop: 0.53 #A03ECD,
                    stop: 1 #6F0475);
            }
        """)

        class ShrinkingButton(QtWidgets.QPushButton):
            def __init__(self, icon_path, parent=None):
                super().__init__(parent)
                self.setIcon(QtGui.QIcon("close.png"))  # Set the icon
                self.setIconSize(QtCore.QSize(60, 60))  # Set the icon size
                self.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: rgba(255, 255, 255, 0);  /* Transparent by default */
                    }
                """)

                self.setFixedSize(60, 60)  # Set a fixed size for the button

            def mousePressEvent(self, event):
                """ Shrink the button when clicked """
                self.setIconSize(QtCore.QSize(50, 50))  # Shrink the icon
                super().mousePressEvent(event)  # Call the original method

            def mouseReleaseEvent(self, event):
                """ Restore the original size after click and close the parent """
                self.setIconSize(QtCore.QSize(60, 60))  # Restore the original icon size
                super().mouseReleaseEvent(event)  # Call the original method
                QtCore.QTimer.singleShot(250, self.parent().close)

            def paintEvent(self, event):
                """ Draw gradient circles on hover """
                painter = QtGui.QPainter(self)
                rect = self.rect()
                if self.underMouse():  # Check if the mouse is over the button
                    # Create a radial gradient for the background
                    gradient = QtGui.QRadialGradient(rect.center(), 30)  # Adjust the radius for the glow
                    gradient.setColorAt(0, QtGui.QColor(255, 0, 0, 150))  # Red center with some transparency
                    gradient.setColorAt(1, QtGui.QColor(255, 0, 0, 0))  # Transparent red at the edges

                    # Draw the gradient
                    painter.setBrush(gradient)
                    painter.setPen(QtCore.Qt.NoPen)
                    painter.drawEllipse(rect.adjusted(-10, -10, 10, 10))  # Draw the glowing effect around the button

                super().paintEvent(event)  # Call the original paint event

        # Usage in your window setup
        self.close_button = ShrinkingButton("close.png", self)  # Use your close icon path here
        self.close_button.setGeometry(window_width - 115, 50, 60, 60)  # Set button size and position


    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)  # Show the password
            self.eye_button.setIcon(QtGui.QIcon("visibility.png"))  # Change to open eye icon
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Hide the password
            self.eye_button.setIcon(QtGui.QIcon("hidden.png"))  # Change back to closed eye icon

    def delete_chats(self):
        # Implement the delete chats functionality here
        print("Deleting all chats...")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
