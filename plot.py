#!/usr/bin/env python
#-*- coding:utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

# Copyright 2012 Alexander Eberspächer <alex.eberspaecher@googlemail.com>

"""A Geany plugin for data visualization written in Python.

The plugin is supposed to be used for quick data inspection without the need
to run a Python session just for the purpose of visualization. The plugin uses
Matplotlib and the Geany's Python bindings available from
https://github.com/codebrainz/geanypy
"""

import matplotlib
matplotlib.use('GTKAgg')

import gtk
import geany
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as\
    NavigationToolbar
import itertools


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

        # define cyclers for plot properties (redefine on function entry such
        # that the plots look the same each time the function is called):
        markers = itertools.cycle(["x", "o", "s"])
        linestyles = itertools.cycle(["-", "--"])
        colors = itertools.cycle(["blue", "red", "#014421", "#FF00FF", "gray"])
        # blue, red, forest-green, magenta, gray

        fileName = geany.document.get_current().file_name

        # TODO: use a better/more suitable GTK dialogue
        useLinePlot = geany.dialogs.show_question(
            "Create a line plot (scatter plot otherwise)?")

        # figure out which columns to use:
        xCol = geany.dialogs.show_input_numeric("Select column to plot as x-values",
                                                "x values", 1, 1, 10, 1)
        xCol = int(xCol) - 1 # Python couting

        # load data:
        try:
            x = np.loadtxt(fileName, usecols=[xCol], unpack=True)
        except:
            geany.dialogs.show_msgbox("Loading x data failed!")
            return
        
        addMoreY = True
        yCols = []
        colSuggestion = 2
        yData = []
        
        while(addMoreY):
            yColNew = geany.dialogs.show_input_numeric("Select columns to plot",
                                                       "y values", colSuggestion,
                                                       1, 10, 1)
            # load data:
            try:
                newY = np.loadtxt(fileName, usecols=[int(yColNew)-1])
            except:
                geany.dialogs.show_msgbox("Loading y data from column %s failed!"\
                                          %yColNew)
                return

            yData.append(newY)

            colSuggestion += 1

            # add more y-data?            
            addMoreY = geany.dialogs.show_question("Add more y values?")

        # create a new window
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.connect("destroy", lambda x: gtk.main_quit())
        win.set_default_size(600, 450)
        win.set_title("GeanyPlot")

        vbox = gtk.VBox()
        win.add(vbox)

        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)

        if(useLinePlot):
            for y in yData:
                ax.plot(x, y, color=colors.next(), ls=linestyles.next(), lw=2)
        else:
            for y in yData:
                ax.plot(x, y, ls="", marker=markers.next(),
                        markeredgewidth=1, markeredgecolor=colors.next(),
                        markerfacecolor="None", ms=5)

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        vbox.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, win)
        vbox.pack_start(toolbar, False, False)
        
        win.show_all()
        gtk.main()
