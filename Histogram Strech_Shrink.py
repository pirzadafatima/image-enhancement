import tkinter as tk
from tkinter import Label, Button, filedialog
import numpy as np
from PIL import Image, ImageTk


def histogram_stretch(image, new_min, new_max):
    min_intensity = np.min(image)
    max_intensity = np.max(image)

    print(max_intensity)
    print(min_intensity)

    stretched_values = (image - min_intensity) / (max_intensity - min_intensity) * (new_max - new_min) + new_min
    stretched_image = np.clip(stretched_values, new_min, new_max).astype(np.uint8)

    return stretched_image


def histogram_compress(image, shrink_min, shrink_max):
    min_intensity = np.min(image)
    max_intensity = np.max(image)

    compressed_values = (shrink_max - shrink_min) / (max_intensity - min_intensity) * (
                image - min_intensity) + shrink_min
    compressed_image = np.clip(compressed_values, shrink_min, shrink_max).astype(np.uint8)

    return compressed_image


def uploadImage():
    global original_image
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path)
        displayImage(original_image)
        enhancedButton['state'] = 'normal'


def displayImage(img):
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk


def enhance_image():
    enhance_window = tk.Toplevel()
    enhance_window.title('Enhance Image GUI')

    Label(enhance_window, text='Select Enhancement Type:').pack(pady=10)

    def choose_stretching():
        enhance_window.destroy()

        img_array = np.array(original_image)
        enhanced_image = histogram_stretch(img_array, 0, 255)

        enhanced_img_tk = ImageTk.PhotoImage(Image.fromarray(enhanced_image))
        enhanced_label = Label(root, image=enhanced_img_tk)
        enhanced_label.image = enhanced_img_tk
        enhanced_label.pack(pady=10)

    def choose_compressing():
        enhance_window.destroy()

        img_array = np.array(original_image)
        enhanced_image = histogram_compress(img_array, 50, 200)

        enhanced_img_tk = ImageTk.PhotoImage(Image.fromarray(enhanced_image))
        enhanced_label = Label(root, image=enhanced_img_tk)
        enhanced_label.image = enhanced_img_tk
        enhanced_label.pack(pady=10)

    Button(enhance_window, text='Histogram Stretching', command=choose_stretching).pack(pady=5)
    Button(enhance_window, text='Histogram Compression', command=choose_compressing).pack(pady=5)


root = tk.Tk()
root.title('Histogram Stretching/Compression GUI')

# Buttons
uploadButton = tk.Button(root, text='Upload Image', command=uploadImage)
label = tk.Label(root)
enhancedButton = tk.Button(root, text='Enhance Image', command=enhance_image, state='disabled')
uploadButton.pack(pady=10)
label.pack()
enhancedButton.pack(pady=10)

original_image = None

root.mainloop()
