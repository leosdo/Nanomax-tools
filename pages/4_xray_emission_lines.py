import streamlit as st
from libs import xray_emissison
from collections import OrderedDict

st.title ("X ray emission lines")
st.markdown(r"""
Type below the element you are interest to check the if the emission lines are in the range
of X-ray energy you are targeting the sample.  

NB: Oxigen and Argon will always be ploted alongwith the selected elements.

""")

st.subheader("Select atoms", divider=True)
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

#col_f5 = st.columns(1)[0]
with st.form(key="form_combined"):
    placeholder= "Empty"
    with col_f1:
        el_1 = st.text_input("Element 1", placeholder= placeholder)
    with col_f2:
        el_2 = st.text_input("Element 2", placeholder= placeholder)
    with col_f3:
        el_3 = st.text_input("Element 3", placeholder= placeholder)
    with col_f4:
        el_4 = st.text_input("Element 4", placeholder= placeholder)
    submitted = st.form_submit_button("Run", use_container_width = True)
 # After the form is submitted, display the inputs
if submitted:
    atom_list = [el_1, el_2, el_3, el_4]
    atom_list = ' '.join(atom_list).split()
    for i in atom_list:
        if not i.isalpha(): #check if they are letters or not
            st.warning("Please provide only letters for elements.")
            atom_list.remove(i) 
            #atoms_list = ' '.join(atom_list).split()
    atom_list.extend(['Ar', 'O'])

    fig = xray_emissison.plotxraylines(list(OrderedDict.fromkeys(atom_list))) ##remove duplicates a preserver the order
    st.pyplot(fig)
