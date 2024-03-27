import os
import subprocess
import ffmpeg


def rename_files_for_ffmpeg(input_folder, temp_prefix="temp_"):
    original_filenames = []
    temp_filenames = []
    for i, filename in enumerate(sorted(os.listdir(input_folder)), start=1):
        if filename.endswith(".png"):
            original_filenames.append(filename)
            temp_filename = f"{temp_prefix}{i:03d}.png"
            temp_filenames.append(temp_filename)
            os.rename(os.path.join(input_folder, filename), os.path.join(input_folder, temp_filename))
    return original_filenames, temp_filenames

def revert_filenames(input_folder, original_filenames, temp_filenames):
    for original, temp in zip(original_filenames, temp_filenames):
        os.rename(os.path.join(input_folder, temp), os.path.join(input_folder, original))


def convert_images_to_video(directory_path, framerate=10):
    """
    Convert sets of images in each subdirectory of directory_path into MP4 videos.
    Each subdirectory represents a different angle.
    
    Args:
    - directory_path: Path to the main directory containing angle subdirectories.
    - output_fps: Frames per second for the output videos.
    """

    for subdir, dirs, files in os.walk(directory_path):
        if not files:
            print('fail')
            continue  # Skip if the directory is empty

        original_filenames, temp_filenames = rename_files_for_ffmpeg(subdir, "temp_")
        
        input_pattern = os.path.join(subdir, 'temp_%03d.png')  # Adjust based on your actual filename pattern
       
        output_video_path = os.path.join(subdir, "output.mp4")
        print(f"Converting images in {subdir} to video...")
        (
        ffmpeg
            .input(input_pattern, framerate=framerate, pattern_type='sequence')
            .output(output_video_path, crf=25, pix_fmt='yuv420p', r=30)
            .run(overwrite_output=True)
        )
        print(f"Video saved to {output_video_path}")

directory_path = './angles'
convert_images_to_video(directory_path)
