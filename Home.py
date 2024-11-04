import streamlit as st

st.set_page_config(
    page_title="home",
)

st.title("Experimental planner tools")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This page presents a collection of tools for experimental planning at NanoMAX.  
    Use the sidebars on the left to access and run the calculations you need.  

    If you don't have a .cif file for use with the CIF tools, you can download one for free from resources such as the [COD database](https://www.crystallography.net/cod/) or [Materials project](https://next-gen.materialsproject.org/).
    
    For improvements and suggestions, please feel free to message me [![Email Badge](https://img.shields.io/badge/email-leosdo@dtu.dk-078700ff?style=flat)](mailto:oliveira.leonardo@sljus.lu.se).  
    You can also contribute by forking the repository on GitHub.  
    
    [![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE)
"""
)