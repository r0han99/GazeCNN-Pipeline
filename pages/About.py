import streamlit as st 

from src.dellab import add_logo


st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)
st.divider()
st.subheader("Conceptualised Pipeline", divider="orange")
st.image("pipeline-architecture.png")


add_logo()

st.divider()


readme = '''

### Classification Pipeline Documentation
# Overview
This document outlines the classification pipeline used for processing and analyzing video data. The pipeline is designed to decompose video files into frames, select a period of interest, crop relevant sections, and classify them using a convolutional neural network (CNN) model.

Pipeline Steps
1. Configuration and Input
config_json: This file contains all the necessary configurations required for the pipeline to run.
Trial Video: The raw video file that will be processed.
gaze.csv: A CSV file containing gaze coordinates which are relevant for cropping the images.
2. Sample Count
Count_Samples.py: This script counts the number of samples (frames) in the video file.
Outputs an estimated number of frames (Ex: 200,000).
3. Frame Extraction
ffmpeg-command-construct.py: Constructs the ffmpeg command for extracting frames from the video.
Uses trial_video_file_path, start time, and end time in seconds from the config_json.
Execute-command: Runs the ffmpeg command to extract frames.
Outputs to the source folder with all decomposed images.
4. Period of Interest
estimate_frame.py: Estimates the frame number for the start and end of the experiment period.
Takes input from config_json for start time and end time in seconds.
Copy-interest-period.py: Copies the frames of interest based on the estimated start and end frame numbers from the previous step.
5. Image Cropping
Cropper.py: Crops the images based on gaze coordinates.
Utilizes gaze.csv for gaze coordinates.
Outputs cropped images ready for classification.
6. Classification
CNN Model: MobileNetV2: The selected CNN model for classifying the cropped images.
The model processes the images and outputs classification results.
7. Data Collation
Trial Data: The final output is a structured set of data or results from the classification model, which can be used for further analysis.
Data Flow
The pipeline follows a linear data flow where the output of each step serves as the input for the next. This design allows for modularity and ease of debugging.

Requirements
Python 3.x
FFmpeg for frame extraction
Libraries: OpenCV for image processing, TensorFlow or a similar library that can run MobileNetV2.
Setup
To set up the pipeline, ensure all the dependencies are installed and the config_json is correctly set up with the paths to the trial video and gaze.csv file, as well as other necessary parameters.

Usage
To execute the pipeline, run the scripts in the order specified above, ensuring that each script's output is correctly directed to the next script's input.





'''

st.markdown(readme)


