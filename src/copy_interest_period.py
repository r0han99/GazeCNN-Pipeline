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
    
def rm_flag_file(item_list):
    try: 
        item_list.remove(".flag_file")
        return item_list

    except:
        
        return item_list


def interest_area(start_frame, end_frame, candidate, candidate_path):

    global PATH
    source_path = os.path.join(PATH, candidate,f"{candidate}_source")
    
    # st.title(source_path)
    # st.title(type(start_frame))
    # st.title(type(end_frame))
    # st.title(candidate)
    # st.title(candidate_path)

    st.markdown(f"<span><span style='font-size:30px; font-weight:bold;'>{candidate.capitalize()}</span> Start-frame: <b>{start_frame}</b>, End-frame: <b>{end_frame}</b> ~ {abs(int(end_frame)- int(start_frame))} Frames</span>", unsafe_allow_html=True)
    if os.path.exists(candidate_path):
        folder_name = candidate+"_interest_period"
        folder_path = os.path.join(candidate_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    destination_folder_path = folder_path

    file_names = ["frames_{:04d}.jpg".format(int(x)) for x in np.arange(start_frame, end_frame+1)]
    #st.code(file_names)
    count_for_validation = len(file_names)
    #st.title(count_for_validation)

    try:

        with open(os.path.join(destination_folder_path, ".interest_area_flag_file"), 'r') as f:
            content = f.readline()
            # validate ifrrr the files are already moved
        if content == "interest-area":
            
            st.success(f"{candidate.capitalize()}: Interest Period is already created!")

    except FileNotFoundError:
        
        st.markdown('Executing `Shutil Copy!` copying interest area to a separate folder.')
        
        progress_bar = st.progress(0) 

        #st.code(file_names)
        
        for i, file_name in enumerate(file_names):
            
            path_to_file = os.path.join(source_path, file_name)
            
            shutil.copy(path_to_file, destination_folder_path)
            
            # Update progress bar
            progress_percent = (i + 1) / len(file_names)
            progress_bar.progress(progress_percent)

        st.success(f"{candidate.capitalize()}: Interest Period Created")
        with open(os.path.join(folder_path, ".interest_area_flag_file"), 'w') as f:
            f.write("interest-area")
     


    st.divider()
    