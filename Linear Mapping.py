import tkinter as tk
from tkinter import Label, Button, filedialog, Entry
import numpy as np
from PIL import Image, ImageTk

def linear_mapping(image, start, end, initial, slope):
    # Convert the image to a numpy array
    img_array = np.array(image)

    # Apply linear mapping to each pixel
    mapped_image = (img_array - start) * slope + initial

    # Convert the numpy array back to an Image
    mapped_image = Image.fromarray(mapped_image)

    return mapped_image

def uploadImage():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path).convert('L')  # Convert to grayscale

        # Find the maximum intensity value
        max_grey_level = original_image.getextrema()[1]  # Get the maximum value from the image histogram

        print("Max Grey Level:", max_grey_level)
        #original_image = Image.open(file_path)
        displayImage(original_image)
        mappingButton['state'] = 'normal'  # Enable the linear mapping button

def displayImage(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def apply_linear_mapping():
    linear_mapping_window = tk.Toplevel()
    linear_mapping_window.title('Linear Mapping GUI')

    # Labels and Entry widgets for user input
    tk.Label(linear_mapping_window, text='Start:').pack()
    start_entry = Entry(linear_mapping_window)
    start_entry.pack()

    tk.Label(linear_mapping_window, text='End:').pack()
    end_entry = Entry(linear_mapping_window)
    end_entry.pack()

    tk.Label(linear_mapping_window, text='Initial Mapping Point:').pack()
    initial_entry = Entry(linear_mapping_window)
    initial_entry.pack()

    tk.Label(linear_mapping_window, text='Slope:').pack()
    slope_entry = Entry(linear_mapping_window)
    slope_entry.pack()

    def apply_mapping():
        # Get user inputs
        start_val = float(start_entry.get())
        end_val = float(end_entry.get())
        initial_val = float(initial_entry.get())
        slope_val = float(slope_entry.get())

        # Apply linear mapping to the image
        mapped_image = linear_mapping(original_image, start_val, end_val, initial_val, slope_val)

        # Display the mapped image
        mapped_img_tk = ImageTk.PhotoImage(mapped_image)
        mapped_label = Label(linear_mapping_window, image=mapped_img_tk)
        mapped_label.image = mapped_img_tk
        mapped_label.pack(pady=10)

    tk.Button(linear_mapping_window, text='Apply Mapping', command=apply_mapping).pack()

root = tk.Tk()
root.title('Linear Mapping GUI')

# Buttons
uploadButton = tk.Button(root, text='Upload Image', command=uploadImage)
label = tk.Label(root)
mappingButton = tk.Button(root, text='Linear Mapping', command=apply_linear_mapping, state='disabled')
uploadButton.pack(pady=10)
label.pack()
mappingButton.pack(pady=10)

# Variable to store the original image
original_image = None

# Run the GUI
root.mainloop()
