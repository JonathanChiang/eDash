import numpy as np
import png
import pydicom
from pydicom.data import get_testdata_files

ds = pydicom.dcmread('0002.DCM')

shape = ds.pixel_array.shape
print(ds.pixel_array[0])
print(shape)

# Convert to float to avoid overflow or underflow losses.
image_2d = ds.pixel_array[0].astype(float)

# Rescaling grey scale between 0-255
image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

# Convert to ui
image_2d_scaled = np.uint8(image_2d)

# Write the PNG file
with open('test.png', 'wb') as png_file:
    w = png.Writer(shape[1], shape[2], greyscale=True)
    w.write(png_file, image_2d_scaled)
