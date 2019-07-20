import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Range1d, Arrow, VeeHead, Label, LinearAxis

# Read data
trade_balance = pd.read_csv("PolandTradeBalance.csv", sep=";")
trade_balance.head()

trade_balance.describe()

# Convert year and quarter to specific datetime objects
quarter_begin = []
for row in range(len(trade_balance)):
    quarter_begin.append(datetime.datetime(trade_balance['year'][row], trade_balance['quarter'][row] * 3 - 2, 1))
trade_balance['quarter_begin'] = quarter_begin  # Need to add column for converting to ColumnDataSource later

# Create columns for HoverTool descriptions
period = []  # '2004Q1' format
for row in range(len(trade_balance)):
    period.append(str(trade_balance['year'][row]) + "Q" + str(trade_balance['quarter'][row]))
trade_balance['period'] = period


def add_mln_to_column(column):  # Convert integer to string with commas and add currency
    column_eur = []
    for row in range(len(column)):
        column_eur.append(
            "{:,}".format(column[row]) + " mln EUR")
    return column_eur


trade_balance['import_EUR'] = add_mln_to_column(trade_balance['import'])
trade_balance['export_EUR'] = add_mln_to_column(trade_balance['export'])
trade_balance['balance_EUR'] = add_mln_to_column(trade_balance['balance'])

trade_balance_cds = ColumnDataSource(trade_balance)  # Needed for HoverTool to work

# Create plot
p = figure(plot_width=900,
           plot_height=900,
           title='Polish Trade Balance 2004-2018',
           x_axis_label='Period',
           y_axis_label='Import and export (mln EUR)',
           x_axis_type='datetime',
           y_range=(5000, 60000))
p.extra_y_ranges = {"foo": Range1d(start=-7000, end=5000)}  # Needed to add right scale
p.add_layout(LinearAxis(y_range_name="foo",
                        axis_label='Trade balance (mln EUR)',
                        axis_label_text_font_style='bold'),
             'right')  # Right scale
p.title.align = 'center'
p.title.text_font_size = '18pt'
p.xaxis.axis_label_text_font_style = 'bold'
p.yaxis.axis_label_text_font_style = 'bold'
p.xgrid.visible = False  # Delete vertical grid
p.vbar(x='quarter_begin',
       bottom=0,
       top='balance',
       width=5000000000,  # milliseconds
       y_range_name='foo',  # Use right scale instead of left
       source=trade_balance_cds,
       color='lightsteelblue',
       legend="Trade balance")
p.step('quarter_begin',
       'import',
       source=trade_balance_cds,
       line_width=2,
       mode="before",
       color="blue",
       legend="Import")
p.step('quarter_begin',
       'export',
       source=trade_balance_cds,
       line_width=2,
       mode="before",
       color="green",
       legend="Export")
p.xaxis.major_label_orientation = np.pi / 4  # Flip x-axis labels
hover = HoverTool(tooltips=[('Period', '@period'),
                            ('Import', '@import_EUR'),
                            ('Export', '@export_EUR'),
                            ('Tradebalance', '@balance_EUR')])
p.add_tools(hover)
p.legend.location = "top_left"
p.legend.click_policy = "hide"
p.add_layout(Arrow(end=VeeHead(size=4),
                   line_color="black",
                   x_start=1236552800000,  # Dates converted to milliseconds using online converter
                   y_start=42000,
                   x_end=1218751200000,
                   y_end=37500))
p.add_layout(Arrow(end=VeeHead(size=4),
                   line_color="black",
                   x_start=1083362400000,
                   y_start=40000,
                   x_end=1083362400000,
                   y_end=37500))
p.add_layout(Label(x=1216552800000,
                   y=42300,
                   text='2008Q3 - Financial crisis hits EU',
                   text_font_size='10pt'))
p.add_layout(Label(x=1053362400000,
                   y=40300,
                   text='2004/05/01 - Poland joins EU',
                   text_font_size='10pt'))
p.add_layout(Label(x=1236552800000,
                   y=56000,
                   text='Hover over bar chart to get more details.',
                   text_font_size='10pt',
                   text_alpha=0.5))  # Add transparency
p.add_layout(Label(x=1236552800000,
                   y=54500,
                   text='Click on legend item to hide/show plot.',
                   text_font_size='10pt',
                   text_alpha=0.5))
p.add_layout(Label(x=1236552800000,
                   y=16000,
                   text='Both import and export grew almost 5x since joining EU.',
                   text_font_size='10pt',
                   text_alpha=0.8))
p.add_layout(Label(x=1236552800000,
                   y=14500,
                   text='Most of the time trade balance is still negative.',
                   text_font_size='10pt',
                   text_alpha=0.8))
output_file('PolishTradeBalance.html')
show(p)
