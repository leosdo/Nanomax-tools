import numpy as np
import pandas as pd
from xraydb import material_mu
import matplotlib.pyplot as plt
#plt.style.use('petroff10')

def transmission_factor(layer, energy_eV, angle):
    
    theta = np.deg2rad(angle)
    angle_factor = 1 / np.cos(theta)

    t_cm = layer['thickness'] * 1e-7 * angle_factor
    rho = layer['density']
    material = layer['compound']

    trans = np.zeros_like(energy_eV)

    for i, E in enumerate(energy_eV):
        try:
            mu = material_mu(material, E, density=rho) #already in cm-1
            trans[i] = np.exp(-mu * t_cm)
        except:
            trans[i] = 0

    return trans


def transmission_single_energy(layer, energy_eV, angle):
    
    theta = np.deg2rad(angle)
    angle_factor = 1 / np.cos(theta)

    t_cm = layer['thickness'] * 1e-7 * angle_factor
    rho = layer['density']
    material = layer['compound']

    try:
        mu = material_mu(material, energy_eV, density=rho) #already in cm-1
        trans = np.exp(-mu * t_cm)
    except:
        trans = 0

    return trans


def compute_multilayer_transmission(compounds, energy_keV, angle):

    energy_single_eV = energy_keV * 1000
    energy_axis_eV = np.linspace(5000, 25000, 201)

    # Compute per-layer transmission
    layer_trans = [transmission_factor(layer, energy_axis_eV, angle) 
                    for layer in compounds]

    cumulative_trans = np.ones_like(energy_axis_eV)
    for t in layer_trans:
        cumulative_trans *= t

    # -------------------------
    # Plot
    # -------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi = 600)

    for i, t in enumerate(layer_trans):
        layer = compounds[i]
        ax.plot(
            energy_axis_eV / 1000,
            t * 100, #to show in %
            label=f"{i+1}: {layer['compound']} ({layer['thickness']} nm)", alpha = 0.6,
        )

    ax.set_title(f'Multilayer Transmission at {angle} deg.')
    ax.plot(energy_axis_eV / 1000, cumulative_trans * 100, '-k', label="Cumulative", linewidth=2)
    ax.axvline(energy_keV, color='red', linestyle='--', linewidth=1.5, label=f'Selected Energy: {energy_keV:.3f} keV')
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Transmission (%)")
    ax.grid(True)
    ax.legend(title="Layers")
    ax.set_xlim(5, 25)

    # -------------------------
    # Table at SINGLE ENERGY
    # -------------------------
    cumulative = 1.0
    rows = []
    
    theta = np.deg2rad(angle)
    angle_factor = 1 / np.cos(theta)

    for i, lyr in enumerate(compounds):
        T_layer = transmission_single_energy(lyr, energy_single_eV, angle)
        cumulative *= T_layer

        rows.append({
            "Layer": i + 1,
            "Compound": lyr["compound"],
            "Density (g/cm³)": lyr["density"],
            "Thickness (nm)": lyr["thickness"],
            "Effective Thickness (nm)": round(lyr["thickness"] * angle_factor, 6),
            "Transmission (%)": round(T_layer * 100, 6),
            "Cumulative (%)": round(cumulative * 100, 6),
        })

    df = pd.DataFrame(rows)

    return fig, df
