import matplotlib.pyplot as plt
import numpy as np

from seamless.data import prepare_mos

### PLOTTING EXPERIMENT MOS ###

def plot_mos():
    sorted_combined_mos =  prepare_mos()

    fig, ax = plt.subplots()
    
    labels = []
    for key in [k for k in sorted_combined_mos.keys()]:
        if 'mptcp' in key:
            labels.append('MPTCP')
        if 'seamless1' in key:
            labels.append('Model 1')
        if 'seamless2' in key:
            labels.append('Model 2')
        if 'stock' in key:
            labels.append('Stock')
        if 'z_' in key:
            labels.append('')

    ax.xaxis.set_tick_params(rotation=90)
    ax.boxplot(sorted_combined_mos.values(), labels=labels, whis=1000000)
    
    xticks = ax.xaxis.get_major_ticks()
    xticks[4].set_visible(False)
    xticks[9].set_visible(False)
    xticks[14].set_visible(False)
    
    ax.set_ylabel('$MOS_{combined}$')
    ax.set_ylim(1, 5)
    ax.yaxis.set_ticks(np.arange(1, 5.1, 1))
    ax.text(.15, -0.1, "Scenario 1", transform=plt.gcf().transFigure)
    ax.text(.35, -0.1, "Scenario 2", transform=plt.gcf().transFigure)
    ax.text(.555, -0.1, "Scenario 3", transform=plt.gcf().transFigure)
    ax.text(.76, -0.1, "Scenario 4", transform=plt.gcf().transFigure)
    
    plt.show()