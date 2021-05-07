#!/usr/bin/env python

# Author: Jose Rodriguez (@Cyb3rPandaH)

###### Importing Python Libraries

# Libraries to handle execution errors
import sys

# Libraries to interact with up-to-date ATT&CK content available in STIX format via public TAXII server
from attackcti import attack_client

# Libraries to manipulate data
import pandas as pd
from pandas import json_normalize
pd.set_option("max_colwidth", None)

# Libraries to handle yaml file
import yaml

# Libraries to create visualizations
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import plotly.graph_objects as go

import networkx as nx

###### Functions to Collect ATT&CK Content

# Function to import ATT&CK content as a list of dictionaries
def get_attck_from_stix(matrix = 'enterprise'):
    if  (matrix.lower() == 'enterprise'):
        # Instantiating attack_client class
        lift = attack_client()
        # Getting techniques for windows platform - enterprise matrix
        attck = lift.get_enterprise_techniques(stix_format = False)
        # Removing revoked techniques
        attck = lift.remove_revoked(attck)
        return attck
    else:
        sys.exit('ERROR: Only Enterprise available!!')

###### Functions to Manage ATT&CK Data

# Function to get a dataframe with current current data sources per (sub)technique for the WINDOWS platform within the enterprise matrix.
def get_attack_dataframe (matrix = 'enterprise'):
    if  (matrix.lower() == 'enterprise'):
        # Getting ATT&CK techniques
        attck = get_attck_from_stix(matrix = matrix)
        # Generating a dataframe with information collected
        attck = json_normalize(attck)
        # Selecting columns
        attck = attck[['technique_id','x_mitre_is_subtechnique','technique','tactic','platform','data_sources']]
        # Splitting data_sources field
        attck = attck.explode('data_sources').reset_index(drop=True)
        attck[['data_source','data_component']] = attck.data_sources.str.split(pat = ": ", expand = True)
        attck = attck.drop(columns = ['data_sources'])
        return attck
    else:
        sys.exit('ERROR: Only Enterprise available!!')

###### Functions to Manage YAML Files

# Function to import a yaml file as a pandas dataframe
def import_yaml(path):
    # Accessing yaml file
    yamlFile = open(path, 'r')
    # Loading names of data sources into a dictionary object
    dict = yaml.safe_load(yamlFile)
    # Closing yaml file
    yamlFile.close()
    # Creating Pandas dataframe
    df = pd.DataFrame(dict)
    return df

###### Defining Functions - Visualizations

# Funtion to create a horizontal bar chart using plotly
def bar_chart(data, title, orientation = 'v'):
    if type(data) is pd.core.series.Series: # If the input is a Pandas Series
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y = data.values.tolist(), # Values of Series
            x = data.index.tolist(), # Index of Series
            orientation = orientation))
        
        fig.update_layout(
            title = {
                'text':title,
                'y': 0.85,
                'x': 0.5,
                'xanchor':'center'})

        fig.show()

# Function to get a horizontal bar chart with data labels
def barh_chart(dataframe,xfield,yfield,title,xlabel = '',ylabel = '',figSize = (12,8)):
    ## Code Reference: https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart
    # Bring some raw data.
    if isinstance(dataframe,pd.DataFrame) == True:
        frequencies = dataframe[xfield].values[::-1].tolist()
        max_freq = dataframe[xfield].values.max()
        min_freq = dataframe[xfield].values.min()
        y_labels = dataframe[yfield].values[::-1].tolist()
    elif isinstance(dataframe, DataFrame) == True:
        frequencies = dataframe.toPandas()[xfield].values[::-1].tolist()
        max_freq = dataframe.toPandas()[xfield].values.max()
        min_freq = dataframe.toPandas()[xfield].values.min()
        y_labels = dataframe.toPandas()[yfield].values[::-1].tolist()
    freq_series = pd.Series(frequencies)
    # Plot the figure.
    plt.figure(figsize = figSize)
    ax = freq_series.plot(kind='barh')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticklabels(y_labels)
    ax.set_xlim(min_freq, max_freq) # expand xlim to make labels easier to read
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    rects = ax.patches
    # For each bar: Place a label
    for rect in rects:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2
        # Number of points between bar and label. Change to your liking.
        space = 5
        # Vertical alignment for positive values
        ha = 'left'
        # If value of bar is negative: Place label left of bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label at right
            ha = 'right'
        # Use X value as label and format number with one decimal place
        label = "{:,.0f}".format(x_value)
        # Create annotation
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(space, 0),          # Horizontally shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            va='center',                # Vertically center label
            ha=ha)                      # Horizontally align label differently for
                                        # positive and negative values.

