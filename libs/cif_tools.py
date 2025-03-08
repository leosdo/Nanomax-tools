import Dans_Diffraction as dif
import pandas as pd
from xraydb import material_mu
import matplotlib.pyplot as plt
import numpy as np
import re

def cif_params(cif_path):
    xtl = dif.Crystal(cif_path)
    formula = xtl.cif["_chemical_formula_sum"].replace(' ', '')
    density = float(xtl.cif['_exptl_crystal_density_diffrn'])
    cell_params = pd.DataFrame(str(xtl.Cell).split("\n")[:-1])
    return formula, density, cell_params, xtl

def plot_transmission(formula, density):
    energy = np.linspace(5000, 20000, 1000)
    mu = 10**-4*material_mu(formula, energy, density = density) #1/cm to 1/microns
    fig, ax = plt.subplots(2, 1, figsize = (5,6))
    ax[0].plot(energy/1000, 1/mu, label = formula) #in microns
    ax[0].set_xlabel('Energy [keV]')
    ax[0].set_ylabel(r'Attenuation length [$\mu$m]')
    ax[0].grid(linewidth = 0.4)
    ax[0].set_xlim(energy[0]/1000, energy[-1]/1000)
    ax[0].legend()
    ##
    energy_new = np.linspace(5000, 20000, 5)
    thickness = np.linspace(1, 1000000, 100000) #nm to mm
    transmission = np.empty((np.shape(energy_new)[0], np.shape(thickness)[0]))
    ###
    for i, j in enumerate(energy_new):
        mu_energy_loop = material_mu(formula, j, density = 5)*10**-7 #1/cm to 1/nm
        for k, l in enumerate(thickness):
            transmission[i,k] = 100*np.exp(-l*mu_energy_loop)
        ax[1].plot(thickness, (transmission[i,:]), label = j/1000)
    ax[1].set_xlabel("Thickness [nm]")
    ax[1].set_ylabel("Transmission [%]")
    ax[1].legend(title = "Energy [keV]", framealpha = 1)
    ax[1].grid(linewidth = 0.5, which = "both")
    ax[1].set_xlim(1, 1000000)
    ax[1].set_xscale("log")
    ##
    fig.tight_layout()
    #delta, beta, _ = xray_delta_beta(formula, density, energy) #g/cm3
    #fig, ax = plt.subplots(1,1,dpi = 100)
    #ax.plot(energy/1000, delta/beta, label = formula)
    #ax.set_xlabel("Energy (keV)")
    #ax.set_ylabel(r"$\delta$ / $\beta$")
    #ax.legend(frameon=False)
    #ax.grid()    
    return fig

def xrdplot(xtl, form_values):
    xtl.Scatter.setup_scatter(scattering_type = 'x-ray', 
                              energy_kev = float(form_values["energy"]), 
                              min_twotheta = float(form_values["min_tth"]),
                              max_twotheta =float(form_values["max_tth"])
                            )
    twotheta, inten, _ = xtl.Scatter.powder(units='twotheta')
    ref_list = xtl.Scatter.print_all_reflections()
    ref_list = ref_list.split("\n")[2:-2]
    #
    hkl_values = []
    two_theta_values = []
    intensity_values = []
    #
    plank = 6.6261*10**-34 # j*s
    light = 2.9979*10**8 #m/s
    kev_to_j = 1.602176634*10**-16 #J
    wave = np.round(10**10*plank*light/(float(form_values["energy"])*kev_to_j),4) # angstrons
    # Pattern to match each line of data, except the header
    pattern = r'\(\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)\s+([\d.]+)\s+([\d.]+)'
    # Process each line of data, starting from the second line
    for line in ref_list[1:]:  # Skip the header
        match = re.search(pattern, line)
        if match:
            # Append each group to the corresponding list
            hkl_values.append(f"({match.group(1)}, {match.group(2)}, {match.group(3)})")
            two_theta_values.append(float(match.group(4)))
            intensity_values.append(float(match.group(5)))
    d_spacing_values = wave/(2*np.sin(np.deg2rad(two_theta_values)/2))
    Q_values = 4*np.pi*np.sin(np.deg2rad(two_theta_values)/2)/wave
    ##
    peak_table = pd.DataFrame({'(h k l)': hkl_values,
                               '2theta [deg]': two_theta_values,
                               'd [Å]': d_spacing_values,
                               'Q [Å]': Q_values,
                               'Intensity': intensity_values}
                               )
    fig, ax = plt.subplots(1,1,dpi = 100)
    ax.plot(twotheta, inten)
    ax.set_xlabel(f"2$\\theta$[@{float(form_values['energy'])} keV]")
    ax.set_ylabel("Intensity (a.u.)")
    ax.legend(frameon=False)
    ax.grid(linewidth = 0.4)    
    return fig, peak_table

    
    