#!/usr/bin/env python3
"""
SOF viscoelastic heat/mass transfer in simple shear (Subramanian & Koch, 2007).
Generates Nu (or Sh) vs Pe for multiple De and epsilon values and saves figures.

Run:
    python sof_viscoelastic_ht_mt.py
"""

import numpy as np
import matplotlib.pyplot as plt

def Nu_simple_shear(Pe, De, eps):
    """
    Nusselt (or Sherwood) number in weakly viscoelastic simple shear flow (Ganesh Subramanian & Koch, 2007, eq. 35).
    Parameters
    ----------
    Pe : array-like
        Péclet number
    De : float
        Deborah number (small, De << 1)
    eps : float or array-like
        Ratio psi2/psi1
    Returns
    -------
    Nu : array-like
        Nusselt (or Sherwood) number
    Notes
    -----
    Valid in the asymptotic limit: Pe*De >> 1 and De << 1 (weak elasticity but strong elastic-convective effect).
    """
    Pe = np.asarray(Pe, dtype=float)
    eps = np.asarray(eps, dtype=float)
    if np.any(np.isclose(1 + eps, 0.0)):
        raise ValueError("Some ε values are too close to -1; the correlation becomes singular.")
    factor = ((0.5 + eps) / (1 + eps)) ** (1/3)
    return 0.478 * ((Pe * De) ** (1/3)) * factor

def main():
    # Parameters
    Pe = np.logspace(-2, 3, 300)
    De_values = [0.01, 0.05, 0.1, 0.2]
    eps_values = [-0.9, -0.7, -0.5, -0.3, -0.1]

    # Figure 1–4: Nu vs Pe at different De
    for De in De_values:
        plt.figure(figsize=(6,4))
        for eps in eps_values:
            Nu = Nu_simple_shear(Pe, De, eps)
            plt.loglog(Pe, Nu, label=f"ε={eps:+.1f}")
        plt.title(f"Nusselt (or Sherwood) vs Péclet, De={De}")
        plt.xlabel("Péclet number (Pe)")
        plt.ylabel("Nu (or Sh)")
        plt.grid(True, which="both", ls=":")
        plt.legend()
        plt.savefig(f"nu_vs_pe_De_{str(De).replace('.','p')}.png", dpi=200, bbox_inches="tight")
        plt.close()

    # Figure 5: Relative Nu vs epsilon at a fixed Pe
    Pe_fixed = 10.0
    eps_sweep = np.linspace(-0.95, -0.05, 200)
    plt.figure(figsize=(6,4))
    for De in De_values:
        Nu_vals = Nu_simple_shear(Pe_fixed, De, eps_sweep)
        Nu_ref = Nu_simple_shear(Pe_fixed, De, -0.5)
        plt.plot(eps_sweep, Nu_vals/Nu_ref, label=f"De={De}")
    plt.title(f"Relative Nu (normalized by ε=-0.5) at Pe={Pe_fixed}")
    plt.xlabel("ε = ψ₂/ψ₁")
    plt.ylabel("Nu / Nu(ε=-0.5)")
    plt.grid(True, ls=":")
    plt.legend()
    plt.savefig("relative_nu_vs_eps.png", dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved figures:")
    print("  nu_vs_pe_De_*.png")
    print("  relative_nu_vs_eps.png")

if __name__ == "__main__":
    main()
