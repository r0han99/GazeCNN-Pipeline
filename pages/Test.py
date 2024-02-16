import streamlit as st
import subprocess

import time


st.markdown('''<center><span style="font-size:80px; color:orangered; font-family:'poppins';"> Testing Area</span></center>''', unsafe_allow_html=True)
st.divider()

for _ in range(10):
    st.sidebar.markdown("")
cols = st.sidebar.columns([3,1,3])
cols[0].image("./assets/brain.png", width=100)
cols[1].markdown("")

cols[1].markdown('''<center><span style="font-size:30px; font-family:'poppins'; color:black; font-weight:bold;"><a href="https://www.colorado.edu/lab/del/" style="color: black; text-decoration: none;"><u>Dellab</u></a></span></center>''',unsafe_allow_html=True)
cols[1].markdown('''<center><span style="font-size:25px; font-family:'poppins'; color:black;">Software</span></center>''',unsafe_allow_html=True)

# Function to create or get the session state
# def get_session_state():
#     return st.session_state

# # Main function to initialize the session state and store values
# def main():
#     # Get the session state
#     session_state = get_session_state()

#     # Check if 'my_tuple' key exists in session state, if not, initialize it with default values
#     if 'my_tuple' not in session_state:
#         session_state.my_tuple = (0, 0)  # Default values

#     # Create input fields for each element of the tuple
#     new_value_1 = st.number_input("Enter First Value", value=session_state.my_tuple[0])
#     new_value_2 = st.number_input("Enter Second Value", value=session_state.my_tuple[1])

#     # Update the session state with the new tuple
#     session_state.my_tuple = (new_value_1, new_value_2)

#     # Display the updated tuple
#     st.write("Updated Tuple:", session_state.my_tuple)
#     st.write(session_state)

# if __name__ == "__main__":
#     main()
