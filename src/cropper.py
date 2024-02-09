import argparse
import pandas as pd 
import numpy as np
import cv2
import os
import streamlit as st 

# SOURCE_IMGS = './source/'
def crop_images(candidate, SOURCE_IMGS, gaze_csv):
    input_directory = SOURCE_IMGS


    # Create the output directory if it doesn't exist
    os.makedirs(input_directory, exist_ok=True)

    # Iterate through the dataframe
    st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> cropping frames..</span>", unsafe_allow_html=True)
    
    slot = st.empty()
    progress_bar = st.progress(0) 
    total_images = len(gaze_csv)
    for index, row in gaze_csv.iterrows():
        gaze_x = row['gaze x [px]']
        gaze_y = row['gaze y [px]']
        frame_filename = row['frames']

        # Load the frame image
        frame_path = os.path.join(input_directory, frame_filename)
        frame = cv2.imread(frame_path)

        # Calculate the crop coordinates
        height, width, _ = frame.shape
        x_start = max(0, int(gaze_x - (width / 4)))
        x_end = min(width, int(gaze_x + (width / 4)))
        y_start = max(0, int(gaze_y - (height / 4)))
        y_end = min(height, int(gaze_y + (height / 4)))

        # Crop the image in-place
        frame = frame[y_start:y_end, x_start:x_end]

        # Save the modified image to overwrite the original
        cv2.imwrite(frame_path, frame)

        progress_percent = (index + 1) / total_images
        slot.markdown(f"Cropping `{frame_path}`")
        progress_bar.progress(min(progress_percent, 1.0))

        print(f" Cropped image overwritten: {frame_path}")


    with open(os.path.join(input_directory, ".flag_file"), 'w') as f:
        f.write("cropped")

    st.success(f"{candidate} Cropped and Replaced!")
    st.divider()



def extract_number(filename):
    return int(filename.split('_')[1].split('.')[0])

    

def validate(csv_file):

    global SOURCE_IMGS

    if os.path.exists(csv_file):
        
        print('file exists.')

        data = pd.read_csv(f'{csv_file}')

        num_of_samples = data.shape[0]

        # image files 
        image_files = os.listdir(SOURCE_IMGS)

        if os.listdir(SOURCE_IMGS) == num_of_samples:
            
            gaze_csv =  pd.read_csv(csv_file)

            # Image sorting 
            sorted_img_files  = sorted(image_files, key=extract_number)

            # Aligning 
            gaze_csv['frames'] = sorted_img_files
            gaze_csv =  gaze_csv[['gaze x [px]','gaze y [px]', 'frames']]
            crop_images(gaze_csv)


        else:

            print('Sample Size mismatch!')
            print(f'Number of Decomposed Images: {os.listdir(SOURCE_IMGS)}')
            print(f'Number of Gaze Records in the csv: {num_of_samples}')



    else:

        print('File Does not exists!, Check the file path')



        



def main():
    
    parser = argparse.ArgumentParser(description="Cropper Pipeline")
    parser.add_argument("--csv", required=True, help="Path to the CSV file")

    args = parser.parse_args()

    csv_file = args.csv


    # Prompt the user for Yes/No input
    source_folder = input("Does the source folder contain all the decomposed images of the trial? (Yes/No): ").strip().lower()

    # Check the user's input
    if source_folder == 'yes':
        # Provide the path to the CSV file and source folder
        # Your code to process the CSV file can go here
        print(f"Processing CSV file: {csv_file}")
        validate(csv_file)
    elif source_folder == 'no':
        print("Please make sure all decomposed images are in the source folder before processing the CSV file.")
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")

        

    

    





if __name__ == "__main__":


    main()

   
    print()
    print('--'*25)
    print('Job Completed..')