import xraydb
import matplotlib.pyplot as plt
import numpy as np

def plotxraylines(atom_list):
    fig, ax = plt.subplots(np.shape(atom_list)[0], 1, figsize = (6 , 10), dpi = 600, sharex = True, sharey = True)
    for i, element in enumerate(atom_list):
        edge = xraydb.xray_edges(element)
        #
        for edge_key, j in edge.items():
            #colors = cmap(np.linspace(0, 1, np.shape(energy_key)))
            for key, value in xraydb.xray_lines(element, edge_key).items(): 
                energy = value[0]/1000
                if energy <= 25:
                    #print(element, key, energy)
                    intensity = value[1]
                    #level = key + "(" + value[2] + "-" + value[3] +")"
                    level = key
                    ax[i].bar(energy, intensity, width = 0.08, label = level)
                    ax[i].grid(lw = 0.3)
                    #ax[i].text(energy - 0.2,intensity + 0.02, level)
        ax[i].legend(ncols = 4, title = f'{element} edges', fontsize=8, loc = 'upper left', bbox_to_anchor = (1.05, 1.1), markerscale = 0.1, frameon = False)
    ax[0].set_xlim(0, 26)
    #ax[0].set_ylim(0, 1e0)
    ax[0].set_yscale("log")
    ax[0].set_ylim(1e-5, 1)
    ax[i].set_xlabel("Energy [keV]")
    ax[i].set_xticks(np.arange(0, 27, 2))
    ax[0].set_title("X-ray emission lines")
    plt.show()
    return fig

