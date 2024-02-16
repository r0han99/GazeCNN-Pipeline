import streamlit as st



# system level requirements 
import os 
import sys
import shutil 
import random
import time
import subprocess
import glob
import json
import fnmatch

# data handlers
import pandas as pd 
from tensorflow.keras.models import load_model
import os
import cv2
import numpy as np
import tensorflow as tf


# From src
from src.ffmpeg_construct import construct
from src.estimate_frame import estimation
from src.copy_interest_period import interest_area
from src.cropper import crop_images





# global paths

TRIALS = './trials'


def count_samples(items):


    global TRIALS
    sample_size_for_video = {}
    for_display = {}
    for_validation = {}
    

    for item in items:
        path_to_csv = os.path.join(TRIALS, item, "gaze.csv")
        
        mp4_files = glob.glob(os.path.join(TRIALS, item, '*.mp4'))
        video_name = mp4_files[0].split("/")[-1::][0]
        
        path_to_video =  mp4_files[0]


        # path_to_video = os.path.join(TRIALS, items, "*.mp4")
        if os.path.exists(path_to_csv):
            
            st.markdown(f"- Processing `{item}`, Reading Sample Count!")
            
            sample_size = pd.read_csv(path_to_csv).shape[0]
            sample_size_for_video[path_to_video] = sample_size
            for_display[video_name] = sample_size
            for_validation[item] = sample_size


    st.markdown("")
    st.markdown("**Video Name - Sample Size**")
    st.write(for_display)


    return sample_size_for_video, for_validation

def preprocess_image(image):
    # Resize, normalize, or apply any necessary preprocessing steps
    # Replace this with your actual preprocessing steps
    image_width, image_height = 256, 256  # Update with your image dimensions
    processed_image = cv2.resize(image, (image_width, image_height))
    processed_image = processed_image / 255.0  # Normalize pixel values between 0 and 1
    return processed_image


def check_template_matches(files_and_values):

    items_to_match = ["gaze.csv", "*.mp4", "config.json"]

    
    for template in items_to_match:
      
        matches = fnmatch.filter(files_and_values, template)
        if not matches:
            return False
    
    return True


@st.cache_resource
def load_model_engine():
    try:
        model = load_model("./model-engine/MobileNetV2_gzcnn.keras", compile=False)
    except:
         model = load_model("./model-engine/MobileNetV2_gzcnn.h5", compile=False)
    
    return model


def rm_macos_binaries(item_list):

    try: 
        item_list.remove(".DS_Store")
        return item_list

    except:
        
        return item_list
    
def convert_minute_to_seconds(time):
    # Function to convert a single minute value to seconds
    def to_seconds(minutes):
        return minutes * 60

    if len(str(time)) == 3:
        s_minutes = int(str(time)[0])
        #st.write(s_minutes)
        s_seconds = int(str(time)[1:])
        #st.write(s_seconds)

    elif len(str(time)) == 4:
        s_minutes = int(str(time)[:2])
        #st.write(s_minutes)
        s_seconds = int(str(time)[2:])
        #st.write(s_seconds) 

    time_seconds = to_seconds(s_minutes)+s_seconds
    
    return time_seconds

    

def extract_number(filename):
    return int(filename.split('_')[1].split('.')[0])


def rm_flag_file(item_list):
    try: 
        item_list.remove(".flag_file")
        return item_list

    except:
        
        return item_list



def validate_requirements():

    # acccess global 
    global TRIALS

        
    if os.path.exists(TRIALS):

        items = os.listdir(TRIALS)
        items = rm_macos_binaries(items)
        
        st.markdown("#### Checking if the directories have `Gaze.csv` and `Trial.mp4`")
        st.divider()

        valid_list = []
        invalid_list = []
        for candidate in items:

            # this will normally be directories of individual participants
            st.markdown(f"##### {candidate}")
            count = len(rm_macos_binaries(os.listdir(os.path.join(TRIALS, candidate))))
            listing = rm_macos_binaries(os.listdir(os.path.join(TRIALS, candidate)))
            for subitem in listing:
                st.markdown(f"- {subitem}")

            if check_template_matches(listing):
                st.success(f"{candidate} requirements satisfied!")
                valid_list.append(candidate)

            else:
                st.error(f"{candidate} some requirements are missing!")
                invalid_list.append(candidate)
        
            st.divider()

        st.markdown("### Post Validation Report")
        st.markdown("**Valid Participants**")
        st.code(valid_list)
        st.markdown("**In Valid Participants Paths with Missing Items**")
        st.code(invalid_list)

        if len(valid_list) >= len(invalid_list):
            return True, valid_list
        else:
            return False, invalid_list
                
            
    
    else:
        st.error("Trials Path Missing")


    


