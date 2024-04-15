import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

def uploadReferenceImage():
    global reference_image
    file_path = filedialog.askopenfilename(title="Select Reference Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        reference_image = cv2.imread(file_path)
        displayReferenceImage(reference_image)


def uploadTargetImage():
    global target_image
    file_path = filedialog.askopenfilename(title="Select Target Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        target_image = cv2.imread(file_path)
        displayTargetImage(target_image)


def displayReferenceImage(img):
    if img is not None:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        reference_label.config(image=img_tk)
        reference_label.image = img_tk

def displayTargetImage(img):
    if img is not None:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        target_label.config(image=img_tk)
        target_label.image = img_tk
        specifyButton['state'] = 'normal'

def calculate_histogram(img_gray):
    # Initialize histogram bins
    hist = [0] * 256

    # Calculate histogram
    for pixel_value in img_gray.flatten():
        hist[pixel_value] += 1

    return hist

def calculate_cumulative_sum(hist):
    # Initialize cumulative sum
    running_sum = [0] * 256

    # Calculate cumulative sum
    running_sum[0] = hist[0]
    for i in range(1, 256):
        running_sum[i] = running_sum[i - 1] + hist[i]

    return running_sum


def calculate_normalized_values(running_sum):
    max_sum = np.max(running_sum)
    normalized_vals = running_sum / max_sum
    return normalized_vals


def calculate_scaled_cdf(normalized_vals, max_gray_level):
    scaled_cdf = normalized_vals * max_gray_level
    return scaled_cdf


def equalizeHistogram(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    hist = calculate_histogram(img_gray)  # Compute histogram gives frequency value for each pixel
    running_sum = calculate_cumulative_sum(hist)  # Calculate cumulative sum

    # Normalize the cumulative sum by dividing with the total number of pixels
    normalized_vals = calculate_normalized_values(running_sum)

    # Scale the normalized cumulative sum by multiplying with max gray level value
    scaled_cdf = calculate_scaled_cdf(normalized_vals, np.max(img))

    # Round the scaled cumulative sum to the nearest integer
    rounded_vals = np.around(scaled_cdf).astype('uint8')

    return rounded_vals


def specifyHistogram():

    if reference_image is not None and target_image is not None:
        # Perform histogram equalization on reference and target images
        reference_mapping_table = equalizeHistogram(reference_image)
        target_mapping_table = equalizeHistogram(target_image)

        # Initialize an array to store the mapping from original histogram to desired histogram
        mapping_final = np.zeros(256, dtype=np.uint8)

        # Map each intensity value in the original histogram to the closest intensity value in the desired histogram
        for i in range(256):
            mapping_final[i] = np.argmin(np.abs(target_mapping_table - reference_mapping_table[i]))

        # Apply the mapping to the original image
        specified_histogram_image = mapping_final[reference_image]

        # Display the mapped reference image
        cv2.imshow("Mapped Reference Image", specified_histogram_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# GUI Initialization
root = tk.Tk()
root.title('Histogram Specification')

# Buttons and labels for reference image
referenceUB = tk.Button(root, text='Upload Reference Image', command=uploadReferenceImage)
reference_label = tk.Label(root)
referenceUB.pack(pady=10)
reference_label.pack()

# Buttons and labels for target image
targetUB = tk.Button(root, text='Upload Target Image', command=uploadTargetImage)
target_label = tk.Label(root)
targetUB.pack(pady=10)
target_label.pack()

# Specify button
specifyButton = tk.Button(root, text='Specify Histogram', command=specifyHistogram, state='disabled')
specifyButton.pack(pady=10)

# Variables to store the original images
reference_image = None
target_image = None

# Run the GUI
root.mainloop()
