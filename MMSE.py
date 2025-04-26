import tkinter as tk
from tkinter import filedialog, Entry
import numpy as np
from PIL import Image, ImageTk

def add_gaussian_noise(image, mean=0, std=25):

    img_array = np.array(image)

    # Generate Gaussian noise with the same shape as the image
    noise = np.random.normal(mean, std, img_array.shape)

    # Add the noise to the image
    noisy_image = img_array + noise
    noisy_image = np.clip(noisy_image, 0, 255)

    # Convert the numpy array back to an Image
    noisy_image = Image.fromarray(noisy_image.astype(np.uint8))
    return noisy_image

def mmse_filter(image, window_size, noise_variance):
    # Convert the image to a numpy array
    img_array = np.array(image)

    # Apply ACE filter to each pixel
    height, width = img_array.shape
    enhanced_image = np.zeros_like(img_array, dtype=np.float32)

    if window_size % 2 == 0:
        window_size = window_size + 1  # even can not have exact centre

    half_window = window_size // 2
    padded_img_array = np.pad(img_array, half_window, mode='constant')

    for y in range(height):
        for x in range(width):
            # Define window boundaries
            row = x + half_window
            col = y + half_window

            x_start = row - half_window
            x_end = (row + half_window) + 1  # Adjusted for indexing
            y_start = col - half_window
            y_end = (col + half_window) + 1

            # Extract the window region
            window = padded_img_array[y_start:y_end, x_start:x_end]
            print(x_start, x_end, y_start, y_end)

            # Calculate local mean and standard deviation
            mean = np.sum(window) / (window_size ** 2)
            variance = np.sum((window - mean) ** 2) / ((window_size ** 2) - 1)

            enhanced_image[y, x] = padded_img_array[col, row] - (noise_variance/variance)*(padded_img_array[col, row] - mean)

    # Convert the numpy array back to an Image
    enhanced_image = Image.fromarray(enhanced_image)

    return enhanced_image

def upload_image(label, op_label):
    global original_image, noisy_image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        noisy_image = add_gaussian_noise(original_image)
        display_image(original_image, label)
        display_image(noisy_image, op_label)
        mmseButton['state'] = 'normal'

def display_image(img, label):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def apply_mmse():
    mmse_window = tk.Toplevel()
    mmse_window.title('MMSE Filter Parameters')

    # Labels and Entry widgets for user input
    tk.Label(mmse_window, text='Window Size:').pack()
    window_size_entry = Entry(mmse_window)
    window_size_entry.pack()

    tk.Label(mmse_window, text='Noise Variance:').pack()
    noise_var_entry = Entry(mmse_window)
    noise_var_entry.pack()

    def apply_mmse_filter():
        window_size = int(window_size_entry.get())
        noise_variance = float(noise_var_entry.get())

        enhanced_image = mmse_filter(noisy_image.convert('L'), window_size, noise_variance)

        display_image(original_image, label_original)
        display_image(noisy_image, label_noisy)
        display_image(enhanced_image, label_mmse)

    tk.Button(mmse_window, text='Apply MMSE Filter', command=apply_mmse_filter).pack()

root = tk.Tk()
root.title('MMSE Filter')

# Labels for original, noisy, and MMSE filtered images
label_original = tk.Label(root)
label_noisy = tk.Label(root)
label_mmse = tk.Label(root)
label_original.pack(side='left')
label_noisy.pack(side='left')
label_mmse.pack(side='left')

# Button to upload image and apply MMSE filter
uploadButton = tk.Button(root, text='Upload Image', command=lambda: upload_image(label_original, label_noisy))
uploadButton.pack(pady=10)

# Button to apply MMSE filter
mmseButton = tk.Button(root, text='Apply MMSE Filter', command=apply_mmse, state='disabled')
mmseButton.pack(pady=10)

# Run the GUI
root.mainloop()
