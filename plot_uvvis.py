"""Adapted from J. Grant Hill's PlotBand script, http://www.grant-hill.group.shef.ac.uk/plot-uv.html"""

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


# Information on producing spectral curves (Gaussian and Lorentzian)
# is adapted from:
# P. J. Stephens, N. Harada, Chirality 22, 229 (2010).
# Gaussian curves are often a better fit for UV/Vis.
def gaussBand(x, band, strength, stdev):
    "Produces a Gaussian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev)) * np.exp(-(((1.0/x)-(1.0/band))/(1.0/stdev))**2)
    return bandshape

def lorentzBand(x, band, strength, stdev, gamma):
    "Produces a Lorentzian curve"
    bandshape = 1.3062974e8 * (strength / (1e7/stdev)) * ((gamma**2)/((x - band)**2 + gamma**2))
    return bandshape


def spectra(etenergies, etoscs, low=0.5, high=10.0, resolution=0.01, smear=0.04):
    """Return arrays of the energies and intensities of a Lorentzian-blurred spectrum"""

    maxSlices = int((high - low) / resolution) + 1
    peaks = len(etenergies)

    spectraEV = []
    spectraNM = []
    spectraIntensity = []

    # eV = wavenumbers * 1.23981e-4
    # nm = 1.0e7 / wavenumbers

    for i in range(0, maxSlices):
        # in eV
        energy = float(i * resolution + low)
        wavenumber = energy / 1.23981e-4
        intensity = 0.0
        for trans in range(0, len(etenergies)):
            this_smear = smear / 0.2 * (-0.046 * etoscs[trans] + 0.20)
            # print this_smear
            deltaE = etenergies[trans] * 1.23981e-4 - energy
            intensity = intensity + etoscs[trans] * this_smear**2 / (deltaE**2 + this_smear**2)

        spectraEV.append(energy)
        spectraNM.append(float(1.0e7 / wavenumber))
        spectraIntensity.append(intensity)

    return spectraEV, spectraNM, spectraIntensity


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('bandtype', choices=('gaussian', 'lorentzian'), help='')
    parser.add_argument('plottype', choices=('jghill', 'ghutchis'), help='')
    parser.add_argument('--pdf-prefix', type=str, default='plot', help='')
    parser.add_argument('--stems', action='store_true', help='')
    parser.add_argument('--units-input')
    parser.add_argument('--units-output')
    args = parser.parse_args()

    # Adjust the following three variables to change which area of the
    # spectrum is plotted and number of points used in plotting the
    # curves
    start = 200
    finish = 380
    points = 300

    # A sqrt(2) * standard deviation of 0.4 eV is 3099.6 nm. 0.1 eV is
    # 12398.4 nm. 0.2 eV is 6199.2 nm.
    stdev = 12398.4
    # For Lorentzians, gamma is half bandwidth at half peak height
    # (nm)
    gamma = 12.5
    # Excitation energies in nm
    bands = [330, 328, 328, 308, 290, 290, 288, 283, 276, 270, 268]
    # Oscillator strengths (dimensionless)
    f = [7.90e-7, 0.00, 7.16e-4, 1.02e-2, 1.38e-6, 2.94e-7, 0.00, 8.86e-4, 1.54e-5, 1.25e-2, 9.31e-3]

    # Basic check that we have the same number of bands and oscillator
    # strengths
    if len(bands) != len(f):
        print('Number of bands does not match the number of oscillator strengths.')
        sys.exit()


    if args.plottype == 'jghill':

        x = np.linspace(start, finish, points)

        composite = 0
        for count, peak in enumerate(bands):
            if args.bandtype == 'gaussian':
                thispeak = gaussBand(x, peak, f[count], stdev)
            elif args.bandtype == 'lorentzian':
                thispeak = lorentzBand(x, peak, f[count], stdev, gamma)
            else:
                sys.exit()
            composite += thispeak


        fig, ax = plt.subplots()

        ax.plot(x, composite)

        if args.stems:
            ax.stem(bands, f, markerfmt='.')

        plt.xlabel('$\lambda$ / nm')
        plt.ylabel('$\epsilon$ / L mol$^{-1}$ cm$^{-1}$')

    elif args.plottype == 'ghutchis':

        spectraEV, spectraNM, spectraIntensity = spectra(bands, f)

        fig, ax = plt.subplots()

        ax.plot(spectraNM, spectraIntensity)

    else:
        sys.exit()

    fig.savefig('{}.pdf'.format(args.pdf_prefix), bbox_inches='tight')
