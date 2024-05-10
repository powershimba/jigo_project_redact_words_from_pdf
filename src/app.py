import streamlit as st
import module as module
from streamlit_tags import st_tags_sidebar

st.title('Redact words from PDF docs')

col1, col2 = st.columns(2)

with col1:

    st.subheader('👆 Upload your pdf')
    uploaded_file = st.file_uploader(
        "Upload PDF contract file", 
        type = 'pdf')

    if uploaded_file != None:
        module.show_pdf(uploaded_file, 1)

with col2:
    st.subheader('✅ Get Redacted PDF')

if uploaded_file != None:
    sensitive_words = st_tags_sidebar(
        label = '# Enter Words to Redact',
        text = 'max 4 words',
        maxtags = 4
    )

    if st.sidebar.button("Done!"):  
        st.sidebar.write("Developing...")