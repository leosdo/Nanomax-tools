import streamlit as st
from libs import conversions 

col_f1, col_f2 = st.columns(2)

# Form for X-ray energy
with col_f1:
    with st.form(key="form_xray"):
          st.subheader("keV to Å", divider=True)
          xray_energy = st.number_input("X-ray energy [keV]", key="xray_energy", placeholder = "insert number", value= 8.04)
          submit_xray = st.form_submit_button(label="Run")
          wave_angs = conversions.keV_angs(xray_energy)
          if submit_xray:
               wave_angs = conversions.keV_angs(xray_energy)
               st.write("The wavelenth is: ", wave_angs, "[Å]")

# Form for Wavelength
with col_f2:
    with st.form(key="form_wavelength"):
          st.subheader("Å to keV", divider=True)
          wavelength = st.number_input("Insert a wavelength [Å]", key="wavelength", placeholder = "insert number", value = 1.5421)
          submit_wavelength = st.form_submit_button(label="Run")
          energy_keV = conversions.angs_keV(wavelength)
          if submit_wavelength:
               energy_keV = conversions.angs_keV(wavelength)
               st.write("The energy is: ", energy_keV, "[keV]")
####
st.subheader("Bragg @ energy", divider=True)
col_f3, col_f4 = st.columns(2)
col_f5 = st.columns(1)[0]
with st.form(key="form_combined"):
    with col_f3:
        select_en_in = st.number_input("Intial X-ray energy [keV]")
    with col_f4:
        select_en_fin = st.number_input("Final X-ray energy [keV]")
    with col_f5:
        select_tth = st.number_input(r"$2\theta$ [deg.]")
    new_tth = conversions.newbragg(select_en_in, select_tth, select_en_fin)
    submitted = st.form_submit_button("Run", use_container_width = True)
  

# After the form is submitted, display the inputs
if submitted:
    st.write(f"The new Bragg angle at {select_en_fin} keV is ", new_tth, ".deg")
    #st.write(r"$2\theta$ (deg):", select_tth)
    #st.write("The current number is ", number)

#st.subheader("Bragg @ energy", divider=True)

# st.subheader("what is d-spacing?", divider=True)
# with st.form("form 4"):
#     number = st.number_input("Insert a number")
#     submitted = st.form_submit_button("Run")
#     st.write("The current number is ", number)

# st.subheader(r"what is 2$\theta$ ?", divider=True)
# with st.form("form 5"):
#     number = st.number_input("Insert a number")
#     submitted = st.form_submit_button("Submit")
#     st.write("The current number is ", number)

