import streamlit as st
from tempfile import NamedTemporaryFile
from libs import multistack_absorption

st.title("Multistack Absorption Calculator")



st.markdown("""
Enter your stack configuration below, including density, thickness, and compound
for each layer. The incidence angle is **required** and is half of the Bragg angle (gonphi) (0° = normal incidence).
            
You can also upload your previlisy saved section.

""")

# ---------------------------
# Initialize session state
# ---------------------------

if "num_compounds" not in st.session_state:
    st.session_state.num_compounds = 1
if "input_mode" not in st.session_state:
    st.session_state.input_mode = None
if "loaded_data" not in st.session_state:
    st.session_state.loaded_data = None

# ---------------------------
# Choose load or manual input
# ---------------------------

st.subheader("Choose input method")
col1, col2 = st.columns(2)

with col1:
    if st.button("Load from file", use_container_width=True):
        st.session_state.input_mode = "load"
        st.session_state.loaded_data = None
        st.rerun()

with col2:
    if st.button("Manual input", use_container_width=True):
        st.session_state.input_mode = "manual"
        st.session_state.loaded_data = None
        st.session_state.num_compounds = 1
        st.rerun()

# ---------------------------
# Temporary file upload function
# ---------------------------
def process_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    with NamedTemporaryFile(suffix=".txt", delete=True) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file.flush()
        tmp_file.seek(0)
        content = tmp_file.read().decode("utf-8")

    loaded_energy = None
    loaded_angle = None
    loaded_compounds = []
    num_layers = 0

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("Energy:"):
            loaded_energy = float(line.split(":")[1].strip())
        elif line.startswith("Angle:"):
            loaded_angle = float(line.split(":")[1].strip())
        elif line.startswith("Number_of_Layers:"):
            num_layers = int(line.split(":")[1].strip())
        elif line.startswith("Layer_"):
            parts = line.split(":")[1].strip().split(",")
            if len(parts) == 3:
                formula = parts[0].strip()
                density = float(parts[1].strip())
                thickness = float(parts[2].strip())
                loaded_compounds.append({
                    "compound": formula,
                    "density": density,
                    "thickness": thickness
                })

    return {
        "energy": loaded_energy,
        "angle": loaded_angle,
        "compounds": loaded_compounds,
        "num_layers": num_layers
    }


# ----------------------------------------
# SHOW INPUT UI ONLY IF MODE IS SELECTED
# ----------------------------------------
if st.session_state.input_mode is not None:

    # ---------------------------
    # LOAD MODE
    # ---------------------------
    if st.session_state.input_mode == "load":
        st.subheader("Load from file")
        uploaded_file = st.file_uploader("Upload multilayer TXT", type=["txt"])

        if uploaded_file is not None:
            if st.button("Load Parameters"):
                loaded_data = process_uploaded_file(uploaded_file)
                if loaded_data:
                    st.session_state.loaded_data = loaded_data
                    st.session_state.num_compounds = loaded_data["num_layers"]
                    st.success("Parameters loaded successfully!")
                    st.rerun()

    # ---------------------------
    # MANUAL INPUT OR LOADED DATA DISPLAY
    # ---------------------------
    show_inputs = False
    if st.session_state.input_mode == "manual":
        show_inputs = True
    elif st.session_state.input_mode == "load" and st.session_state.loaded_data:
        show_inputs = True

    if show_inputs:
        # Experimental conditions
        st.subheader("Experimental Conditions")
        col1, col2 = st.columns(2)

        if st.session_state.loaded_data:
            energy_value = st.session_state.loaded_data["energy"]
            angle_value = st.session_state.loaded_data["angle"]
        else:
            energy_value = 100.0
            angle_value = 45.0

        with col1:
            energy = st.number_input("Energy (keV)", min_value=0.0, value=energy_value, step=0.1)
        with col2:
            angle = st.number_input("Angle (degrees)", min_value=0.0, value=angle_value, step=0.1)

        # Multilayer sequence
        st.markdown("---")
        st.subheader("Multilayer Sequence")

        compounds = []
        for i in range(st.session_state.num_compounds):
            st.markdown(f"#### Layer # {i+1}")

            if st.session_state.loaded_data and i < len(st.session_state.loaded_data["compounds"]):
                loaded = st.session_state.loaded_data["compounds"][i]
                formula_value = loaded["compound"]
                density_value = loaded["density"]
                thickness_value = loaded["thickness"]
            else:
                formula_value = "Si"
                density_value = 2.33
                thickness_value = 100.0

            col1_layer, col2_layer, col3_layer = st.columns(3)
            with col1_layer:
                formula = st.text_input("Chemical Formula", key=f"formula_{i}", value=formula_value)
            with col2_layer:
                density = st.number_input("Density (g/cm³)", key=f"density_{i}",
                                          min_value=0.0, step=0.01, value=density_value)
            with col3_layer:
                thickness = st.number_input("Thickness (nm)", key=f"thickness_{i}",
                                            min_value=0.0, step=0.1, value=thickness_value)

            compounds.append({
                "compound": formula,
                "density": density,
                "thickness": thickness
            })

        # ---------------------------
        # ACTION BUTTONS IN ONE ROW
        # ---------------------------
        st.markdown("---")
        col_add, col_save, col_compute, col_reset = st.columns(4)

        with col_add:
            if st.button("Add New Layer") and st.session_state.num_compounds < 10:
                st.session_state.num_compounds += 1
                st.rerun()

        with col_save:
            if st.button("Save Parameters"):
                data_lines = [
                    f"Energy: {energy}",
                    f"Angle: {angle}",
                    f"Number_of_Layers: {st.session_state.num_compounds}"
                ]
                for i, c in enumerate(compounds):
                    data_lines.append(f"Layer_{i+1}: {c['compound']}, {c['density']}, {c['thickness']}")
                data_str = "\n".join(data_lines)
                st.download_button("Download parameters as TXT", data=data_str,
                                   file_name="multilayer_parameters.txt", mime="text/plain")
                st.success("Parameters saved!")

        with col_compute:
            compute_clicked = st.button("Compute")

        # render outside the columns so it has full width
        if compute_clicked:
            fig, df = multistack_absorption.compute_multilayer_transmission(compounds, energy, angle)
            st.markdown("---")
            #st.subheader("Transmission Plot")
            st.pyplot(fig, use_container_width=True)

            st.subheader(f"Computation at {energy} keV")
            st.dataframe(df, use_container_width=True)

        with col_reset:
            if st.button("Reset to Default"):
                st.session_state.num_compounds = 1
                st.session_state.input_mode = None
                st.session_state.loaded_data = None
                st.rerun()
