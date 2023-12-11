from io import BytesIO

import cv2
import requests
import numpy as np

# URL of the image
image_url = "https://raw.githubusercontent.com/Mattl1565/maturaprojekt/90d165127120ceedcbd4e45c6251d14ab09572e5/Resources/Images/karim_busted.jpg"

# Download the image using requests
response = requests.get(image_url)
image_bytes = BytesIO(response.content)

# Read the image using cv2
img = cv2.imdecode(np.asarray(bytearray(image_bytes.read()), dtype=np.uint8), cv2.IMREAD_COLOR)

#show the image
cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()