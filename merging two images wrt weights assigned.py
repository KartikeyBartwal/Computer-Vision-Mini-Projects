import cv2

def resize_images_inplace(img1, img2):
    # Check if both images are not None
    if img1 is not None and img2 is not None:
        # Get the dimensions of both images
        height1, width1, _ = img1.shape
        height2, width2, _ = img2.shape

        # Determine the smaller dimensions
        min_height = min(height1, height2)
        min_width = min(width1, width2)

        # Resize both images to the smaller dimensions
        img1 = cv2.resize(img1, (min_width, min_height))
        img2 = cv2.resize(img2, (min_width, min_height))

        return img1, img2
    else:
        print("Error: One or both of the images are None.")
        return None, None



# Load the images
img1 = cv2.imread("C:\\Users\\hp\\OneDrive\\Desktop\\before.png")
img2 = cv2.imread("C:\\Users\\hp\\OneDrive\\Desktop\\after.png")

# Resize the images in place
img1, img2 = resize_images_inplace(img1, img2)


add = img1 + img2 
cv2.imshow("add" , add)

weights = cv2.addWeighted(img1 , 0.5, img2, 0.5 , 0)

cv2.imshow("weights" , weights)
cv2.waitKey(0)
cv2.destroyAllWindows()