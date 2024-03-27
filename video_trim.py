import cv2
import numpy as np

def is_similar(image1, image2, threshold=0.98):
    """Compare two images for similarity."""
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    similarity = cv2.matchTemplate(image1_gray, image2_gray, cv2.TM_CCOEFF_NORMED)
    return np.max(similarity) >= threshold

def find_loop_and_process(video_path, similarity_threshold=0.98, min_frame_gap=90):
    """Find a loop in the video with a minimum gap, or reverse the video."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    
    frames = []
    loop_found = False

    # Read and store all frames for comparison and potential reversal
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    # Compare frames for loop with a minimum gap
    for i in range(len(frames) - min_frame_gap):
        for j in range(i + min_frame_gap, len(frames)):
            if is_similar(frames[i], frames[j], similarity_threshold):
                print(f"Loop found between frames {i} and {j}")
                loop_found = True
                # Here, you could trim the video to [i:j] using another function or FFmpeg command
                return  # Exit after finding the loop

    if not loop_found:
        print("No loop found, reversing the video")
        reverse_video(video_path, 'reversed_video.mp4')

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

# Example usage
video_path = './angles/0/output.mp4'
find_loop_and_process(video_path)
