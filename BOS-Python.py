#MIT License
#Copyright (c) 2023 Adrian Winter

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import time

# Open the default camera (0) of your MacBook
#cap = cv2.VideoCapture(0)

#use external IP Cam 
yourIP = "192.168.178.53"

url = "http://"+yourIP+":8080/video"
cap = cv2.VideoCapture(url)
ALPHA = 0.4
GRIDSIZE = 1
THRESH = 22.0
THRESHWINDOWFILTER = 0
AUTOREFERENCEINTERVALL = 0.1
OVERLAY = 0.5

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# Flag to indicate if an image has been taken
image_taken = False

last_execution_time = 0

# Define a function to update the parameters
def update_params(lol):
    global ALPHA, GRIDSIZE, THRESH, THRESHWINDOWFILTER, AUTOREFERENCEINTERVALL, OVERLAY
    ALPHA = float(scale_alpha.get())
    GRIDSIZE = int(scale_gridsize.get())
    THRESH = float(scale_thresh.get())
    THRESHWINDOWFILTER = int(scale_threshwindowfilter.get())
    OVERLAY = float(scale_overlay.get())
    AUTOREFERENCEINTERVALL = float(scale_autoreferenceintervall.get())
    print(f"Updated parameters: ALPHA={ALPHA}, GRIDSIZE={GRIDSIZE}, THRESH={THRESH}, THRESHWINDOWFILTER={THRESHWINDOWFILTER}, AUTOREFERENCEINTERVALL={AUTOREFERENCEINTERVALL},OVERLAY={OVERLAY}")

# Create the parameter window
window = tk.Tk()
window.title("Parameters")

# Add a slider for ALPHA
label_alpha = ttk.Label(window, text="ALPHA")
label_alpha.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
scale_alpha = ttk.Scale(window, from_=0.0, to=2.0, orient=tk.HORIZONTAL, command=update_params)
scale_alpha.set(ALPHA)
scale_alpha.grid(row=0, column=1, padx=5, pady=5)

# Add a slider for GRIDSIZE
label_gridsize = ttk.Label(window, text="GRIDSIZE")
label_gridsize.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
scale_gridsize = ttk.Scale(window, from_=1, to=80, orient=tk.HORIZONTAL, command=update_params)
scale_gridsize.set(GRIDSIZE)
scale_gridsize.grid(row=1, column=1, padx=5, pady=5)

# Add a slider for THRESHWINDOWFILTER
label_threshwindowfilter = ttk.Label(window, text="THRESHWINDOWFILTER")
label_threshwindowfilter.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
scale_threshwindowfilter = ttk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=update_params)
scale_threshwindowfilter.set(THRESHWINDOWFILTER)
scale_threshwindowfilter.grid(row=2, column=1, padx=5, pady=5)

# Add a slider for THRESH
label_thresh = ttk.Label(window, text="THRESH")
label_thresh.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
scale_thresh = ttk.Scale(window, from_=0.0, to=70.0, orient=tk.HORIZONTAL, command=update_params)
scale_thresh.set(THRESH)
scale_thresh.grid(row=3, column=1, padx=5, pady=5)

# Add a slider for OVERLAY
label_overlay = ttk.Label(window, text="OVERLAY")
label_overlay.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
scale_overlay = ttk.Scale(window, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=update_params)
scale_overlay.set(OVERLAY)
scale_overlay.grid(row=4, column=1, padx=5, pady=5)

# Add a slider for AUTOREFERENCEINTERVALL
label_autoreferenceintervall = ttk.Label(window, text="AUTOREFERENCEINTERVALL")
label_autoreferenceintervall.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
scale_autoreferenceintervall = ttk.Scale(window, from_=0.1, to=10, orient=tk.HORIZONTAL, command=update_params)
scale_autoreferenceintervall.set(AUTOREFERENCEINTERVALL)
scale_autoreferenceintervall.grid(row=5, column=1, padx=5, pady=5)

autoReferenceImage = False
def toggle_switch():
    global autoReferenceImage 
    autoReferenceImage = switch_value.get()
    if switch_value.get():
        print("Switch is ON")
    else:
        print("Switch is OFF")

# AutoReferenceImage
switch_value = tk.BooleanVar(value=False)
switch = tk.Checkbutton(window, text="AutoReferenceImage", variable=switch_value, command=toggle_switch)
switch.grid(row=5, column=1, padx=5, pady=5)


# Loop through the video stream
while cap.isOpened():
   
    # Read the next frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if image_taken:
        # Compute the absolute difference between the grayscale frame and the taken image
        diff = cv2.absdiff(gray, image)

        # Define the grid size and threshold
        rows = GRIDSIZE
        cols = GRIDSIZE
        threshold = THRESHWINDOWFILTER

        # Get the image dimensions and grid cell size
        height, width  = diff.shape
        cell_width = width // cols
        cell_height = height // rows

        # Loop through each grid cell and check the average pixel intensity
        for r in range(rows):
            for c in range(cols):
                # Get the cell boundaries
                x1 = c * cell_width
                y1 = r * cell_height
                x2 = (c + 1) * cell_width
                y2 = (r + 1) * cell_height

               # Get the average pixel intensity in the cell
                cell = diff[y1:y2, x1:x2]
                avg_intensity = np.mean(cell)

                # If the average intensity is below the threshold, set all pixels in the cell to black
                if avg_intensity < threshold:
                    #diff[y1:y2, x1:x2] = 0
                    diff[y1:y2, x1:x2] = cv2.multiply(diff[y1:y2, x1:x2], np.array([1/(alpha+0.1)]))

        #increase contrast
        alpha = ALPHA
        diff = cv2.multiply(diff, np.array([alpha]))

        # Apply a threshold to the difference image to filter out small changes and amplify large changes
        _, diff = cv2.threshold(diff, THRESH, 255, cv2.THRESH_BINARY)

        #invert
        #img = cv2.bitwise_not(diff)

        # Create an empty redscale image with the same dimensions as the grayscale image
        height, width = diff.shape
        img_red = np.zeros((height, width, 3), dtype=np.uint8)

        # Set the red channel to the intensity of the grayscale image
        img_red[:, :, 2] = diff
       

        # Display the difference image
        overlay = cv2.addWeighted(img_red, 1 - OVERLAY, cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), OVERLAY, 0)
        cv2.imshow('Difference Image', overlay)
       
    else:
        # Display the current frame
        
        cv2.imshow('Current Frame', frame)

    # Wait for a key press to take an image
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Convert the current frame to grayscale and save it as the taken image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image_taken = True
        cv2.destroyWindow('Current Frame')
        print("Image taken")

    if autoReferenceImage:
        
        current_time = time.time()
        if current_time - last_execution_time >= AUTOREFERENCEINTERVALL:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print("Image taken")
            last_execution_time = current_time
     
    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #print("Processing next frame")

    # Start the parameter window
    #window.mainloop()
    window.update_idletasks()
    window.update()
    
# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
