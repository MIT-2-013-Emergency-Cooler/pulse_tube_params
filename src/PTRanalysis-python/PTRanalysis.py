'''Pulse
Tube
Refrigerator
Analysis
# First
developed
by: Alisha
Schor, alisha.schor @ gmail.com
Used
from DSpace
# Further
Developed
by
Jacob
Miske
for 2.013 PTR 2019-2020
Define
geometric
parameters
# All
units
SI(kg - m - s)
TODO: input
based
calculations
'''

import numpy as np
import matplotlib.pyplot as plt
from pyfiglet import Figlet

# convert metric
TOSI = 0.0254
pi = 3.141592653

## # Dimensions
# Swept
#Volume(cylinder)
dswept = 1.364 * TOSI
lswept = 0.1
f = 60 # Hz
Aswept = pi * dswept ** 2 / 4
w = 2 * pi * f
# Aftercooler(first HEX)
do = 0.811 * TOSI
lo = 0.7 * TOSI
Ao = pi * do ** 2 / 4
Vo = Ao * lo
# Regenerator
dr = 1.364 * TOSI
lr = 6 * TOSI
Ar = pi * dr ** 2 / 4
Vr = Ar * lr
# ColdHEX
dc = 0.811 * TOSI
lc = 0.7 * TOSI
Ac = pi * dc ** 2 / 4
Vc = Ac * lc
# PulseTube
dpt = 0.81 * TOSI
lpt = 6 * TOSI
Apt = pi * dpt ** 2 / 4
Vpt = Apt * lpt
# WarmHEX
dh = 0.811 * TOSI
lh = 0.7 * TOSI
Ah = pi * dh ** 2 / 4
Vh = Ah * lh
# Choose temperatures
Tc = 200 # K
Th = 300 # K
Tr = (Th - Tc) / np.log(Th / Tc)
# NOTE: Either properties of air or properties
# of nitrogen must be commented prior to running
# this file, only one set of working fluid
# params is used

# # Material Properties

# TODO: have users input Air, N, CH4, or He and re - evalaute model for each

# Properties of air
# R = 287 # J / kg - K
# rhoo = 1.229 # kg / m - 3
# gamma = 1.4
# Patm = 1.1Oe5 # Pa
# mu = 1.5e-5 # Pa - s
# cp = 1003 # J / kg - K
# kair = 0.02544 # W / m - K
# nu = 1.475e-5 # m ** 2 / s

# Properties of nitrogen
R = 290 # J / kg - K
rhoo = 1.116 # kg / m ** 3
gamma = 1.4 # Non - dimensional
Patm = 1.01e5 # Pa
mu = 1.8042e-5 # Pa - s
cp = 1041.4 # J / kg - K
kair = 0.02607 # W / m - K
nu = 1.6231 - 5 # m ^ 2 / s

# Properties of Helium
#R = 2077 # J / kg - K
#rhoo = 0.2501 # kg / m ^ 3 at - 80 C
#gamma = 1.4 # Non - dimensional
#Patm = 1.01e5 # Pa
#mu = 1.96e-5 # Pa - s
#cp = 5188 # J / kg - K
#kair = 0.149 # W / m - K
#nu = 1.87 - 5 # m ^ 2 / s

# Properties of copper
ccu = 385 # J / kg - K
kcu = 385 # W / m - K
rhocu = 8960 # kg / m ^ 3

# Chosen properties for init pressure and k(orifice flow rate)
Po = Patm
Va = Aswept * lswept
k = np.linspace(2, 15, num=52) # matlab linspace 2:0.25:15
k = 10 ** (-k) # log scale

# Time vector
t = np.linspace(0, 2, num=400) # matlab linspace 0:0.005:2
# Correlation coefficients
a = []
b = []
c = []
for j in range(len(k)):
    a.append(R * Th / Po * (Vh / (R * Th) + (k[j] * rhoo / (1j * w))) )

    b.append( a[j] + Vpt / (gamma * Po) + Vh / (rhoo * R * Th) - 1 / rhoo * (Vh / (R * Th) + (k[j] * rhoo / (1j * w)) + k[j] / (1j * w)) )

    c.append( R * Th / Po * (Vo / (R * Th) + Vr / (R * Th) + Vc / (R * Tc) + b[j] * Po / (R * Tc) - b[j] * rhoo + a[j] * rhoo + rhoo * Vpt / (gamma * Po) + Vh / (R * Th) - a[j] * Po / (R * Th) + k[j] * rhoo / (1j * w)) )


