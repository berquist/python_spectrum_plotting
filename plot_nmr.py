#!/usr/bin/env python

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from numpy import nan


n_water = [1, 2, 3, 4, 5, 6, 7, 8, 9, 20]
water_dft = [5.63, 10.13, 11.56, 12.00, 11.87, 11.80, 12.28, 12.64, 13.07, 13.03]
water_pol_0 = [-1.19, -0.75, -0.36, -0.09, 0.13, 0.26, 0.25, 0.29, 0.31, -0.47]
water_pol_1 = [0.57, 0.75, 1.05, 1.32, 1.55, 1.66, 1.69, 1.78, 1.86, nan]
water_pol_4 = [0.57, 1.36, 1.85, 2.30, 2.52, 2.68, 2.75, 2.83, 2.94, nan]
water_pol_all = [0.57, 1.36, 1.85, 2.30, 2.69, 2.97, 3.18, 3.40, 3.60, nan]

n_chloro = [1, 2, 3, 4, 5, 6, 7, 8, 9]
chloro_dft = [0.02, 1.11, 0.92, 0.88, 1.02, 1.23, 1.28, 1.38, 1.58]
chloro_pol_0 = [-0.39, 0.10, 0.82, 1.19, 1.33, 1.36, 1.41, 1.41, 1.34]
chloro_pol_1 = [0.84, 1.24, 1.94, 2.31, 2.46, 2.47, 2.52, 2.53, 2.46]
chloro_pol_4 = [0.84, 1.44, 2.50, 3.01, 3.61, 3.62, 4.12, 4.02, 3.94]
chloro_pol_all = [0.84, 1.44, 2.50, 3.01, 3.89, 4.07, 4.29, 4.45, 4.47]

n_cycl = [1, 2, 3, 4]
cycl_dft = [-1.19, -1.53, -1.68, -1.63]
cycl_pol_0 = [0.63, 0.92, 1.08, 1.36]
cycl_pol_1 = [1.67, 1.98, 2.14, 2.09]
cycl_pol_all = [1.67, 1.56, 2.21, 2.72]

##########

fig, ax = plt.subplots()

ax.set_title('solvent: water')

ax.plot(n_water[:-1], water_dft[:-1], marker='o', label='shift')
ax.plot(n_water[:-1], water_pol_0[:-1], marker='x', label='RMSD from pol = 0')
ax.plot(n_water[:-1], water_pol_1[:-1], marker='x', label='RMSD from pol = 1')
ax.plot(n_water[:-1], water_pol_4[:-1], marker='x', label='RMSD from pol = 4')
ax.plot(n_water[:-1], water_pol_all[:-1], marker='x', label='RMSD from pol = all')

ax.set_xlabel('# solvent molecules')
ax.set_ylabel('')

ax.legend(loc='best', fancybox=True, framealpha=0.30)

fig.savefig('plot_nmr_water.pdf', bbox_inches='tight')

##########

fig, ax = plt.subplots()

ax.set_title('solvent: chloroform')

ax.plot(n_chloro, chloro_dft, marker='o', label='shift')
ax.plot(n_chloro, chloro_pol_0, marker='x', label='RMSD from pol = 0')
ax.plot(n_chloro, chloro_pol_1, marker='x', label='RMSD from pol = 1')
ax.plot(n_chloro, chloro_pol_4, marker='x', label='RMSD from pol = 4')
ax.plot(n_chloro, chloro_pol_all, marker='x', label='RMSD from pol = all')

ax.set_xlabel('# solvent molecules')

ax.legend(loc='best', fancybox=True, framealpha=0.30)

fig.savefig('plot_nmr_chloro.pdf', bbox_inches='tight')

##########

fig, ax = plt.subplots()

ax.set_title('solvent: cyclohexane')

ax.plot(n_cycl, cycl_dft, marker='o', label='shift')
ax.plot(n_cycl, cycl_pol_0, marker='x', label='RMSD from pol = 0')
ax.plot(n_cycl, cycl_pol_1, marker='x', label='RMSD from pol = 1')
ax.plot(n_cycl, cycl_pol_all, marker='x', label='RMSD from pol = all')

ax.set_xlabel('# solvent molecules')

ax.legend(loc='best', fancybox=True, framealpha=0.30)

fig.savefig('plot_nmr_cycl.pdf', bbox_inches='tight')

##########
