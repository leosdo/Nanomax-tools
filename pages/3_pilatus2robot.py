import streamlit as st
from libs import detectorswap
import numpy as np
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile

st.title ("Pilatus 1M to robot arm detector")
st.markdown(r"""
By uploading a `.poni` file and setting the pixel positions (x,y), you will obtaing:
- the gamma angle
- the delta angle

NB: the uploaded files are not stored after use !
""")


def upload_poni():
    poni_uploader = st.file_uploader(label = "Upload .poni file", type = ".poni", key = "poni")
    poni_path = None
    if poni_uploader is not None:
        with NamedTemporaryFile(dir='.', suffix='.poni', delete = False) as f:
            f.write(poni_uploader.getbuffer())
            poni_path = f.name
    return poni_path
# upload_cif()

poni_path = upload_poni()

if poni_path:
    
    form_values = {}

    st.subheader("Set Pixel to conversion", divider=True)
    with st.form(key = "user_form"):
        col1, col2 = st.columns(2)
        with col1:
            form_values["pixel_x"] = st.number_input("Pixel x [num]", value=0.0)

        with col2:
            form_values["pixel_y"] = st.number_input("Pixel y [num]",value=0.0)
        submit_button = st.form_submit_button()
        #
        if submit_button:
                if form_values["pixel_x"] == 0.0 or form_values["pixel_y"] == 0.0:
                    st.warning("Please provide non-zero values for both pixel positions.")
                else:
                    try:
                        delta, gamma, tth = detectorswap.pilatus2robot(poni_path, px = form_values["pixel_x"], py = form_values["pixel_y"])
                        st.write("The delta angle is = ", np.round(delta, 5), "[deg.]")
                        st.write("The gamma angle is = ", np.round(gamma, 5), "[deg.]")
                        st.write(r" The 2$\theta$ is  angle is = ", np.round(tth, 5), "[deg.]")
                    except Exception as e:
                        st.error(f"An error occurred during calculation: {e}")

