# Image Enhancement Algorithms
This repository contains Python code for implementing various image enhancement algorithms using the Tkinter GUI library. 

It includes an implementation of the following: 

### Linear Mapping
Linear mapping is a simple image enhancement technique that stretches the pixel values of an image to a desired range. It is often used to improve the contrast and brightness of an image.

### Digital Negative
This is the equivalent of performing a logical NOT on the input image. This technique can be valuable for image enhancement because it takes advantage of the human visual system's complex response. It enhances details characterized by subtle brightness changes by shifting them from bright to dark regions and vice versa. As a result, small deviations in brightness become more discernible across the entire image.

### Histogram Stretch & Shrink
Histogram stretching expands the range of intensity values in an image to utilize the full dynamic range, thereby enhancing contrast and improving visual quality.  Histogram shrink reduces the dynamic range of intensity values in an image, often used to highlight specific intensity ranges and enhance visual features.

### ACE Filter
The Adaptive Contrast Enhancement (ACE) filter is a method for enhancing image contrast by adaptively adjusting pixel intensities based on local image characteristics, resulting in improved visibility of details.

### Histogram Specification
Histogram specification is a technique used to manipulate the intensity distribution of an image to match a desired histogram, enabling control over the image's contrast, brightness, and overall appearance.

### Minimum Mean Square Error (MMSE) Enhancement
The MMSE method is a statistical approach to image enhancement that estimates pixel values by minimizing the mean square error between the enhanced image and the ideal image. It reduces noise while preserving important image details, making it effective for improving image quality in low-light or noisy conditions.

### Pseudo-Median Filter
The Pseudo-Median Filter is a non-linear filter that enhances image quality by reducing noise while preserving edges. Unlike a standard median filter, it approximates the true median using a computationally simpler method, resulting in faster processing while maintaining effective noise suppression.

### Dependencies
- Python 3.x
- Tkinter
- NumPy
- Pillow (PIL)
