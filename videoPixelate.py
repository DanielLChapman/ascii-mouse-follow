import cv2
import numpy as np

def pixelate(frame, block_size=8):
    (height, width) = frame.shape[:2]
    # Calculate the number of blocks along the width and height
    x_blocks = max(1, width // block_size)
    y_blocks = max(1, height // block_size)
    
    # Calculate block size, could be adjusted if you need more precise control
    block_width = width // x_blocks
    block_height = height // y_blocks

    # Ensure the last block's size adds up to the full width/height
    for y in range(0, y_blocks):
        for x in range(0, x_blocks):
            # Compute the region of interest
            start_x = x * block_width
            start_y = y * block_height
            end_x = start_x + block_width
            end_y = start_y + block_height

            # Adjust for the last block possibly being smaller than the others
            if x == x_blocks - 1:  # Last column
                end_x = width
            if y == y_blocks - 1:  # Last row
                end_y = height

            roi = frame[start_y:end_y, start_x:end_x]
            avg_color = np.mean(roi, axis=(0, 1), dtype=int)
            frame[start_y:end_y, start_x:end_x] = avg_color
    
    return frame

video_path = 'video_in.mp4'  # Change to your video path
cap = cv2.VideoCapture(video_path)

# Video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'MP4V')

# Output video
out = cv2.VideoWriter('pixelated_video.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = pixelate(frame, block_size=16)  # Adjust block_size if necessary
    
    out.write(result)

cap.release()
out.release()
