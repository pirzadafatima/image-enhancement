from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import numpy as np

def digitalNegative(pic):

    if pic is not None and hasattr(pic, 'size'):
        width, height = pic.size

        max_intensity = np.max(pic)
        print(max_intensity)

        for x in range(width):
            for y in range(height):
                pixel_color = pic.getpixel((x, y))

                if type(pixel_color) == tuple:
                    red_pixel = max_intensity - pixel_color[0]
                    green_pixel = max_intensity - pixel_color[1]
                    blue_pixel = max_intensity - pixel_color[2]
                    pic.putpixel((x, y), (red_pixel, green_pixel, blue_pixel))

                else:
                    pixel_color = max_intensity - pixel_color
                    pic.putpixel((x, y), pixel_color)
        return pic
    else:
        print("Error: Invalid image type or image not loaded.")
        return None

def uploadImage():
    global original_image  # Use the global variable
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path)  # Update the global variable
        displayImage(original_image)

def displayImage(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk
    DNbutton['state'] = 'normal'  # Enable the digital negative button

def applyDN():
    global original_image
    if original_image is not None:
        original_image = digitalNegative(original_image)
        displayImage(original_image)

# GUI Initialization
root = tk.Tk()
root.title('Digital Negative Application')

# Buttons
uploadButton = tk.Button(root, text='Upload Image', command=uploadImage)
label = tk.Label(root)  # create a Tkinter Label widget. later it will be replaced by the uploaded image
DNbutton = tk.Button(root, text='Apply Digital Negative', command=applyDN, state='disabled')
uploadButton.pack(pady=10)
label.pack()
DNbutton.pack(pady=10)

# Variable to store the original image
original_image = None

# Run the GUI
root.mainloop()
