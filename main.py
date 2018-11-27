from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.layouts import widgetbox, row, column
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, DaysTicker, FuncTickFormatter, Range1d
from bokeh.models.widgets import CheckboxGroup
from bokeh.palettes import Viridis as palette
from bokeh.plotting import figure
from bokeh.server.server import Server


import itertools
import numpy as np
import os
import pandas as pd


s
data = pd.read_excel(os.path.join(__file__, "data\52-SD002_cleaned.xlsx"))


def datetime(x):
    return np.array(x, dtype=np.datetime64)
    

def make_dataset(measurement_list):
    
    # Define data source dict
    d = dict(date=data["DateTime"])
    for meas in measurement_list:
        d[meas] = data[meas]
            
    return ColumnDataSource(data=d)


def make_power_plot(src):
      
    # Setup plot
    p = figure(plot_width=800,
               plot_height=300,
               title="Power",
               x_axis_type='datetime',
               toolbar_location="right",
               tools="pan,wheel_zoom,box_zoom,reset")
    
    # Color
    colors = palette[4]
    
    # Configure hover tool      
    hovertool = HoverTool(
                        tooltips=[
                                    ( 'Date',   '@date{%d-%b-%Y %H:%M}'            ),
                                    ( 'P',   '@{P[W]} W' ), # use @{ } for field names with spaces
                                    ( 'P1',  '@{P1[W]} W' ), # use @{ } for field names with spaces
                                    ( 'P2',  '@{P2[W]} W' ), # use @{ } for field names with spaces
                                    ( 'P3',  '@{P3[W]} W' ), # use @{ } for field names with spaces
                                 ],

                        formatters={
                                    'date'  : 'datetime', # use 'datetime' formatter for 'date' field
                                    'P[W]'  : 'printf',   # use 'printf' formatter for 'adj close' field
                                    'P1[W]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                    'P2[W]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                    'P3[W]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                                      # use default 'numeral' formatter for other fields
                                    },

                        # display a tooltip whenever the cursor is vertically in line with a glyph
                        mode='vline',
                        )

    # Configure axes
    # - x -
    p.xaxis.ticker = DaysTicker(days=np.arange(0, len(data["DateTime"])))
    p.xaxis.major_label_orientation = 1
    p.xaxis.formatter=DatetimeTickFormatter(
                                            hours=["%d %b %Y"],
                                            days=["%d %b %Y"],
                                            months=["%d %b %Y"],
                                            years=["%d %b %Y"],
                                            )

    # - y -
    p.yaxis.axis_label = "Power in W"

    # Add plots
    l0 = p.line("date", "P[W]", source=src, line_color=colors[0], legend="Total")
    l1 = p.line("date", "P1[W]", source=src, line_color=colors[1], legend="Phase 1")
    l2 = p.line("date", "P2[W]", source=src, line_color=colors[2], legend="Phase 2")
    l3 = p.line("date", "P3[W]", source=src, line_color=colors[3], legend="Phase 3")
    
    # Add hovertool
    hovertool.renderers = [l1]
    p.add_tools(hovertool)
    
    # Legend
    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    return p, l0, l1, l2, l3


def make_current_plot(src):
      
    # Setup plot
    p = figure(plot_width=800,
               plot_height=300,
               title="Current",
               x_axis_type='datetime',
               toolbar_location="right",
               tools="pan,wheel_zoom,box_zoom,reset")
    
    # Color
    colors = palette[4]
    
    # Configure hover tool
    hovertool = HoverTool(
                        tooltips=[
                                    ( 'Date',   '@date{%d-%b-%Y %H:%M}'            ),
                                    ( 'I1',  '@{A1[A]} A' ), # use @{ } for field names with spaces
                                    ( 'I2',  '@{A2[A]} A' ), # use @{ } for field names with spaces
                                    ( 'I3',  '@{A3[A]} A' ), # use @{ } for field names with spaces
                                 ],

                        formatters={
                                    'date'  : 'datetime', # use 'datetime' formatter for 'date' field
                                    'A1[A]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                    'A2[A]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                    'A3[A]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                                      # use default 'numeral' formatter for other fields
                                    },

                        # display a tooltip whenever the cursor is vertically in line with a glyph
                        mode='vline',
                        )

    # Configure axes
    # - x -
    p.xaxis.ticker = DaysTicker(days=np.arange(0, len(data["DateTime"])))
    p.xaxis.major_label_orientation = 1
    p.xaxis.formatter=DatetimeTickFormatter(
                                            hours=["%d %b %Y"],
                                            days=["%d %b %Y"],
                                            months=["%d %b %Y"],
                                            years=["%d %b %Y"],
                                            )

    # - y -
    p.yaxis.axis_label = "Current in A"

    # Add plots
    l1 = p.line("date", "A1[A]", source=src, line_color=colors[1], legend="Phase 1")
    l2 = p.line("date", "A2[A]", source=src, line_color=colors[2], legend="Phase 2")
    l3 = p.line("date", "A3[A]", source=src, line_color=colors[3], legend="Phase 3")
    
    # Add hovertool
    hovertool.renderers = [l1]
    p.add_tools(hovertool)
    
    # Legend
    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    return p, l1, l2, l3


