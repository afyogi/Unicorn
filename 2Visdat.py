
# coding: utf-8

# In[40]:


# Standard imports 

from bokeh.io import output_notebook, show
output_notebook()


# In[56]:


from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import row, column
import pandas as pd
import numpy as np
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Slider, Select, TextInput
from os.path import dirname, join
from bokeh.layouts import layout, column
from bokeh.models import ColumnDataSource, Div
from bokeh.models import HoverTool
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure, output_file
from bokeh.models import Select
import geopandas as gpd
import numpy as np
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import json
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer




# In[57]:


df = pd.read_csv("unicorn.csv")
SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

shapefile = 'ne_110m_admin_0_countries.shp'

#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
gdf = gdf.drop(gdf.index[159])


merged = df.merge(gdf, left_on = 'Country', right_on = 'country')
buff = gpd.GeoDataFrame(merged)

#Read data to json
merged_json = json.loads(buff.to_json())
m_json = json.loads(gdf.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)
all_data =  json.dumps(m_json)


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

#Create figure object.
p = figure(title = 'Share of adults who are obese, 2016', plot_height = 700 , plot_width = 800, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 

p.patches('xs','ys', source = sfc , line_color = 'black', line_width = 0.25, fill_alpha = 0)

p.patches('xs','ys', source = geosource,fill_color = {'field' :'Valuation', 'transform' : color_mapper},
          line_color = 'white', line_width = 0.25, fill_alpha = 1)
# In[58]:


#Display figure.
show(p)

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]


# In[59]:


def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    TOOLTIPS=[
    	("Company Name", "@Company"),
    	("Country", "@Country"),
    	("Category", "@Category"),
    	("Valuation", "@Valuation")
	]

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    
    p = figure(plot_height=620, plot_width=1100, tools='pan,box_zoom,reset,hover', toolbar_location = None, **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]

    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

    return p


# In[60]:


def update(attr, old, new):
    layout.children[1] = create_figure()


# In[61]:



x = Select(title='X-Axis', value='Valuation', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='Country', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + continuous)
color.on_change('value', update)

controls = column([x, y, color, size], width=200)
layout = row(create_figure(), controls)


# In[65]:


curdoc().add_root(layout)
curdoc().title = "Unicorn"

output_file("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.html")
