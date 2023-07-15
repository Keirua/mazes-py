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

# Create a mask for alpha pixels with alpha = 255
mask = (image[:, :, 3] == 255)

# Create a black image with the same size as the input image
output = np.zeros_like(image[:, :, :3])

# Set alpha pixels with alpha = 255 to white
output[mask] = (255, 255, 255)

result = cv2.bitwise_not(output)

# Resize the resulting image to 10% of the size of the initial image
result = cv2.resize(result, None, fx=0.2, fy=0.2)

# Display the result
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite(f"masks/{filename}", result)