def make_voltage_plot(src):
      
    # Setup plot
    p = figure(plot_width=800,
               plot_height=300,
               title="Voltage",
               x_axis_type='datetime',
               toolbar_location="right",
               tools="pan,wheel_zoom,box_zoom,reset")
    
    # Color
    colors = palette[4]   
    
    # Configure hover tool
    hovertool = HoverTool(
                            tooltips=[
                                        ( 'Date',   '@date{%d-%b-%Y %H:%M}'            ),
                                        ( 'U1',  '@{V1[V]} V' ), # use @{ } for field names with spaces
                                        ( 'U2',  '@{V2[V]} V' ), # use @{ } for field names with spaces
                                        ( 'U3',  '@{V3[V]} V' ), # use @{ } for field names with spaces
                                     ],

                            formatters={
                                        'date'  : 'datetime', # use 'datetime' formatter for 'date' field
                                        'V1[V]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                        'V2[V]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                        'V3[V]' : 'printf',   # use 'printf' formatter for 'adj close' field
                                                          # use default 'numeral' formatter for other fields
                                        },

                            # display a tooltip whenever the cursor is vertically in line with a glyph
                            mode='vline',
                            )

    # Configure axes
    # - x -
    p.xaxis.ticker = DaysTicker(days=np.arange(0, len(data["DateTime"])))
    p.xaxis.major_label_orientation = 1
    p.xaxis.formatter=DatetimeTickFormatter(
                                            hours=["%d %b %Y"],
                                            days=["%d %b %Y"],
                                            months=["%d %b %Y"],
                                            years=["%d %b %Y"],
                                            )

    # - y -
    p.yaxis.axis_label = "Voltage in V"
    p.y_range=Range1d(225, 260)

    # Add plots
    l1 = p.line("date", "V1[V]", source=src, line_color=colors[1], legend="Phase 1")
    l2= p.line("date", "V2[V]", source=src, line_color=colors[2], legend="Phase 2")
    l3 = p.line("date", "V3[V]", source=src, line_color=colors[3], legend="Phase 3")
    
    # Add hovertool
    hovertool.renderers = [l1]
    p.add_tools(hovertool)
    
    # Legend
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    
    return p, l1, l2, l3


def make_document(doc):
    
    # Load initial data
    src_power = make_dataset(["P[W]", "P1[W]", "P2[W]", "P3[W]"]) 
    src_voltage = make_dataset(["V1[V]", "V2[V]", "V3[V]"])
    src_current = make_dataset(["A1[A]", "A2[A]", "A3[A]"]) 
    
    # Create initial plot
    plot_power, p0, p1, p2, p3 = make_power_plot(src_power)
    plot_voltage, v1, v2, v3 = make_voltage_plot(src_voltage)
    plot_current, i1, i2, i3 = make_current_plot(src_current)

    # Layout
    layout = column(row(plot_power),
                    row(plot_voltage),
                    row(plot_current)
                   )
    
    #doc.add_periodic_callback(update, 1000)
    doc.title("Power Monitoring Agok")
    doc.add_root(layout)

    
# Start Server    
apps = {'/': Application(FunctionHandler(make_document))}
server = Server(apps, port=5000)
server.start()