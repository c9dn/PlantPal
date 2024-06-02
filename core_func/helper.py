import cv2
import numpy as np
import os

from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw


def create_static_map(output_path, lat=37.7595, lon=-121.9358, zoom=15):
    # Create a StaticMap object
    print(os.getcwd())
    #url_template='http://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png'
    m = StaticMap(width=200, height=200)

    marker = CircleMarker((lon, lat), 'blue', 3)
    m.add_marker(marker)

    # Render the map
    image = m.render(zoom=zoom)
    print("HH")

    # Save the map to an image file
    image.save(output_path)
    print("HH")

def add_border_radius(input_path, output_path, border_radius=20, border_width=5, border_color=(0, 0, 0)):
    # Open the image
    image = Image.open(input_path).convert("RGBA")

    # Calculate size with border
    size_with_border = (image.width + 2 * border_width, image.height + 2 * border_width)

    # Create image with border
    image_with_border = Image.new("RGBA", size_with_border, border_color)
    image_with_border.paste(image, (border_width, border_width))

    # Create rounded mask
    mask = Image.new('L', size_with_border, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(border_width, border_width), (image_with_border.width - border_width, image_with_border.height - border_width)],
        radius=border_radius,
        fill=255
    )

    # Apply mask to image
    image_with_border.putalpha(mask)

    # Save the output image
    image_with_border.save(output_path, format="PNG")

def overlay_images(background_path, overlay_path, output_path, opacity=0.2):

    background_image = cv2.imread(background_path)
    overlay_image = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)    

    b_h, b_w, b_ch = background_image.shape
    o_h, o_w, o_ch = overlay_image.shape

    if 1:
        W = 800
        #oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)

        imgScale = W/b_w
        new_b_h,new_b_w = int(b_h*imgScale), int(b_w*imgScale)
        new_background = cv2.resize(background_image,(new_b_w, new_b_h))
        #cv2.imshow("Show by CV2",new_background)
        #cv2.waitKey(0)
        #cv2.imwrite("resizeimg_new_background.jpg",new_background)

    if 1:
        W = 350
        #oriimg = cv2.imread(filename,cv2.CV_LOAD_IMAGE_COLOR)

        imgScale = W/o_w
        new_o_h,new_o_w = int(o_h*imgScale), int(o_w*imgScale)
        new_overlay = cv2.resize(overlay_image,(new_o_w, new_o_h))
        new_overlay = new_overlay, 3
    
        #cv2.imshow("Show by CV2",new_overlay)
        #cv2.waitKey(0)
        #cv2.imwrite("resizeimg_new_overlay.jpg",new_overlay)
        
        
    if 1:
        square= np.zeros((new_b_h, new_b_w, b_ch), np.uint8)
        square.fill(255)
        x= new_b_w
        y= new_b_h
        print (new_b_h,new_b_w)
        print (new_o_h,new_o_w)
        offset =0
        broad = {int(y - new_o_h) - offset:int(y)- offset, int(x-new_o_w)- offset:int(x)- offset}
        print(broad)
        square[int(y - new_o_h) - offset:int(y)- offset, int(x-new_o_w)- offset:int(x)- offset] = new_overlay
        

    #if 0:
    #    cv2.imwrite("resizeimg.jpg",newimg)


    if 1: #OVERLAY
        OPACITY = 0.7
        added_image = cv2.addWeighted(new_background,0.6,square,0.4,0)
        #cv2.imshow('adjusted', added_image)  
        #cv2.waitKey()
        cv2.imwrite(out, added_image)
    


def is_plant(image_path):
    print(image_path)
    img = cv2.imread(image_path)

    # Convert image to HSV color space (better for color analysis)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define green color range in HSV (adjust values as needed)
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create a mask for green pixels
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Calculate percentage of green pixels
    green_pixels = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]
    green_ratio = green_pixels / total_pixels

    # If green ratio is high, consider it a plant (adjust threshold)
    if green_ratio > 0.3:
        return 1
    else:
        return 0