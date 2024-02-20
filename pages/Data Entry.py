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




def rm_macos_binaries(item_list):

    try: 
        item_list.remove(".DS_Store")
        return item_list

    except:
        
        return item_list
    
def convert_df_to_csv(df):
    # Convert DataFrame to CSV, then to string (if no index is desired, set index=False)
    return df.to_csv(index=False).encode('utf-8')
    

def check_template_matches(files_and_values):

    items_to_match = ["*.mp4"]

    
    for template in items_to_match:
      
        matches = fnmatch.filter(files_and_values, template)
        if not matches:
            return False
    
    return matches




st.set_page_config(layout="wide", page_title="GazeCNN Software")
st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)

st.divider()
st.markdown('''<center><span style="font-size:40px; font-family:'poppins'; color:dodgerblue; font-weight:bold;">Identifying Start and End Time of a Trial.</span></center>''',unsafe_allow_html=True)
st.markdown("")
st.markdown("")
st.markdown('''<center><span style="font-size:25px; font-family:'poppins'; color:red; font-weight:bold;">Enter Start and End time as a whole number for example: time 1min:20secs i.e 1.20 will be 120.</span></center>''',unsafe_allow_html=True)
st.markdown("")
st.markdown("")
st.divider()











path = "./trials"
    
items = os.listdir(path)
items = rm_macos_binaries(items)


video_paths = []

# Make lists prior to start entering
for item in items:

    # this will normally be directories of individual participants
    candidate_path = os.path.join(path, item)
    video_name = check_template_matches(os.listdir(candidate_path))
    video_path = os.path.join(path, item, video_name[0])
    video_paths.append(video_path)


# st.write()
    
tabs = st.tabs(items)


for tab,item, video_path in zip(tabs,items, video_paths):
    tab.subheader(item)
    tab.video(video_path, )


st.divider()
st.subheader("Enter Times in the Form.")

with st.form("Record Data"):
    video_pattern = "*.mp4"
    
    
    times = {}
        
    for item in items:
        
        st.subheader(item,divider="rainbow")
        cols = st.columns(2)
        random_key = f"{item}_"
        # st.write(random_key)
        with cols[0]:
            start = st.number_input("Start time", min_value=0, max_value=10000, key=f"start_{random_key}")
        with cols[1]:                            
            end = st.number_input("End time", min_value=0, max_value=10000, key=f"end_{random_key}")
        
        if start > end: 
            st.error("Start Time Cannot be larger than End Time!")
    
        st.divider()

        times[item] = {"start": start, "end": end}


    submit = st.form_submit_button("submit")
            


valid = True
for candidate, (start, end) in times.items():
    if start >= end:
        valid = True

    else:
        valid = False
        break




if submit and valid:
    # Process/display the times dictionary in the desired format
    st.write(times)

    df = pd.DataFrame(list(times.items()), columns=['Item', 'Time'])
    # Split the Time tuple into Start and End columns
    df[['Start', 'End']] = pd.DataFrame(df['Time'].tolist(), index=df.index)
    # Drop the original 'Time' column as it's no longer needed
    df.drop(columns=['Time'], inplace=True)

    df.columns = ["candidate","start","end"]

    st.data_editor(df)

    csv = convert_df_to_csv(df)

    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="config.csv",
    mime="text/csv",
)

elif submit:
    st.write(times)
    st.error(f"{candidate} times are invalid, Start time > or = End Time Fix it.")





