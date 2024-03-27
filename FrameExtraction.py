import cv2
import os

# Define the video file path and the output directory
video_path = 'IMG_5120.mov'
output_dir = './third_pass/'
output_dir_gray = './third_pass_gray/'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(output_dir_gray):
    os.makedirs(output_dir_gray)

# Load the video
cap = cv2.VideoCapture(video_path)

# Initialize a variable to keep track of the frame count
frame_count = 0

# Loop through each frame in the video
while True:
    # Read the next frame
    ret, frame = cap.read()
    
    # Check if the frame was read correctly
    if not ret:
        break  # Exit the loop if there are no frames left to read

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_colored = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    # Construct the output file path
    output_filepath = os.path.join(output_dir, f'frame_{frame_count}.png')
    output_filepath_gray = os.path.join(output_dir_gray, f'frame_{frame_count}.png')
    
    # Save the frame as a JPEG file
    cv2.imwrite(output_filepath_gray, gray_frame_colored)
    cv2.imwrite(output_filepath, frame)
    
    # Increment the frame count
    frame_count += 1

# Release the video capture object
cap.release()

print(f'Frames extracted: {frame_count}')
