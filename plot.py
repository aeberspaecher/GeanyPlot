#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""A Geany plugin for data visualization written in Python.

The plugin is supposed to be used for quick data inspection without the need
to run a Python session just for the purpose of visualization. The plugin uses
Matplotlib.
"""

import gtk
import geany
import numpy as np
import matplotlib.pyplot as plt

class GeanyPlot(geany.Plugin):

    __plugin_name__ = "GeanyPlot"
    __plugin_version__ = "0.01"
    __plugin_description__ = "Plot numerical data stored in textfiles using Matplotlib."
    __plugin_author__ = "Alexander Eberspächer <alex.eberspaecher@googlemail.com>"

    def __init__(self):
        self.menu_item = gtk.MenuItem("Plot data")
        self.menu_item.show()
        geany.main_widgets.tools_menu.append(self.menu_item)
        self.menu_item.connect("activate", self.on_plot_item_clicked)

    def cleanup(self):
        self.menu_item.destroy()

    def on_plot_item_clicked(widget, data):
        # load data TODO: support more than two columns and more than one dataset
        fileName = geany.document.get_current().file_name
        x, y = np.loadtxt(fileName, usecols=(0,1), unpack=True)
        plt.plot(x, y)
        plt.show()
