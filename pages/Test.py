import streamlit as st
import subprocess

import time


st.markdown('''<center><span style="font-size:170px; color:orangered; font-family:'poppins';"> Testing Area</span></center>''', unsafe_allow_html=True)
st.divider()


from fire_state import create_store, form_update, get_state, set_state, get_store, set_store
# create in session state a slot with key-value pair
create_store("MY_SLOT_NAME", [("my_btn", False)])

# define button
button = st.button("Know")

# update value in session state to value equal of button e.g. True if clicked
set_state("MY_SLOT_NAME", ("my_btn", button))

# set condition to only code run if button is not True
if get_state("MY_SLOT_NAME", "my_btn") != True:
  st.write("do not run this!")





def process_1():
    st.subheader("Process 1")
    for num in range(0, 5):
        st.code(num)

def process_2():
    st.subheader("Process 2")
    for num in range(0, 7):
        st.code(num)

def process_3(start, end):
    st.subheader("Process 3")
    for num in range(start, end):
        st.code(num)

# Initialize session state variables if they don't exist
if 'initiated' not in st.session_state:
    st.session_state['initiated'] = False

if 'process_1_and_2_done' not in st.session_state:
    st.session_state['process_1_and_2_done'] = False

if st.button("START processes!") or st.session_state['initiated']:
    st.session_state['initiated'] = True

    if not st.session_state['process_1_and_2_done']:
        process_1()
        process_2()
        st.session_state['process_1_and_2_done'] = True

    # Only show inputs and run process_3 after process_1 and process_2 are done
    if st.session_state['process_1_and_2_done']:
        start = st.number_input("Enter Start Seconds", min_value=0)
        end = st.number_input("Enter End Seconds", min_value=0)

        # Process 3 is executed only when both start and end have been entered
        if start and end:
            process_3(start, end)



import streamlit as st

# Create three sections for "Start" and "End" categories
with st.form("Input Form"):
    # First category: Start
    st.write("Category: Start")
    start_values = []
    for i in range(1, 4):
        start_values.append(st.number_input(f"Start {i}", value=0))

    # Second category: End
    st.write("Category: End")
    end_values = []
    for i in range(1, 4):
        end_values.append(st.number_input(f"End {i}", value=0))

    # Submit button
    submitted = st.form_submit_button("Submit")

# If the form is submitted, display the values
if submitted:
    st.write("Start Values:", start_values)
    st.write("End Values:", end_values)
