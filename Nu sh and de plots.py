# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 22:02:44 2025

@author: PC
"""

import numpy as np
import matplotlib.pyplot as plt

# ---- User-set: baseline Newtonian correlations (examples; replace with your values) ----
# For demo, take Nu0 and Sh0 as constants or simple functions of Re, Pr, Sc
def Nu0(Re, Pr):  # placeholder (e.g., Dittus-Boelter for turbulent pipe would differ)
    return 0.664 * np.sqrt(Re) * Pr**(1/3)  # laminar flat-plate style scaling proxy

def Sh0(Re, Sc):  # analogous mass transfer
    return 0.664 * np.sqrt(Re) * Sc**(1/3)

# ---- Weak-VE correlation form (to be fitted or chosen) ----
# Nu/Nu0 = 1 + a1*De + a2*De^2 ; Sh/Sh0 = 1 + b1*De + b2*De^2
# Start with small positive a1,b1 to show enhancement; tune later with data.
def Nu_ratio_weakVE(De, a1=0.8, a2=0.15):
    return 1.0 + a1*De + a2*De**2

def Sh_ratio_weakVE(De, b1=0.7, b2=0.10):
    return 1.0 + b1*De + b2*De**2

# ---- Sweep parameters ----
Re = 100.0
Pr = 5.0
Sc = 1000.0

De_vals = np.linspace(0.0, 0.6, 50)     # weak viscoelasticity range
Wi_vals = De_vals.copy()                 # for simple shear, Wi ~ De (same order)

Nu0_val = Nu0(Re, Pr)
Sh0_val = Sh0(Re, Sc)

Nu_VE = Nu0_val * Nu_ratio_weakVE(De_vals)
Sh_VE = Sh0_val * Sh_ratio_weakVE(De_vals)

pct_Nu = 100.0 * (Nu_VE - Nu0_val) / Nu0_val
pct_Sh = 100.0 * (Sh_VE - Sh0_val) / Sh0_val

# ---- Plots ----
plt.figure(figsize=(10,4), dpi=110)

plt.subplot(1,2,1)
plt.plot(De_vals, pct_Nu, lw=2)
plt.xlabel("De")
plt.ylabel("% increase in Nu")
plt.title(f"Heat transfer enhancement @ Re={Re}, Pr={Pr}")
plt.grid(True, alpha=0.3)

plt.subplot(1,2,2)
plt.plot(De_vals, pct_Sh, lw=2)
plt.xlabel("De")
plt.ylabel("% increase in Sh")
plt.title(f"Mass transfer enhancement @ Re={Re}, Sc={Sc}")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ---- Optional: surface vs (Re, De) to see combined effect ----
Re_vals = np.linspace(25, 300, 40)
De_vals2 = np.linspace(0.0, 0.6, 40)
RE, DE = np.meshgrid(Re_vals, De_vals2)

Nu0_grid = Nu0(RE, Pr)
Nu_ve_grid = Nu0_grid * Nu_ratio_weakVE(DE)
pct_grid = 100.0 * (Nu_ve_grid - Nu0_grid) / Nu0_grid

import matplotlib.ticker as mtick
plt.figure(figsize=(6,4), dpi=110)
cs = plt.contourf(RE, DE, pct_grid, levels=20)
plt.xlabel("Re")
plt.ylabel("De")
plt.title("% Nu enhancement surface")
cbar = plt.colorbar(cs)
cbar.formatter = mtick.PercentFormatter(decimals=0)
cbar.update_ticks()
plt.tight_layout()
plt.show()