# Function to create network graph
def attack_network_graph(mapping):
    ## Code Reference: https://towardsdatascience.com/customizing-networkx-graphs-f80b4e69bedf
    ## Creating dataframe for relationships
    technique_to_component = mapping[['technique','data_component']].rename(columns={'technique':'source','data_component':'target'})
    data_source_to_component = mapping[['data_source','data_component']].rename(columns={'data_source':'source','data_component':'target'})
    df = pd.concat([technique_to_component,data_source_to_component]).drop_duplicates()
    ## Creating dataframe nodes characteristics
    technique = mapping[['technique']].rename(columns={'technique':'node'})
    technique['type'] = 'technique'
    data_source = mapping[['data_source']].rename(columns={'data_source':'node'})
    data_source['type'] = 'data_source'
    component = mapping[['data_component']].rename(columns={'data_component':'node'})
    component['type'] = 'component'
    nodes_characteristics = pd.concat([technique,data_source,component]).dropna().drop_duplicates()
    ## Defining size of graph
    fig, ax = plt.subplots(figsize=(18,10))
    ## Creating graph object
    G = nx.from_pandas_edgelist(df, 'source', 'target', create_using = nx.Graph())
    ## Making types into categories
    nodes_characteristics = nodes_characteristics.set_index('node')
    # To validate if there are duplicated values before applying reindex: print(nodes_characteristics[nodes_characteristics.index.duplicated()])
    nodes_characteristics = nodes_characteristics.reindex(G.nodes())
    nodes_characteristics['type'] = pd.Categorical(nodes_characteristics['type'])
    nodes_characteristics['type'].cat.codes
    ## Specifying Color
    cmap = matplotlib.colors.ListedColormap(['lime','cyan','orange','gold','lightgray'])
    ## Setting nodes sizes
    node_sizes = [6000 if entry == 'technique'  else (4000 if entry == 'data_source' else 3000) for entry in nodes_characteristics.type]
    ## Drawing graph
    nx.draw(G, with_labels=True, font_size = 14, node_size = node_sizes, node_color = nodes_characteristics['type'].cat.codes,cmap = cmap, node_shape = "o", pos = nx.fruchterman_reingold_layout(G, k=0.3))
    # Creating legend with color box
    leg_technique = mpatches.Patch(color='lightgray', label='Technique')
    leg_data_source = mpatches.Patch(color='orange', label='Data Source')
    leg_data_component = mpatches.Patch(color='lime', label='Data Component')
    plt.legend(handles=[leg_technique,leg_data_source,leg_data_component],loc = 'best', fontsize = 14)
    plt.margins(0.1)
    plt.show()

def network_graph_bokeh(dataframe):
    # Output in Notebook
    output_notebook()

    # Creating networkx graph object
    G = nx.from_pandas_edgelist(dataframe, source = 'source', target = 'target', create_using = nx.DiGraph()) # DiGraph

    # Creating plot object
    plot = Plot(plot_width=900, plot_height=600,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Relationships among Techniques and Data Sources"
    plot.title.align = "center"
    plot.title.text_font_size = "25px"

    # Creating renderer objects
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=20, fill_color=Spectral5[1])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral5[3])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral5[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.9, line_width=1)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral5[3], line_width=4)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral5[4], line_width=4)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()
    plot.renderers.append(graph_renderer)

    # Adding nodes labels
    x,y = zip(*graph_renderer.layout_provider.graph_layout.values())

    names = []
    for i in nx.nodes(G): names.append(i) 
        
    nodes_table = ColumnDataSource({'x': x, 'y': y,'name': names})
    labels = LabelSet(x='x',y='y',text='name',render_mode='canvas',y_offset=-30,text_align='center',
                    text_font_size='15px',source = nodes_table, background_fill_color=None,text_color = 'black')

    plot.renderers.append(labels)

    # Adding tools
    plot.add_tools(HoverTool(tooltips=None),WheelZoomTool(),TapTool(),BoxSelectTool(),BoxZoomTool(),
                PanTool(),LassoSelectTool(),ResetTool())

    # Showing graph
    show(plot)
