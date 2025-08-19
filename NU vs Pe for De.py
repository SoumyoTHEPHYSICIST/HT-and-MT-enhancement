# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 11:20:40 2025

@author: PC
"""

import numpy as np
import matplotlib.pyplot as plt

# Define Nusselt correlation from Ganesh & Koch (2007)
def Nu(Pe, De, a=0.378):
    return 1.0 + a*(Pe*De)**(1/3)

# Compute curves for various De
Pe_vals = np.logspace(0, 6, 200)
De_list = [0.0, 0.001, 0.01, 0.1, 1.0]
plt.figure(figsize=(6,4))
for De in De_list:
    Nu_vals = Nu(Pe_vals, De)
    label = f"De={De}"
    plt.loglog(Pe_vals, Nu_vals, label=label)
# Reference slope-1/3 line (arbitrary scaling)
ref_Pe = np.array([1e2, 1e6])
ref_Nu = Nu(ref_Pe, 0.1)  # take De=0.1 as example
plt.loglog(ref_Pe, ref_Nu, 'k--', label='slope 1/3')
plt.xlabel("Péclet number (Pe)")
plt.ylabel("Nusselt number (Nu)")
plt.title("Nu vs Pe for different Deborah numbers")
plt.legend()
plt.grid(True, which='both', ls=':')
plt.show()
