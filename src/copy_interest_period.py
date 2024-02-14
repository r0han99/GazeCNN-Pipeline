import shutil 
import os
import numpy as np 
import streamlit as st



PATH = "./trials"


def rm_macos_binaries(item_list):

    try: 
        item_list.remove(".DS_Store")
        return item_list

    except:
        
        return item_list


def interest_area(start_frame, end_frame, candidate, candidate_path):

    global PATH
    source_path = os.path.join(PATH, candidate,f"{candidate}_source")
    
    

    st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> Start-frame: <b>{start_frame}</b>, End-frame: <b>{end_frame}</b></span>", unsafe_allow_html=True)
    if os.path.exists(candidate_path):
        folder_name = candidate+"_interest_period"
        folder_path = os.path.join(candidate_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    destination_folder_path = folder_path

    file_names = ["frames_" +x+".jpg" for x in list(map(str,list(np.arange(start_frame, end_frame+1))))]
    count_for_validation = len(file_names)

    

    # validate if the files are already moved
    if len(rm_macos_binaries(os.listdir(destination_folder_path))) == count_for_validation+1:
        
        st.success(f"{candidate.capitalize()}: Interest Period is already created!")

    else:
        st.markdown('Executing `Shutil Move!` copying interest area to a separate folder.')
        progress_bar = st.progress(0) 
        for i, file_name in enumerate(file_names):
            path_to_file = os.path.join(source_path, file_name)
            
            shutil.move(path_to_file, destination_folder_path)
            
            # Update progress bar
            progress_percent = (i + 1) / len(file_names)
            progress_bar.progress(progress_percent)

        st.success(f"{candidate.capitalize()}: Interest Period Created")
     


    st.divider()
    