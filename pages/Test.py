import streamlit as st
from src.dellab import add_logo
import subprocess

import time


st.markdown('''<center><span style="font-size:80px; color:orangered; font-family:'poppins';"> Testing Area</span></center>''', unsafe_allow_html=True)
st.divider()

add_logo()

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
