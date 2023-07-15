import sys

import cv2
import numpy as np

# Check if a command line parameter is provided
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    raise RuntimeError("No command line parameter provided.")

# Read the transparent PNG image
image = cv2.imread(f"pokemon/{filename}", cv2.IMREAD_UNCHANGED)

# Extract the alpha channel from the image
alpha_channel = image[:, :, 3]

# Threshold the alpha channel to create a binary mask
_, binary_mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

# Find contours in the binary mask
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour by area
largest_contour = max(contours, key=cv2.contourArea)

# Create a black and white image with the same size as the input image
result = np.zeros_like(image[:, :, :3])

# Draw the largest contour as white on the black and white image
cv2.drawContours(result, [largest_contour], 0, (255, 255, 255), thickness=cv2.FILLED)
result = cv2.bitwise_not(result)

# Resize the resulting image to 10% of the size of the initial image
result = cv2.resize(result, None, fx=0.1, fy=0.1)

# Display the result
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite(f"masks/{filename}", result)
