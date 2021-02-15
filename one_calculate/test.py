import concom
import cv2
import os

DATA_DIR = './data'
path = os.path.join(DATA_DIR)

# this is only for this example
new_image = cv2.imread(os.path.join(path, '0.png'))
image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
result = []
result = concom.make_predict(image)
print (result)