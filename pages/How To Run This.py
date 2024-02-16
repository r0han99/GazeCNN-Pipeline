import streamlit as st 

st.markdown('''<center><span style="font-size:80px; font-family:'poppins'; color:orangered;">GazeCNN Pipeline Software</span></center>''',unsafe_allow_html=True)
st.divider()

for _ in range(10):
    st.sidebar.markdown("")

    
cols = st.sidebar.columns([3,1,3])
cols[0].image("./assets/brain.png", width=100)
cols[1].markdown("")

cols[1].markdown('''<center><span style="font-size:30px; font-family:'poppins'; color:black; font-weight:bold;"><a href="https://www.colorado.edu/lab/del/" style="color: black; text-decoration: none;"><u>Dellab</u></a></span></center>''',unsafe_allow_html=True)
cols[1].markdown('''<center><span style="font-size:25px; font-family:'poppins'; color:black;">Software</span></center>''',unsafe_allow_html=True)

st.title("Watch the video instructions on how to operate this application")





