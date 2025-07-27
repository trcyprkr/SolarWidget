import tkinter as tk
import requests
from PIL import Image, ImageTk
import io
import webbrowser
import ctypes

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)  # 0 = Hide

class SolarWidget:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window borders
        self.root.attributes("-topmost", False)  # Keep widget on top
        self.root.attributes("-alpha", 0.8)  # Set transparency (0.0 to 1.0)
        self.root.geometry("+50+50")  # Position at (50,50)

        # Styling
        self.root.configure(bg="#333333")  # Dark background for centering effect

        # Image label (centered)
        self.label = tk.Label(root, bg="#333333", borderwidth=0)
        self.label.pack(pady=10, padx=10)

        # URL for the solar data image and link
        self.image_url = "https://www.hamqsl.com/solar101vhf.php"
        self.link_url = "https://www.hamqsl.com/solar.html"

        # Dragging functionality
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<Button-3>", self.close_widget)  # Right-click to close
        self.label.bind("<Button-2>", self.open_link)  # Middle-click to open URL

        # Load and display the image
        self.update_image()

    def start_drag(self, event):
        self.drag_start_x = event.x_root - self.root.winfo_x()
        self.drag_start_y = event.y_root - self.root.winfo_y()

    def on_drag(self, event):
        x = event.x_root - self.drag_start_x
        y = event.y_root - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def close_widget(self, event):
        self.root.destroy()

    def open_link(self, event):
        webbrowser.open(self.link_url)

    def update_image(self):
        try:
            # Fetch the image
            response = requests.get(self.image_url, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            image_data = response.content

            # Convert image data to Tkinter-compatible format
            image = Image.open(io.BytesIO(image_data))
            self.photo = ImageTk.PhotoImage(image)

            # Update label with new image
            self.label.configure(image=self.photo)

            # Adjust window size to fit image
            self.root.geometry(f"{image.width + 20}x{image.height + 20}+{self.root.winfo_x()}+{self.root.winfo_y()}")

        except Exception as e:
            # Display error if image fetch fails
            self.label.configure(image="", text=f"Error: {str(e)}", fg="white", font=("Arial", 12))

        # Schedule next update (every 15 minutes)
        self.root.after(90000, self.update_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarWidget(root)
    root.mainloop()
