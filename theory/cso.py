#!/usr/bin/env python3
#
# cso dispersion
#
# @author Tobias Weber <tweber@ill.fr>
# @date 11-jun-2026
# @license see 'LICENSE' file
#
# - The original magnetic model for CSO and its parameters are from this paper:
#   https://doi.org/10.1103/PhysRevB.101.144411
#   (which is also available here: https://arxiv.org/abs/2002.06283)
# - The adapted settings and parameters are from this paper:
#   https://doi.org/10.1103/q77j-5g59
#

import lswt
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


num_Q_points = 512    # number of Q points to calculate
only_pos_E   = True   # hide magnon annihilation?
verbose      = False  # debug output
weight_scale = 8.


# exchange constants
J1, J2        = -0.601, -0.971
D1x, D1y, D1z = 0.618, 0.018, 0.107
D2x, D2y, D2z = 0.755, 0.234, 0.303

pos = 0.25


# magnetic sites
sites = [
	{ "S" : 1, "Sdir" : [ 0, 0, 1 ], "pos" : [ 1/2 - pos, 1/2 - pos, 1/2 - pos ] },
	{ "S" : 1, "Sdir" : [ 0, 0, 1 ], "pos" : [ 1 - pos,   pos,       1/2 + pos ] },
	{ "S" : 1, "Sdir" : [ 0, 0, 1 ], "pos" : [ pos,       1/2 + pos, 1 - pos ] },
	{ "S" : 1, "Sdir" : [ 0, 0, 1 ], "pos" : [ 1/2 + pos, 1 - pos,   pos ] }
]

# magnetic couplings
couplings = [
	{ "sites" : [ 1, 0 ], "dist" : [  1,  0,  0 ], "J" : J1, "DMI" : [  D1x,  D1y,  D1z ] },
	{ "sites" : [ 0, 1 ], "dist" : [ -1,  0, -1 ], "J" : J1, "DMI" : [ -D1x, -D1y,  D1z ] },
	{ "sites" : [ 3, 2 ], "dist" : [  0,  0,  0 ], "J" : J1, "DMI" : [ -D1x,  D1y, -D1z ] },
	{ "sites" : [ 2, 3 ], "dist" : [  0,  0,  1 ], "J" : J1, "DMI" : [  D1x, -D1y, -D1z ] },
	{ "sites" : [ 3, 0 ], "dist" : [  0,  1,  0 ], "J" : J1, "DMI" : [  D1z,  D1x,  D1y ] },
	{ "sites" : [ 0, 3 ], "dist" : [ -1, -1,  0 ], "J" : J1, "DMI" : [  D1z, -D1x, -D1y ] },
	{ "sites" : [ 2, 1 ], "dist" : [  0,  0,  0 ], "J" : J1, "DMI" : [ -D1z, -D1x,  D1y ] },
	{ "sites" : [ 1, 2 ], "dist" : [  1,  0,  0 ], "J" : J1, "DMI" : [ -D1z,  D1x, -D1y ] },
	{ "sites" : [ 2, 0 ], "dist" : [  0,  0,  1 ], "J" : J1, "DMI" : [  D1y,  D1z,  D1x ] },
	{ "sites" : [ 0, 2 ], "dist" : [  0, -1, -1 ], "J" : J1, "DMI" : [ -D1y,  D1z, -D1x ] },
	{ "sites" : [ 1, 3 ], "dist" : [  0,  0,  0 ], "J" : J1, "DMI" : [  D1y, -D1z, -D1x ] },
	{ "sites" : [ 3, 1 ], "dist" : [  0,  1,  0 ], "J" : J1, "DMI" : [ -D1y, -D1z,  D1x ] },
	{ "sites" : [ 1, 0 ], "dist" : [  0,  0,  1 ], "J" : J2, "DMI" : [  D2x,  D2y,  D2z ] },
	{ "sites" : [ 0, 1 ], "dist" : [  0,  0,  0 ], "J" : J2, "DMI" : [ -D2x, -D2y,  D2z ] },
	{ "sites" : [ 3, 2 ], "dist" : [  1,  0, -1 ], "J" : J2, "DMI" : [ -D2x,  D2y, -D2z ] },
	{ "sites" : [ 2, 3 ], "dist" : [ -1,  0,  0 ], "J" : J2, "DMI" : [  D2x, -D2y, -D2z ] },
	{ "sites" : [ 3, 0 ], "dist" : [  1,  0,  0 ], "J" : J2, "DMI" : [  D2z,  D2x,  D2y ] },
	{ "sites" : [ 0, 3 ], "dist" : [  0,  0,  0 ], "J" : J2, "DMI" : [  D2z, -D2x, -D2y ] },
	{ "sites" : [ 2, 1 ], "dist" : [ -1,  1,  0 ], "J" : J2, "DMI" : [ -D2z, -D2x,  D2y ] },
	{ "sites" : [ 1, 2 ], "dist" : [  0, -1,  0 ], "J" : J2, "DMI" : [ -D2z,  D2x, -D2y ] },
	{ "sites" : [ 2, 0 ], "dist" : [  0,  1,  0 ], "J" : J2, "DMI" : [  D2y,  D2z,  D2x ] },
	{ "sites" : [ 0, 2 ], "dist" : [  0,  0,  0 ], "J" : J2, "DMI" : [ -D2y,  D2z, -D2x ] },
	{ "sites" : [ 1, 3 ], "dist" : [  0, -1,  1 ], "J" : J2, "DMI" : [  D2y, -D2z, -D2x ] },
	{ "sites" : [ 3, 1 ], "dist" : [  0,  0, -1 ], "J" : J2, "DMI" : [ -D2y, -D2z,  D2x ] }
]

print("Calculating CSO dispersion...")
lswt.init(sites, couplings, verbose)

# plot a dispersion branch
qs, Es, ws = [], [], []
for q in np.linspace(0, 1, num_Q_points):
	try:
		Qvec = np.array([ q, 0.5, 0 ])
		#Qvec = np.array([ 0.5, 0.5, q ])
		for E, w in zip(*lswt.get_energies(Qvec, sites, couplings)):
			if only_pos_E and E < 0.:
				continue
			qs.append(q)
			Es.append(E)
			ws.append(w * weight_scale)
	except la.LinAlgError:
		pass

plt.plot()
plt.xlabel("q (rlu)")
plt.ylabel("E (meV)")
plt.scatter(qs, Es, marker = '.', s = ws, label = "CSO")


print("Plotting...")
plt.legend(loc = "upper right")
plt.tight_layout()
plt.show()
