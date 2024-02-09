import streamlit as st



# system level requirements 
import os 
import sys
import shutil 
import random
import time
import subprocess
import glob
import fnmatch
import json

# data handlers
import pandas as pd 


path = './trials/'


def rm_macos_binaries(item_list):

    try: 
        item_list.remove(".DS_Store")
        return item_list

    except:
        
        return item_list


def watch_videos_create_configs(INITIATE_FLAG):

    global path

    candidates = rm_macos_binaries(os.listdir(path))
    st.divider()
    if INITIATE_FLAG:
        st.markdown("#### Recording Interest Period Time Stamps")
        
        for candidate in candidates:
            candidate_path = os.path.join(path, candidate)
            candidate_items = rm_macos_binaries(os.listdir(candidate_path))
            video_pattern = "*.mp4"
            
            
            for item in candidate_items:
                if fnmatch.fnmatch(item, video_pattern):
                    st.markdown(f"#### {candidate} Trial Video")
                    video_path = os.path.join(path, candidate, item)
                    st.video(video_path)
                    st.divider()

        # Dictionary to store start and end pairs for each candidate
        candidate_start_end_pairs = {}

        with st.form("Form"):
            for candidate in candidates:
                st.markdown(f"#### {candidate}")
                candidate_path = os.path.join(path, candidate)
                candidate_items = rm_macos_binaries(os.listdir(candidate_path))
                video_pattern = "*.mp4"

                for item in candidate_items:
                    if fnmatch.fnmatch(item, video_pattern):
                        cols = st.columns(2)
                        video_path = os.path.join(path, candidate, item)
                        random_key = f"{candidate}_{item}"
                        with cols[0]:
                            start = st.number_input("Start Second", min_value=0, max_value=10000, key=f"start_{random_key}")
                        with cols[1]:                            
                            end = st.number_input("End Second", min_value=0, max_value=10000, key=f"end_{random_key}")
                        # Store the start and end values in the dictionary
                        candidate_start_end_pairs[random_key] = (start, end)
                        st.divider()

            submitted = st.form_submit_button("Submit")

        st.subheader("Creating Config Files with the interest Periods", divider="rainbow") 
        if submitted: 
        
            for candidate, (_, pair) in zip(candidates, candidate_start_end_pairs.items()):
                candidate_path = os.path.join(path, candidate)
                st.markdown(f"- Creating Config file for `{candidate}`.")
                config_dict = {"start": pair[0], "end": pair[1]}
                with open(os.path.join(candidate_path, "config.json"), 'w') as f:
                    json.dump(config_dict, f)

                
            st.divider()
            st.success("Configs Created!")




def configuration():
    st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)
    st.divider()

    # check if all the config files are present in the trials/sources 
        # if not 
            # run the collection part where each folder is iteratively selected, video is presented,
            # operator looks through and notes down the start second and end second
            # when all videos are processed it will prompt the user to click on the main page on the right
            # it will show a big message prompting the user that once the button is pressed there's no interruption
    
        # if yes 
            # it will prompt the user to go to the main page and start processing
    
    # Validation part 

    
    st.markdown("#### Traversing the trial folders and validating")

    doesnt_exist_count = 0
    exist_count = 0

    with st.status("Validation") as STATUS:

        candidates = rm_macos_binaries(os.listdir(path))

        for candidate in candidates:
            candidate_path = os.path.join(path, candidate)
            candidate_items = rm_macos_binaries(os.listdir(candidate_path))
            st.markdown(f"#### {candidate}")
            st.markdown(f"`items in {candidate}`")
            # st.code(candidate_items)
            items_to_match = ["gaze.csv","*.mp4","config.json"]

            matched_items = []
            for pattern in items_to_match:
                for item in candidate_items:
                    if fnmatch.fnmatch(item, pattern):
                        matched_items.append(item)

            # st.code(matched_items)

            if "config.json" in matched_items:
                st.success("Config files exist!")
                exist_count += 1

            else:
                st.error("Config doesn't exist!")
                doesnt_exist_count +=1 


    st.divider()
    INITIATE_FLAG = False
    if exist_count < doesnt_exist_count:
        st.markdown("##### All or Few config files are missing, proceeding to config population.")
        STATUS.update(expanded=False, state="error")
        INITIATE_FLAG = True
    else:
        st.markdown("##### All Config files exists, Proceed to Pipeline! Click on Main in the Sidebar!")
        expander = st.expander("Re-Do Config Files!")
        if expander.button("Re-Run Config Creation"):
            watch_videos_create_configs(INITIATE_FLAG=True)
            

        STATUS.update(expanded=True,state= "complete")

    watch_videos_create_configs(INITIATE_FLAG)

    


                    







configuration()
