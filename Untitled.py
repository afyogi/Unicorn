
# coding: utf-8

# In[20]:


import geopandas as gpd
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns


# In[21]:


shapefile = 'ne_110m_admin_0_countries.shp'

#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
gdf


# In[3]:


print(gdf[gdf['country'] == 'Antarctica'])

#Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])


# In[4]:


import pandas as pd

datafile = 'unicorn.csv'

#Read csv file using pandas
df = pd.read_csv(datafile)

df


# In[41]:


merged = df.merge(gdf, left_on = 'Country', right_on = 'country')
gdf.plot()


# In[47]:


buff = gpd.GeoDataFrame(merged)
buff


# In[46]:


import json

#Read data to json
merged_json = json.loads(buff.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)


# In[48]:


from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40)

#Create figure object.
p = figure(title = 'Share of adults who are obese, 2016', plot_height = 600 , plot_width = 950, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'Valuation', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)


#Display figure inline in Jupyter Notebook.
output_notebook()

#Display figure.
show(p)

