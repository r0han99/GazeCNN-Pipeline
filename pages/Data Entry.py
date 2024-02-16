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






def check_template_matches(files_and_values):

    items_to_match = ["*.mp4"]

    
    for template in items_to_match:
      
        matches = fnmatch.filter(files_and_values, template)
        if not matches:
            return False
    
    return matches


def rm_macos_binaries(item_list):

    try: 
        item_list.remove(".DS_Store")
        return item_list

    except:
        
        return item_list
    


def show_trial_video(candidate, video_path):

    
    path = "./trials"
    


    with st.form(candidate):
    
        st.markdown(f"<center><span style='font-size:40px; font-weight:bold; '>Candidate - {candidate}</span></center>",unsafe_allow_html=True)
        st.divider()
        candidate_path = os.path.join(path, candidate)
        candidate_items = rm_macos_binaries(os.listdir(candidate_path))
        video_pattern = "*.mp4"
        candidate_start_end_pairs = {}
        for item in candidate_items:
            if fnmatch.fnmatch(item, video_pattern):
                cols = st.columns([2,5,2])
                cols[1].video(video_path)
                cols = st.columns(2)
                
                random_key = f"{candidate}_{item}"
                with cols[0]:
                    start = st.number_input("Start time", min_value=0, max_value=10000, key=f"start_{random_key}")
                with cols[1]:                            
                    end = st.number_input("End time", min_value=0, max_value=10000, key=f"end_{random_key}")
                # Store the start and end values in the dictionary
                candidate_start_end_pairs[random_key] = (start, end)
                st.divider()

        
        submitted = st.form_submit_button("Submit",use_container_width=True)

    if submitted: 
        
        if end < start:
            st.error("End Time should not be less than Start Time")

        return start, end 
    
    else:
        
        return None, None


    st.markdown("")
    st.markdown("")
    st.divider()
    




def main():


    path = "./trials"
    
    items = os.listdir(path)
    items = rm_macos_binaries(items)
    st.divider()
    st.markdown('''<center><span style="font-size:40px; font-family:'poppins'; color:dodgerblue; font-weight:bold;">Identifying Start and End Time of a Trial.</span></center>''',unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown('''<center><span style="font-size:25px; font-family:'poppins'; color:red; font-weight:bold;">Enter Start and End time as a whole number for example: time 1min:20secs i.e 1.20 will be 120.</span></center>''',unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.divider()
    

    
    if os.path.exists(path):

        for candidate in items:

            # this will normally be directories of individual participants
            candidate_path = os.path.join(path, candidate)
            video_name = check_template_matches(os.listdir(candidate_path))
            video_path = os.path.join(path, candidate, video_name[0])
            
            start, end = show_trial_video(candidate, video_path)
            
            if candidate not in st.session_state:

                st.session_state.candidate = (start, end)


        #st.write(dict(st.session_state))
        to_series = pd.Series(st.session_state)
        # st.write(to_series)
        filtered_series = to_series[to_series.index.str.startswith(('start', 'end'))]
        # st.write(filtered_series)
        start_series = filtered_series[filtered_series.index.str.startswith(('start'))]
        end_series = filtered_series[filtered_series.index.str.startswith(('end'))]


        st.divider()
        st.subheader("Start and End Times Data Preview",divider="red")


        # st.write(pd.DataFrame(start_series).reset_index())

        start_df = pd.DataFrame(start_series).reset_index()
        end_df = pd.DataFrame(end_series).reset_index()

        start_df['index'] = start_df['index'].apply(lambda x: x.split("_")[1])
        end_df['index'] = end_df['index'].apply(lambda x: x.split("_")[1])

        start_df.columns = ['candidate','start']
        end_df.columns = ['candidate','end']

        config = pd.concat([start_df, end_df.drop('candidate',axis=1)],axis=1)
        config = config.set_index("candidate")

        st.data_editor(config)
        



if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="GazeCNN Software")
    st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)
    main()