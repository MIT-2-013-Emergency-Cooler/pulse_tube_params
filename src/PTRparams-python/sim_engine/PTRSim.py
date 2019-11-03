# Copyright 2019 2.013
# Jacob Miske
# !/usr/bin/python3

import cmd
import sys
import os
import getpass
from pyfiglet import Figlet
import matplotlib.pyplot as plt
from .PTRParams import PTRParams

class PTRSim:
    """
    Class for functions related to modelling cooler.
    """

    def __init__(self):
        # TODO: these self params are not used, just thinking for now.
        self.internal_temp = 4      # [C]
        self.external_temp = 25     # [C]
        self.thermal_cond = 10      # [W/(m*C)]
        self.cooler_area = 1        # [m^2]
        self.wall_thick = 0.01      # [m]
        self.sim_time = 10         # [s]

    def __main__(self):
        pass

    def get_sim_params(self):
        """
        Asks user questions in CoolerParams class.
        :return:
        """
        cooler_params = CoolerParams()
        cooler_q_ans = cooler_params.get_cooler_params()
        return cooler_q_ans


    def get_heat_transfer_rate(self, k, temp_in, temp_out, thickness):
        """
        Calculates the following functions:
        q = - k dT/dx
        for heat transfer rate from the cooler given parameters
        :return: q
        """
        return -k * (temp_in - temp_out)/thickness

    def get_heat_flux(self, q, area):
        """
        Calculates the following functions:
        Q = qA
        for heat flux from the cooler given parameters
        :return: Q
        """
        return q*area

    def run_simulation(self, cooler_ans):
        """
        Considers set params, finds temperature profiles, and plots them over a time.
        Determines energy needed to run the cooler and cool object inside of it.
        Uses thermal resistance model.
        :param cooler_answers: Returned from the CoolerParams object with a
        set of responses for the geometry and constants of the problem.
        :return:
        """
        print(cooler_ans)

        def get_thermal_resistance(cooler_answers):
            """
            From the sim params, find the thermal resistances across the system.
            There is a long series system, with a parallel radiative and convective ends.

            :return: list of 7 different thermal resistances. [rad_in, conv_in, in, wall, out, rad_out, conv_out]
            """

            length_inner = cooler_answers[7]                         # Length of inner cube's walls [m]
            length_wall = cooler_answers[9]                          # Length of cube's walls [m]
            length_outer = cooler_answers[11]                        # Length of outer cube's walls [m]
            area_inner = (cooler_answers[0]) ** (2 / 3)              # Area of inner cube's surface [m^2]
            area_wall = (length_inner + 2 * cooler_answers[7]) ** 2  # Area of cube wall's surface [m^2]
            area_outer = (length_wall + 2 * cooler_answers[9]) ** 2  # Area of outer cube's surface [m^2]
            # TODO: Fix radiative losses beyond simple model
            rad_in = 10*cooler_answers[6]                       # resistance from internal radiative loss [deg C/W]
            conv_in = 1 / (cooler_answers[5] * 6 * area_inner)  # resistance from internal convective loss [deg C/W]
            cond_in = length_inner / (cooler_answers[8] * area_inner)    # R inner surface conduction [deg C/W]
            cond_wall = length_wall / (cooler_answers[10] * area_wall)   # R wall conduction [deg C/W]
            cond_out = length_outer / (cooler_answers[12] * area_outer)  # R outer surface conduction [deg C/W]
            rad_out = 8*cooler_answers[14]                      # resistance from external radiative loss [deg C/W]
            conv_out = 1 / (cooler_answers[13] * area_outer)    # resistance from external convective loss [deg C/W]
            list_resistances = [rad_in, conv_in, cond_in, cond_wall, cond_out, rad_out, conv_out]
            return list_resistances

        def run_sim_plot(c_as, res, inner_temp, outer_temp):
            """
            First, find total heat transfer rate from the equivalent resistance and temperature difference.
            Second, use piecewise thermal resistances to find temperature at each node.
            Third, plot T(x) from inside cooler to ambient air.
            :param c_as: cooler_answers from the cooler params class
            :param res: list of resistances from get_thermal_resistances
            :param inner_temp:
            :param outer_temp:
            :return:
            """
            R_eq = res[2] + res[3] + res[4] + (1/res[0] + 1/res[1])**(-1) + (1/res[5] + 1/res[6])**(-1)
            Q_total = (outer_temp - inner_temp)/R_eq
            cooler_width = ((c_as[0])**(1/3))/2
            x_distances = [0,
                           cooler_width,
                           cooler_width+c_as[7],
                           cooler_width+c_as[7]+c_as[9],
                           cooler_width+c_as[7]+c_as[9]+c_as[11],
                           cooler_width+c_as[7]+c_as[9]+c_as[11]+1]    # distance from cooler center[m]
            y_temperatures = [0,0,0,0,0,0]
            y_temperatures[0] = outer_temp - Q_total * ((1/res[5] + 1/res[6])**(-1) + res[4] + res[3] + res[2] + (1/res[0] + 1/res[1])**(-1))
            y_temperatures[1] = outer_temp - Q_total * ((1/res[5] + 1/res[6])**(-1) + res[4] + res[3] + res[2])
            y_temperatures[2] = outer_temp - Q_total * ((1/res[5] + 1/res[6])**(-1) + res[4] + res[3])
            y_temperatures[3] = outer_temp - Q_total * ((1/res[5] + 1/res[6])**(-1) + res[4])
            y_temperatures[4] = outer_temp - Q_total * (1/res[5] + 1/res[6])**(-1)
            y_temperatures[5] = outer_temp
            # Plotting with matplotlib
            plt.figure(1)
            plt.plot(x_distances, y_temperatures)
            plt.xlabel("Distance from center of cooler [m]")
            plt.ylabel("Temperature at point [degrees C]")
            plt.title("Fourier's Law Analysis of Thermal Leakage Temperatures")
            plt.savefig("sim_plot.png")
            plt.show()
            # Print some important numbers
            print("The following quantities describe the analysis: \n")
            print("The inner, cooler temperature used was {} degrees C. \n".format(inner_temp))
            print("The outer, ambient temperature used was {} degrees C. \n".format(outer_temp))
            print("The thermal leakage was measured as {} W. \n".format(Q_total))
            print("The thermal resistance was measured as {} C/W. \n".format(R_eq))

        therm_rads = get_thermal_resistance(cooler_ans)
        print(therm_rads)
        run_sim_plot(cooler_ans, therm_rads, 5, 43)
