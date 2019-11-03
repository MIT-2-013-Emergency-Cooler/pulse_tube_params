# Copyright 2019 2.013
# Jacob Miske
# !/usr/bin/python3

import cmd
import sys
import os
import getpass
from pyfiglet import Figlet


class PTR(cmd.Cmd):
    """A simple cmd application using cmd.
    """
    custom_fig = Figlet(font='slant')
    intro = 'Welcome to the PTR shell.  Type help or ? to list commands.\n'
    prompt = '> '
    file = None
    print(custom_fig.renderText('  Pulse Tube Params'))

    def do_status(self, arg):
        """Yields device status for the edge device being used.
        Returns a table of details related to health of unit.
        """
        def status():
            """Runs the list generation
            """
            custom_fig = Figlet(font='slant')
            print(custom_fig.renderText(' status'))
            print("You are running PTR Params Version 0.0.2 \n")
            print("Current Functionality: Enthalpy flow for CHX.")
        status()

    def do_whoami(self, arg):
        """Prints out user data specific to OS.
        """
        def whoami():
            print(getpass.getuser())
            print('File Directory')
            cwd = os.getcwd()  # Get the current working directory (cwd)
            files = os.listdir(cwd)  # Get all the files in that directory
            print("Files in '%s': %s" % (cwd, files))
        whoami()

    def do_run_sim(self, arg):
        """Begins prompts for sim engine, step by step process.
        """
        pass

    def do_PCM_calculator(self, arg):
        """Simple calculator for looking at how long a PCM material will last in supplied cooler conditions.
        """
        pass


    def do_bye(self, arg):
        """Stop cmd, close the window, and exit:  BYE
        """
        print("Thank you for using PTR Params")
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == "__main__":
    c = PTR()
    sys.exit(c.cmdloop())
