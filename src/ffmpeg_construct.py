import argparse
import os



def construct(file, frames, dest_path):

    return f'''ffmpeg -i {file} -vf fps=200 -q:v 2 -start_number 0 -vsync 0 -frames:v {frames} {dest_path}/frames_%04d.jpg'''


def check_existence(file):
    if os.path.exists(file):

        return True
    else:
        return False


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process a video file with a specified number of frames.")
    parser.add_argument("--file", required=True, help="Input video file (e.g., file.mp4)")
    parser.add_argument("--frames", type=int, required=True, help="Number of frames to process")

    args = parser.parse_args()

    # file name and frames from arguments
    filename = args.file
    frames = args.frames

    if check_existence(filename):

        ffmpeg_config = construct(filename, frames)

    else:

        print(" x Video File Not Found! Check Path.")
        exit()
    
    print()
    print("- "+ffmpeg_config)
    print()

    print('Use the Above command to decompose to Images.')
