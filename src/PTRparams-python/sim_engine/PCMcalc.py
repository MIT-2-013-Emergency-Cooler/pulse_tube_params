# Copyright 2019 2.013
# Jacob Miske
# !/usr/bin/python3

import cmd
import sys
import os
import getpass
from pyfiglet import Figlet
import matplotlib.pyplot as plt
from .PTRParams import CoolerParams

class PCMcalc:
    """
    Class for functions related to modelling various PCM materials.
    """

    def __init__(self):
        # TODO: these self params are not used, just thinking for now.
        self.internal_temp = 5      # [C]
        self.external_temp = 43     # [C]

    def __main__(self):
        pass

    def get_pcm_params(self):
        """

        :return:
        """
        return 0

    def run_simulation(self, pcm_answers):
        """

        :return:
        """
        pass
