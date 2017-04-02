import sys
# Check for numpy and matplotlib, try to exit gracefully if not found
import imp
try:
    imp.find_module('numpy')
    foundnp = True
except ImportError:
    foundnp = False
try:
    imp.find_module('matplotlib')
    foundplot = True
except ImportError:
    foundplot = False
if not foundnp:
    print("Numpy is required. Exiting")
    sys.exit()
if not foundplot:
    print("Matplotlib is required. Exiting")
    sys.exit()
import numpy as np
import matplotlib.pyplot as plt

# Adjust the following three variables to change which area of the spectrum is plotted and number of points used
# in plotting the curves
start=200
finish=380
points=300

# A sqrt(2) * standard deviation of 0.4 eV is 3099.6 nm. 0.1 eV is 12398.4 nm. 0.2 eV is 6199.2 nm.
stdev = 12398.4
# For Lorentzians, gamma is half bandwidth at half peak height (nm)
gamma = 12.5
# Excitation energies in nm
bands = [330,328,328,308,290,290,288,283,276,270,268]
# Oscillator strengths (dimensionless)
f = [7.90e-7,0.00,7.16e-4,1.02e-2,1.38e-6,2.94e-7,0.00,8.86e-4,1.54e-5,1.25e-2,9.31e-3]

# Basic check that we have the same number of bands and oscillator strengths
if len(bands) != len(f):
    print('Number of bands does not match the number of oscillator strengths.')
    sys.exit()

# Information on producing spectral curves (Gaussian and Lorentzian) is adapted from:
# P. J. Stephens, N. Harada, Chirality 22, 229 (2010).
# Gaussian curves are often a better fit for UV/Vis.
def gaussBand(x, band, strength, stdev):
    "Produces a Gaussian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev))  * np.exp(-(((1.0/x)-(1.0/band))/(1.0/stdev))**2)
    return bandshape

def lorentzBand(x, band, strength, stdev, gamma):
    "Produces a Lorentzian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev)) * ((gamma**2)/((x - band)**2 + gamma**2))
    return bandshape 

x = np.linspace(start,finish,points)

composite = 0
for count,peak in enumerate(bands):
    thispeak = gaussBand(x, peak, f[count], stdev)
#    thispeak = lorentzBand(x, peak, f[count], stdev, gamma)
    composite += thispeak

fig, ax = plt.subplots()
ax.plot(x,composite)
plt.xlabel('$\lambda$ / nm')
plt.ylabel('$\epsilon$ / L mol$^{-1}$ cm$^{-1}$')

plt.show()
