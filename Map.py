
# coding: utf-8

# In[11]:


import geopandas as gpd
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool, Panel
from bokeh.layouts import widgetbox, row, column
from bokeh.models import (CategoricalColorMapper, HoverTool, ColumnDataSource, Panel, FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Tabs, CheckboxButtonGroup, TableColumn, DataTable, Select)



def map_tab():
    shapefile = 'ne_110m_admin_0_countries.shp'

#Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

#Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']

#Drop row corresponding to 'Antarctica'
    gdf = gdf.drop(gdf.index[159])


# In[14]:


    datafile = 'unicorn.csv'

#Read csv file using pandas
    df = pd.read_csv(datafile)

# In[15]:


    merged = df.merge(gdf, left_on = 'Country', right_on = 'country')


# In[16]:


    buff = gpd.GeoDataFrame(merged)


# In[17]:


    import json

#Read data to json
    merged_json = json.loads(buff.to_json())
    m_json = json.loads(gdf.to_json())

#Convert to str like object
    json_data = json.dumps(merged_json)
    all_data =  json.dumps(m_json)


# In[19]:


    from bokeh.io import output_notebook, show, output_file
    from bokeh.plotting import figure
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
    from bokeh.palettes import brewer

#Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)
    sfc = GeoJSONDataSource(geojson = all_data)

#Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40)

#Define custom tick labels for color bar.

    hover = HoverTool(tooltips = [ ('Company Name', '@Company'),('Country/region','@Country'),('Valuation', '@Valuation')])

#Create figure object.
    p = figure(title = 'World Map of Unicorn Start-Up', plot_height = 550 , plot_width = 978, toolbar_location = None, tools = [hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

#Add patch renderer to figure. 



    p.patches('xs','ys', source = sfc , line_color = 'black', line_width = 0.25, fill_alpha = 0)

    p.patches('xs','ys', source = geosource,fill_color = {'field' :'Valuation', 'transform' : color_mapper},
          line_color = 'white', line_width = 0.25, fill_alpha = 1)

    layout = column(p)
    tab = Panel(child = layout, title = 'Map')
    return tab    
        

