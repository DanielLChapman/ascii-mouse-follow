import cv2
import numpy as np
import os

def reverse_video(video_path, output_filename):
    cap = cv2.VideoCapture(video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    
    frames = []
    # Read and store all frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    
    # Write original frames
    for frame in frames:
        out.write(frame)
    
    # Write reversed frames
    for frame in reversed(frames):
        out.write(frame)
    
    out.release()
    print(f"Loop video saved to {output_filename}")

def process_directory(directory_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for filename in os.listdir(directory_path):
        if filename.endswith(".mp4"):
            video_path = os.path.join(directory_path, filename)
            output_filename = os.path.join(output_path, filename)
            reverse_video(video_path, output_filename)
    

directory_path = './trimmed'
output_path = './trimmed-reverse'

process_directory(directory_path, output_path)