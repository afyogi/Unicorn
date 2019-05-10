
# coding: utf-8

# In[13]:


# Pandas for data management
import pandas as pd
import geopandas as gpd
# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from Map import map_tab
from SPlot import plot_tab

# In[15]:


# Put all the tabs into one application
tab1 = map_tab()
tab2 = plot_tab()
#tab3 = map_tab()


tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

