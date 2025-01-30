import streamlit as st
from libs import scan_time

col_f1, col_f2,  col_f2= st.columns(3)

st.subheader("Estimate time for scan", divider=True)

col_f1, col_f2, col_f3 = st.columns(3)
with st.form(key="form_combined"):
    with col_f1:
        npx = st.number_input("Number of steps along fast motor")
    with col_f2:
        npy = st.number_input("Number of steps along slow motor")
    with col_f3:
        exposure = st.number_input("exposure time")
    hh_mm_ss, total_time = scan_time.estimate_time(npx, npy, exposure, 0.3)
    #set now as 0.3.change it for new types of scan
    submitted = st.form_submit_button("Run", use_container_width = True)
    if submitted:
        st.write("Scan ends at:", total_time.replace(microsecond=0))
        st.write('Time to scan:',  hh_mm_ss)