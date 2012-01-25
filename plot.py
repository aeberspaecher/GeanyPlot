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

import matplotlib
matplotlib.use('GTKAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar


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
        # remove canvas? figure? anything else?

    def on_plot_item_clicked(widget, data):
        """Open dialogs that allow the user the select which columns to plot.
        Then, load and plot the data.
        """

        fileName = geany.document.get_current().file_name

        # figure out which columns to use:
        xCol = geany.dialogs.show_input_numeric("Select columns to plot", "x values", 1, 1, 10, 1)
        yCol = geany.dialogs.show_input_numeric("Select columns to plot", "y values", 2, 1, 10, 1)
        xCol, yCol = int(xCol)-1, int(yCol)-1 # use Python counting!

        try:
            x, y = np.loadtxt(fileName, usecols=(xCol, yCol), unpack=True)
        except:
            geany.dialogs.show_msgbox("Loading data failed!")
            return

        # create a new window
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.connect("destroy", lambda x: gtk.main_quit())
        win.set_default_size(600,450)
        win.set_title("GeanyPlot")

        vbox = gtk.VBox()
        win.add(vbox)

        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        vbox.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, win)
        vbox.pack_start(toolbar, False, False)
        
        win.show_all()
        gtk.main()
