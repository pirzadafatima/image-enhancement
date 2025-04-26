import tkinter as tk
from tkinter import filedialog, Entry
import numpy as np
from PIL import Image, ImageTk


def get_sl_elements(elements, M):
    sl_elements = []
    if len(elements) <= M:
        return elements
    for i in range(len(elements) - M + 1):
        sl_elements.append(elements[i:i + M])
    return sl_elements


def calculate_maximin(sl_elements):
    maxi_min = [min(subsequence) for subsequence in sl_elements]
    return max(maxi_min)


def calculate_minimax(sl_elements):
    mini_max = [max(subsequence) for subsequence in sl_elements]
    return min(mini_max)


def pmed_filter(image, window_size):
    # Convert the image to a numpy array
    img_array = np.array(image)

    # Apply Pmed filter to each pixel
    height, width = img_array.shape
    enhanced_image = np.zeros_like(img_array, dtype=np.float32)

    if window_size % 2 == 0:
        window_size = window_size + 1     # even can not have exact centre

    half_window = window_size // 2
    padded_img_array = np.pad(img_array, half_window, mode='edge')

    L = window_size*window_size
    M = int((L + 1) / 2)  # Convert M to an integer

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
            SL = window.flatten()

            sl_elements = get_sl_elements(SL, M)
            maximin = calculate_maximin(sl_elements)
            minimax = calculate_minimax(sl_elements)

            enhanced_image[y, x] = 0.5*maximin + 0.5*minimax

    # Convert the numpy array back to an Image
    enhanced_image = Image.fromarray(enhanced_image)

    return enhanced_image


def upload_image():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        display_image(original_image)
        pMedButton['state'] = 'normal'  # Enable the pmed button


def display_image(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def display_image_op(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    op_label.config(image=img_tk)
    op_label.image = img_tk


def apply_pmed():
    pmed_window = tk.Toplevel()
    pmed_window.title('PMED Filter Parameters')

    # Labels and Entry widgets for user input
    tk.Label(pmed_window, text='Window Size:').pack()
    window_size_entry = Entry(pmed_window)
    window_size_entry.pack()

    def apply_pmed_filter():
        window_size = int(window_size_entry.get())

        pixel_color = original_image.getpixel((0, 0))

        if type(pixel_color) == tuple:
            oi = Image.Image.split(original_image)
            red_channel, green_channel, blue_channel = oi[0], oi[1], oi[2]

            # Apply pmed filter to each channel separately
            enhanced_red_channel = pmed_filter(red_channel, window_size).convert('L')
            enhanced_green_channel = pmed_filter(green_channel, window_size).convert('L')
            enhanced_blue_channel = pmed_filter(blue_channel, window_size).convert('L')

            # Merge the enhanced channels back into an RGB image
            enhanced_image_rgb = Image.merge('RGB', (enhanced_red_channel, enhanced_green_channel, enhanced_blue_channel))

            display_image(original_image)
            display_image_op(enhanced_image_rgb)
        else:
            enhanced_image = pmed_filter(original_image, window_size)

            # Display the enhanced image
            display_image(original_image)
            display_image_op(enhanced_image)

    tk.Button(pmed_window, text='Apply PseudoMedian', command=apply_pmed_filter).pack()


root = tk.Tk()
root.title('PseudoMedian')

# Buttons
uploadButton = tk.Button(root, text='Upload Image', command=upload_image)
label = tk.Label(root)
pMedButton = tk.Button(root, text='Apply PseudoMedian Filter', command=apply_pmed, state='disabled')
op_label = tk.Label(root)
uploadButton.pack(pady=10)
label.pack()
op_label.pack()
pMedButton.pack(pady=10)

# Variable to store the original image
original_image = None

# Run the GUI
root.mainloop()