def main_cs():
    
    st.divider()

    cols = st.columns([5,8])
        
    cols[0].subheader("Click Here to Start Processing →")
    

    slot_1 = cols[1].empty()
    slot_2 = cols[1].empty()

    if slot_1.button("Begin Processing Trial Videos", use_container_width=True):
        st.subheader("",divider="blue")

        slot_1.code("Intiated Processing, disabled re-run until process is elapsed.")
        slot_2.code("You can override this by pressing `R`")

        # Heading
        st.title("Phase-1 Validation of Requirements")

        with st.status("Validation", expanded=True) as STATUS:
            
            

            status, items = validate_requirements()

            if status:

                STATUS.update(label="Validation complete!", state="complete", expanded=not status)
                
            else:
                
                STATUS.update(label="Validation Failed! Lot of Incompletly formated trials", state="error", expanded=not status)


        if status:
            st.markdown("#### Processing the following")
            st.code(items)

        else:
            st.markdown("#### Fix the following")
            st.code(items)


        st.divider()
                
    
    
        st.title("Phase-2 `ffmpeg` Command Construction! & Execution")
        with st.status("Video Decomposition", expanded=True) as status:
            

            st.markdown("#### Making Folders for Images!")
            # create subfolders 
            global TRIALS 

            source_folder_paths = []
            for item in items:
                source_folder_path = os.path.join(TRIALS, item, f'{item}_source')
                st.markdown(f"- Creating folders at `{source_folder_path}`")
                
                os.makedirs(source_folder_path, exist_ok=True)
                source_folder_paths.append(source_folder_path)
                
                
            st.markdown("#### Reading Sample Sizes from `gaze.csv`")
            

            # count_samples for all the valid items 
            sample_size_for_video, for_validation = count_samples(items)

            st.markdown("#### Constructing `ffmpeg` command to decompose video to individual frames.")

            command_dict = {}
            for (file, frames), dest_path, participant_id in zip(sample_size_for_video.items(), source_folder_paths, items):

                command = construct(file, frames, dest_path)
                st.subheader(participant_id)
                st.code(command)

                # command_dict filling
                command_dict[participant_id] = command

            status.update(label="Command Construction completed!", state="complete", expanded=False)



        ffmpeg_commands = []
        for command in command_dict.values():
            cmd_parts_list = []
            # Split the command into a list of strings by spaces
            command_parts = command.split()
            # Append the list of strings to ffmpeg_commands
            ffmpeg_commands.append(command_parts)


        # Create a Streamlit app
        st.markdown("### Ffmpeg Command Execution!")

        

        # Run the ffmpeg command and capture the output
        for ffmpeg_command, item in zip(ffmpeg_commands, items):
            

            num_of_frames_for_validation = len(rm_macos_binaries(os.listdir(os.path.join(TRIALS, item, f"{item}_source"))))

            if num_of_frames_for_validation == for_validation[item]:

                st.info(f"Decomposed Images Already Exists For {item}")
                
            else:

                with st.status(f"Running Process for {item}", expanded=False) as STATUS:
                    
                    process = subprocess.Popen(
                        ffmpeg_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,  # Merge stdout and stderr
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        stdin=subprocess.DEVNULL  # Redirect stdin to /dev/null
                    )

                    for line in process.stdout:
                        # Display the ffmpeg output line by line
                        st.text(line.strip())

                    process.wait()  # Wait for the subprocess to finish

                    if process.returncode == 0:
                        
                        STATUS.update(label=f"{item} - Decomposition Successful!", state="complete", expanded=False)
                        
                    else:
                        st.error(f"FFmpeg command failed with return code {process.returncode}")
                        STATUS.update(label=f"{item} - Failed Please Recheck Files!", state="error", expanded=False)
                    
        
        st.divider()
        st.title("Phase-3 Estimate Start-End Frames `&` Attention to Interest Period")
        

        doesnt_exist_count = 0
        exist_count = 0

        with st.status("Validation") as STATUS:

            st.markdown("#### Number of frames decomposed per each candidate")
            st.write(sample_size_for_video)
            st.divider()

            proceed = False
            if os.path.exists("./config.csv"):
                proceed=True

            # for candidate in items:
            #     candidate_path = os.path.join(TRIALS, candidate)
            #     candidate_items = rm_macos_binaries(os.listdir(candidate_path))
            #     st.markdown(f"#### {candidate}")
            #     # st.code(candidate_items)
            #     items_to_match = ["gaze.csv","*.mp4","config.json"]

            #     matched_items = []
            #     for pattern in items_to_match:
            #         for item in candidate_items:
            #             if fnmatch.fnmatch(item, pattern):
            #                 matched_items.append(item)


            
                # if "config.json" in matched_items:
                #     st.success("Config files exist!")
                #     with open(os.path.join(candidate_path, "config.json"), 'r') as f:
                #         st.write(f.readlines())
                #     exist_count += 1
                #     proceed = True
            else:
                st.error("Config doesn't exist!")
                doesnt_exist_count +=1 


        st.divider()

        if proceed:
            
            candidate_interest_period_json = {}

            data = pd.read_csv("config.csv")
            for candidate in items:
                candidate_path = os.path.join(TRIALS, candidate)
                # candidate_items = rm_macos_binaries(os.listdir(candidate_path))

                s = data.set_index("candidate").loc[candidate, 'start']
                e = data.set_index("candidate").loc[candidate, 'end']

                #st.success(s)
                #st.success(e)
                
                start_sec = convert_minute_to_seconds(s)
                end_sec = convert_minute_to_seconds(e)
                #st.write(start_sec, end_sec)

    
                # candidate_config = os.path.join(candidate_path, "config.json")
                
                # with open(candidate_config, 'r') as f:
                #     each_candidate_config = json.load(f)

                # start_sec = each_candidate_config['start']
                # end_sec = each_candidate_config['end']

        
                #st.markdown(f"- Estimating Interest area ( Start Frame to End Frame ) for `{candidate}`")
                start_frame, end_frame = estimation(start_sec, end_sec)
                
            
                # COPY interest Area to other folder. 
                interest_area(start_frame, end_frame, candidate, candidate_path)

        
    
            st.title("Phase-4 `50%` Cropping")
            
            for candidate in items:

                candidate_path = os.path.join(TRIALS, candidate)
                gaze_csv = pd.read_csv(os.path.join(candidate_path, "gaze.csv"))
                source_images = os.path.join(candidate_path, f"{candidate}_interest_period")


                candidate_config = os.path.join(candidate_path, "config.json")
                
                with open(candidate_config, 'r') as f:
                    each_candidate_config = json.load(f)

                start_sec = each_candidate_config['start']
                end_sec = each_candidate_config['end']
                start_frame, end_frame = estimation(start_sec, end_sec)


                try:
                    with open(os.path.join(source_images, ".flag_file"), 'r') as f:
                        content = f.readline()
                
                    if content == "cropped":
                        st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> <span style='color:green;'>already cropped!</span></span>", unsafe_allow_html=True)
                
                except FileNotFoundError:

                    # st.success("in except")
                    image_files = rm_macos_binaries(rm_flag_file(os.listdir(source_images)))
                    # st.success(len(image_files))

                    sorted_img_files  = sorted(image_files, key=extract_number)
                    # st.success(len(sorted_img_files))
                    interest_gaze = gaze_csv.iloc[start_frame:end_frame+1, :]
                    # st.write(interest_gaze.shape)
                    interest_gaze['frames'] = sorted_img_files
                    # st.write(sorted_img_files)
                    # st.DataFrame(interest_gaze)

                    interest_gaze = interest_gaze[['gaze x [px]','gaze y [px]', 'frames']]

                    crop_images(candidate, source_images, interest_gaze)


       
            st.divider()

            st.title("Phase-5 MobileNetV2 Model Engine: Classification!")
            
            with st.status("Loading Model", expanded=False):

                model_engine = load_model_engine()
                model_engine.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'], )
                train_input_shape = (256, 256,3)
                
                class_index = ['NA', 'Notation', 'SpaceBarScreen', 'Keyboard']
                st.markdown("`MobileNetV2_gzcnn` model-engine loaded.")



            for candidate in items:
                candidate_path = os.path.join(TRIALS, candidate)
                directory = os.path.join(candidate_path,f"{candidate}_interest_period" )
                

                # results dir
                candidate_data_table_dir = os.path.join(candidate_path, f"{candidate}_behvioral_datatable")
                os.makedirs(candidate_data_table_dir,exist_ok=True )


                CLASSIFICATION_DICTIONARY = {}
                st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> <span style='color:orangered; font-weight:bold; font-size:20px;'>- Classifying Frames</span></span>", unsafe_allow_html=True)
                
                try:
                    with open(os.path.join(candidate_data_table_dir, ".flag_file"), 'r') as f:
                        content = f.readline()

                    if content == "classified":
                        st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> <span style='color:green;'>already classfied! check datatable folders within the participant folder.</span></span>", unsafe_allow_html=True)
                
                except FileNotFoundError:
                    # Initialize progress bar
                    progress_bar = st.progress(0)

                    # Iterate through all files in the directory
                    for index, filename in enumerate(os.listdir(directory)):
                        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust extensions as needed
                            image_path = os.path.join(directory, filename)
                            
                            # Read the image
                            image = cv2.imread(image_path)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB if necessary
                            
                            # Preprocess the image
                            processed_image = preprocess_image(image)
                            
                            # Ensure image shape matches the model_engine's input shape
                            if processed_image.shape == train_input_shape:
                                # Make prediction
                                predictions = model_engine.predict(np.array([processed_image]))
                                
                                # Process predictions (use as needed)
                                # For example, print predicted classes or save results
                                # Find the index of the maximum probability
                                max_prob_index = np.argmax(predictions)

                                # Create a new array with all zeros and set the maximum probability index to 1
                                binary_prediction = np.zeros_like(predictions)
                                binary_prediction[0, max_prob_index] = 1
                                #st.code(f"Image: {filename}, Predictions: {binary_prediction}")
                                CLASSIFICATION_DICTIONARY[filename] = binary_prediction
                            else:
                                st.error(f"Image: {filename} has incorrect dimensions and was skipped.")
            
                            # Update progress bar
                            progress_bar.progress((index + 1) / len(os.listdir(directory)))


            
                    with st.status(f"Packaging {candidate} Behavioural DataTable"):
                            test = pd.DataFrame(pd.Series(CLASSIFICATION_DICTIONARY))
                            test[0] = test[0].apply(lambda x:x[0])
                            test.columns = ['predictions']
                            st.markdown("- Creating Raw DataFrame.")
                            
                            exp_df = pd.DataFrame(test["predictions"].to_list(), columns=class_index)
                            exp_df = exp_df.astype(int)
                            st.markdown("- Managing Data Types.")

                            test = test.reset_index()
                            test.columns = ['frames','_']
                            exp_df['frames'] = test['frames']
                            
                            exp_df = exp_df.sort_values(by='frames').reset_index(drop=True)
                            exp_df = exp_df[['frames'] + class_index]
                            st.markdown("- Organising Data Table.")

                            st.success(f"Saving the data to {candidate_data_table_dir}/{candidate}_datatable.csv")
                            exp_df.to_csv(os.path.join(candidate_data_table_dir, f"{candidate}_datatable.csv"))

                            with open(os.path.join(candidate_data_table_dir, ".flag_file"), 'w') as f:
                                f.write("classfied")

            
            st.divider()

            st.title("Process Completed! Check Datafolders.")

            st.divider()
            st.title(":red[Commencing Delete Protocol]")

            

            

            
            




            



     
                

    

                    

if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="GazeCNN Software")
    st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)
    main_cs()

    for _ in range(10):
        st.sidebar.markdown("")
    cols = st.sidebar.columns([3,1,3])
    cols[0].image("./assets/brain.png", width=100)
    cols[1].markdown("")

    cols[1].markdown('''<center><span style="font-size:30px; font-family:'poppins'; color:black; font-weight:bold;"><a href="https://www.colorado.edu/lab/del/" style="color: black; text-decoration: none;"><u>Dellab</u></a></span></center>''',unsafe_allow_html=True)
    cols[1].markdown('''<center><span style="font-size:25px; font-family:'poppins'; color:black;">Software</span></center>''',unsafe_allow_html=True)