phase = np.angle(c) * 180 / pi
MagC = [abs(i) for i in c]

# # Calculate work and cooling power by choosing either
# pressure or volume amplitude.
# Pa = Va. / MagC or Va = Pa. * MagC
Pa = [Va / MagC[i] for i in range(len(MagC))]
Work = [0.5 * Pa[i] * Va * np.sin(np.angle(c)) * f for i in range(len(Pa))]
DV3 = [Pa[i] * abs(b[i]) for i in range(len(Pa))]
Qc = [abs(-0.5 * Pa[i] * DV3[i] * np.sin(np.angle(b[i])) * f + 1j * w / (R * Tc) * (Pa[i] * Vc + DV3[i] * Po)) for i in range(len(Pa))]

MaxWork = [max(-Work[i]) for i in range(len(Work))]
MaxCooling = max(Qc)
for g in range(len(Work)):
    if Qc[g] == MaxCooling:
        OptimumK = k[g]
        OptimumPhase = np.angle(c[g]) * 180 / pi
        MassFlow = OptimumK * rhoo * Pa[g]
        VolFlow = OptimumK * Pa[g]


def get_plot_outputs(k, phase, Work, Qc):
    """
    Plots the phase, work, qc relations to k
    :param k: Valve state
    :param phase: Phase shift state
    :param Work: Input Work
    :param Qc: Output Cooling Power
    :return:
    """
    # Plot outputs
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.semilogx(k, phase)
    plt.xlabel('k')
    plt.ylabel('Phase (deg)')
    plt.title("P-T Phase Shift and Cooling Power")
    plt.xlim([1e-10, 1e-5])
    plt.subplot(2, 1, 2)
    plt.semilogx(k, Work)
    plt.semilogx(k, Qc)
    plt.legend(['Work', 'Qc'])
    plt.xlabel('k')
    plt.ylabel('Cooling Power (W)')
    plt.xlim([1e-10, 1e-5])


    # PhaseShift
    plt.figure(2)
    plt.semilogx(k, phase)
    plt.xlabel('k')
    plt.ylabel('Phase (deg)')
    plt.title("P-T Phase Shift")
    plt.xlim([1e-10, 1e-5])
    plt.show()

    # Cooling Power
    plt.figure(3)
    plt.semilogx(k, Work)
    plt.semilogx(k, Qc)
    plt.legend(['Work', 'Qc'])
    plt.xlabel('k')
    plt.ylabel('Cooling Power (W)')
    plt.xlim([1e-10, 1e-5])
    plt.title("Cooling Power Ratio f(k)")
    plt.show()

def get_valve_sizing():
    # # Valve sizing and Cv
    # Based on Swagelok & Parker references
    Q = [OptimumK * Pa[i] * 2118.88 for i in range(len(Pa))] # CFM
    P1 = [(Po + Pa[i] / 2) * 0.0001450377 for i in range(len(Pa))] # PSIA
    P2 = Po * 0.0001450377 # PSIA
    # SG = I # air
    SG = 0.967 # nitrogen
    T = (Th - 273.15) * 9 / 5 + 32 + 460 # "Absolute Temperature"
    T = 180
    Cv = [Q[i] / 16.05 * np.sqrt(SG * T / (P1[i] ** 2 - P2 ** 2)) for i in range(len(Q))]

    # Required nozzle size based on mass flow rate
    Pup = 60 # upstream pressure in psi
    Pup = Pup * 6894.757 # upstream pressure in Pa
    Anoz = MassFlow / (gamma ** .5) * (2 / (gamma + 1)) ** (-(gamma + 1) / (2 * gamma - 1)) * np.sqrt(R * Th) / (Pup)
    Dnoz = np.sqrt(4 / pi * Anoz)

if __name__ == '__main__':
    get_plot_outputs(k, phase, Work, Qc)
