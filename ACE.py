import tkinter as tk
from tkinter import Label, Button, filedialog, Entry
import numpy as np
from PIL import Image, ImageTk


def ace_filter(image, window_size, k1, k2):
    # Convert the image to a numpy array
    img_array = np.array(image)

    # Apply ACE filter to each pixel
    height, width = img_array.shape
    enhanced_image = np.zeros_like(img_array, dtype=np.float32)

    if window_size % 2 == 0:
        window_size = window_size + 1     # even can not have exact centre

    half_window = window_size // 2
    padded_img_array = np.pad(img_array, half_window, mode='edge')

    for y in range(height):
        for x in range(width):

            # Define window boundaries
            row = x + half_window
            col = y + half_window

            x_start = row - half_window
            x_end = (row + half_window) + 1  # Adjusted for indexing
            y_start = col - half_window
            y_end = (col + half_window) + 1

            print(x_start, x_end, y_start, y_end)

            # Extract the window region
            window = padded_img_array[y_start:y_end, x_start:x_end]

            # Calculate local mean and standard deviation
            mean = np.mean(window)
            std_dev = np.std(window)

            enhanced_image[y, x] = (k1 * (np.mean(padded_img_array) / std_dev) * (padded_img_array[col, row] - mean) +
                                    (mean * k2))

    # Convert the numpy array back to an Image
    enhanced_image = Image.fromarray(enhanced_image)

    return enhanced_image


def uploadImage():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path).convert('L')  # Convert to grayscale
        displayImage(original_image)
        aceButton['state'] = 'normal'  # Enable the ACE button


def displayImage(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def displayImage_op(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    op_label.config(image=img_tk)
    op_label.image = img_tk


def apply_ace():
    ace_window = tk.Toplevel()
    ace_window.title('ACE Filter Parameters')

    # Labels and Entry widgets for user input
    tk.Label(ace_window, text='Window Size:').pack()
    window_size_entry = Entry(ace_window)
    window_size_entry.pack()

    tk.Label(ace_window, text='k1:').pack()
    k1_entry = Entry(ace_window)
    k1_entry.pack()

    tk.Label(ace_window, text='k2:').pack()
    k2_entry = Entry(ace_window)
    k2_entry.pack()

    def apply_ace_filter():
        # Get user inputs
        window_size = int(window_size_entry.get())
        k1 = float(k1_entry.get())
        k2 = float(k2_entry.get())

        # Apply ACE filter to the image
        enhanced_image = ace_filter(original_image, window_size, k1, k2)

        # Display the enhanced image
        displayImage(original_image)
        displayImage_op(enhanced_image)

    tk.Button(ace_window, text='Apply ACE', command=apply_ace_filter).pack()


root = tk.Tk()
root.title('ACE Filter GUI')

# Buttons
uploadButton = tk.Button(root, text='Upload Image', command=uploadImage)
label = tk.Label(root)
aceButton = tk.Button(root, text='Apply ACE', command=apply_ace, state='disabled')
op_label = tk.Label(root)
uploadButton.pack(pady=10)
label.pack()
op_label.pack()
aceButton.pack(pady=10)

# Variable to store the original image
original_image = None

# Run the GUI
root.mainloop()