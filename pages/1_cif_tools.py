import streamlit as st
from libraries import cif_tools
import numpy as np
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile

st.title ("Experimental planner tools")
st.markdown(r"""
By uploading a `.cif` file, you will obtaing:
- Unit cell parameters
- Absorption spectra and transmission fractions
- Diffraction peaks (*hkl*, 2$\theta$, Q, d-spacing) at selected energy

NB: the uploaded files are not stored after use !
""")


def upload_cif():
    cif_uploader = st.file_uploader(label = "Upload .cif file", type = ".cif", key = "cif")
    cif_path = None
    if cif_uploader is not None:
        with NamedTemporaryFile(dir='.', suffix='.cif', delete = False) as f:
            f.write(cif_uploader.getbuffer())
            cif_path = f.name
    return cif_path
# upload_cif()

cif_path = upload_cif()

if cif_path:
    st.subheader("Unit cell parameters", divider=True)
    compound, density, cell_params, xtl = cif_tools.cif_params(cif_path)
    st.write("Compound:", compound)
    st.write("Lattice paramenters", cell_params)
    st.subheader("Absorption spectra", divider=True)
    st.pyplot(cif_tools.plot_transmission(compound, density))
#print(ref_list)

    form_values = {
        "energy": None,
        "min_tth": None,
        "max_tth": None,
        }

    st.subheader("Diffraction peaks", divider=True)
    with st.form(key = "user_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            form_values["energy"] = st.number_input("x-ray energy [keV]")

        with col2:
            form_values["min_tth"] = st.number_input(r"2$\theta$ min")

        with col3:
            form_values["max_tth"] = st.number_input(r"2$\theta$ max")
        submit_button = st.form_submit_button()
        #
        if submit_button:
                # Ensure all fields are filled and convert energy to float
                if not all(form_values.values()):
                    st.warning("Please fill all the fields.")
                else:
                    try:
                        # Convert energy input to float
                        form_values["energy"] = (form_values["energy"])
                        
                        # Plot XRD only if xtl was defined (CIF uploaded)
                        if 'xtl' in locals():
                            fig, peak_tables = cif_tools.xrdplot(xtl, form_values)
                            st.pyplot(fig)
                            st.dataframe(peak_tables, use_container_width= True)
                            #peak_tables.rename(columns={'2theta [deg]': st.latex("$2\theta$ [deg]")}, inplace=True)
                        else:
                            st.warning("Please upload a valid .cif file first.")
                    except ValueError:
                        st.error("Energy input must be a number.")


#     if submit_bottom:
#         if not all(form_values.values()):
#             st.warning("Hey, fill all the fields")

# if xtl:
#     alra = cif_tools.xrdplot(xtl, form_values)
#     st.pyplot(alra)

# @st.fragment()
# def load_url():
#     title = st.text_input("URL from Crystallography Open Database")
# load_url()

#referces
#X-rayDB and link
#Dans-diffraction and link
#Another one and link
