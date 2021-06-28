'''
Created on 15 sept. 2017
@author: Guillaume Gaillard
'''
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages 
from matplotlib import rcParams
import matplotlib.colors as mpl_colors
import matplotlib.colorbar as mpl_colorbar
import matplotlib.lines as mpl_lines
import matplotlib.spines as mpl_spines
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.axes as maxes
from matplotlib.ticker import ScalarFormatter
from matplotlib.patches import PathPatch


import io
from PIL import Image


#from wrapper_plottings 
try:
	from . import config_plottings as conf
except ImportError:
	import config_plottings as conf

plot_has_been_shown=False



""" DOCUMENTATION PARAMETERS """

plot_params={}
function_params={}
plot_types=["plot","polar","semilogx","semilogy","loglog","scatter","boxplot","violinplot","vline","hline","vspan","hspan","annotate","imshow","pcolormesh","bar","text","table"]
args_params={}
details={"plot_params":{},"func_params":{}}
for plot_type in plot_types:
    args_params[plot_type]={}
    details["func_params"][plot_type]={}

plot_params["colors"]="""The list of colors in the plots.\n Default: ['black','red']"""
details["plot_params"]["colors"]="""If no colors are given for the plot, color list from config_plotting is used"""
plot_params["file_to_save"]="""The filename you want to save the plot in."""
plot_params["format_to_save"]="""The file format you want to save the plot in."""
plot_params["dir_to_save"]="""The local subdirectory name you want to save the plot file in."""
plot_params["x_axis_label"]="""The label corresponding to the x_axis."""
details["plot_params"]["x_axis_label"]="""Opt. arguments fontsize, font dict, and label pad are set according to config_plotting parameters."""    
plot_params["y_axis_label"]="""The label corresponding to the y_axis."""
details["plot_params"]["y_axis_label"]="""Opt. Arguments fontsize, font dict, and label pad are set according to config_plotting parameters."""    
plot_params["title"]="""The title of the plot.\n Default: none."""
details["plot_params"]["title"]="""Opt. Arguments fontsize and titlepad (using rcParams or y) are set according to config_plotting parameters.\n
Arguments 'verticalalignment': 'baseline' and 'horizontalalignment': "center" are default ones."""
plot_params["legends"]="""The legend/label configuration of the plot.\n Default: ['black','red']"""
details["plot_params"]["legends"]="""Param legend_loc controls the location of the legend in the plot. Default location of legend is 'best'.
italic_legends puts the legend in italic for the plot.
manual_legends enables to create individual legends independently of the items in the plot.
Font size and marker scale&linewidth, and border line width&color of legend are defined in config_plotting."""
plot_params["x_ticks"]="""The tick configuration on the x axis."""
details["plot_params"]["x_ticks"]="""By Default, ticks are on left and bottom axis, labeled with increasing numeric values.
You can define minor and major ticks and configure both using the param dict.
E.G.: "x_ticks":{"major":{"range_step":1, "from":1, "to":8, "labels":["b",'a',2], "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}}
The "params" dict controls axis where ticks are, direction, label presence.
The param range step creates a range of ticks between from and to positions, whereas the positions param is a list of user defined tick positions.
The param "labels" lists the tick labels.
See #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html#matplotlib.axes.Axes.tick_params"""
plot_params["y_ticks"]="""The tick configuration on the y axis."""
details["plot_params"]["y_ticks"]=details["plot_params"]["x_ticks"]    
plot_params["extra_xtick_label_size"]="""Increase or decrease (neg value) in points the size of the x axis label. """
details["plot_params"]["extra_xtick_label_size"]="""Default tick label size is defined in config_plotting."""
plot_params["extra_ytick_label_size"]="""Increase or decrease (neg value) in points the size of the y axis label. """
details["plot_params"]["extra_ytick_label_size"]="""Default tick label size is defined in config_plotting."""
plot_params["xmin"]="""The min value shown on the x axis."""
plot_params["xmax"]="""The max value shown on the x axis."""
plot_params["ymin"]="""The min value shown on the y axis."""
plot_params["ymax"]="""The max value shown on the y axis."""
plot_params["axes_projection"]="""The projection of the axes. Can be in ['polar'] but not for func in ['semilogx','semilogy','loglog']"""
plot_params["theta_max"]="""The max value shown on the theta axis."""
plot_params["theta_min"]="""The min value shown on the theta axis."""
plot_params["rmax"]="""The max value shown on the r axis."""
plot_params["rmin"]="""The min value shown on the r axis."""
plot_params["grid"]="""Set a grid on the plot."""
details["plot_params"]["grid"]="""E.G.: "grid":{"which":'major',"axis":"both"} will grid on major ticks in x and y directions."""
plot_params["axis_off"]="""Remove the display of the axes of the plot"""
plot_params["color_bar"]="""Add and configure a color bar for the plot"""
details["plot_params"]["color_bar"]="""param location is default right of the plot.
color_list can be given as a parameter, default the one in config_plottings.
Bound values for each color in the list can be given too, otherwise default_bounds triggers the use of the bounds defined in config_plottings.
If neither color_bounds nor default_bounds is used, the color bar is uniformly splitted betwwen 0 and 1.
A label can be defined for the color bar."""    
plot_params["tight_layout"]="""Scale the plot to fit the maximum size without overlapping/outside titles, axis labels, ticklabels """
plot_params["type"]="""The list of types of plots.\n types: {0}""".format(plot_types)


function_params["plot"]="""The basic curve plot function."""
args_params["plot"]["legend"]="""The legend associated with the plot function."""
args_params["plot"]["type"]="""The type of plot function: 'plot'."""
args_params["plot"]["y_values"]="""The y values of the curve to plot"""
args_params["plot"]["x_values"]="""The x values of the curve to plot. \n Default range of x axis"""
details["func_params"]["plot"]["linewidth"]="""Default in config_plotting."""         


function_params["polar"]="""The polar plot function. Same as plot with axes projection polar (y <-> r, theta <-> x)"""
args_params["polar"]["legend"]="""The legend associated with the plot function."""
args_params["polar"]["type"]="""The type of plot function: 'polar'."""
args_params["polar"]["r_values"]="""The r values of the polar curve to plot"""
args_params["polar"]["theta_values"]="""The theta values of the curve to plot."""
details["func_params"]["polar"]["linewidth"]="""Default in config_plotting."""
details["func_params"]["polar"]["theta_min"]="""Default in config_plotting."""
details["func_params"]["polar"]["theta_max"]="""Default in config_plotting."""
details["func_params"]["polar"]["rmin"]="""Default in config_plotting."""
details["func_params"]["polar"]["rmax"]="""Default in config_plotting."""


function_params["semilogx"]="""The basic curve plot function."""
args_params["semilogx"]["legend"]="""The legend associated with the plot function."""
args_params["semilogx"]["type"]="""The type of plot function: 'plot'."""
args_params["semilogx"]["y_values"]="""The y values of the curve to plot"""
args_params["semilogx"]["x_values"]="""The x values of the curve to plot. \n Default range of x axis"""
details["func_params"]["semilogx"]["linewidth"]="""Default in config_plotting."""         

function_params["semilogy"]="""The basic curve plot function."""
args_params["semilogy"]["legend"]="""The legend associated with the plot function."""
args_params["semilogy"]["type"]="""The type of plot function: 'plot'."""
args_params["semilogy"]["y_values"]="""The y values of the curve to plot"""
args_params["semilogy"]["x_values"]="""The x values of the curve to plot. \n Default range of x axis"""
details["func_params"]["semilogy"]["linewidth"]="""Default in config_plotting."""         

function_params["loglog"]="""The basic curve plot function."""
args_params["loglog"]["legend"]="""The legend associated with the plot function."""
args_params["loglog"]["type"]="""The type of plot function: 'plot'."""
args_params["loglog"]["y_values"]="""The y values of the curve to plot"""
args_params["loglog"]["x_values"]="""The x values of the curve to plot. \n Default range of x axis"""
details["func_params"]["loglog"]["linewidth"]="""Default in config_plotting."""  

function_params["scatter"]="""The basic point plot function."""
args_params["scatter"]["legend"]="""The legend associated with the plot function."""    
args_params["scatter"]["type"]="""The type of plot function: 'scatter'."""
args_params["scatter"]["y_values"]="""The y values of the points to plot"""
args_params["scatter"]["x_values"]="""The x values of the points to plot. \n They are necessary."""
details["func_params"]["scatter"]["s"]="""s parameter is the size of the point. Default exists in config_plotting."""    


function_params["boxplot"]="""The boxplot curve creation and configuration function. default: no fliers."""
args_params["boxplot"]["legend"]="""The legend associated with the plot function."""
args_params["boxplot"]["type"]="""The type of plot function: 'boxplot'."""
args_params["boxplot"]["y_sets"]="""The sets of y values of the data points."""
args_params["boxplot"]["x_values"]="""The x positions of the boxplots."""
args_params["boxplot"]["x_size"]="""The width of the box plots."""
details["func_params"]["boxplot"]["linewidth"]="""lw of the boxplot lines. Default exists in config_plotting."""    
details["func_params"]["boxplot"]["linestyle"]="""ls of the boxplot lines. Default exists in config_plotting."""    
details["func_params"]["boxplot"]["fill"]="""Boolean filling facecolor for inside the bp. Default False."""    
details["func_params"]["boxplot"]["fill_color"]="""The filling facecolor for inside the bp. Default cyan."""    
details["func_params"]["boxplot"]["x_size"]="""The width is constant in current wrapper."""    


function_params["violinplot"]="""The violinplot curve creation and configuration function. default: no fliers."""
args_params["violinplot"]["legend"]="""The legend associated with the plot function."""
args_params["violinplot"]["type"]="""The type of plot function: 'violinplot'."""
args_params["violinplot"]["y_sets"]="""The sets of y values of the data points."""
args_params["violinplot"]["x_values"]="""The x positions of the violinplot."""
args_params["violinplot"]["x_size"]="""The width of the box plots."""
details["func_params"]["violinplot"]["linewidth"]="""lw of the violinplot lines. Default exists in config_plotting."""    
details["func_params"]["violinplot"]["linestyle"]="""ls of the violinplot lines. Default exists in config_plotting."""    
details["func_params"]["violinplot"]["fill"]="""Boolean filling facecolor for inside the bp. Default False."""    
details["func_params"]["violinplot"]["fill_color"]="""The filling facecolor for inside the bp. Default cyan."""    
details["func_params"]["violinplot"]["x_size"]="""Constant width or max for custom w.r.t. range degree."""    


function_params["vline"]="""The vertical line creation and configuration function."""
args_params["vline"]["legend"]="""The legend associated with the plot function."""
args_params["vline"]["type"]="""The type of plot function: 'vline'."""
args_params["vline"]["y_axis_prop_range"]="""The size of the line in proportion of the y axis, defined by start,end couple.\n If not given, covers whole axis length.\n E.G.: (0.25,0.75)"""
args_params["vline"]["x_pos"]="""The x position of the vertical line."""
details["func_params"]["vline"]["linewidth"]="""Default exists in config_plotting."""    

function_params["hline"]="""The horizontal line creation and configuration function."""
args_params["hline"]["legend"]="""The legend associated with the plot function."""
args_params["hline"]["type"]="""The type of plot function: 'hline'."""
args_params["hline"]["x_axis_prop_range"]="""The size of the line in proportion of the x axis, defined by start,end couple.\n If not given, covers whole axis length.\n E.G.: (0.25,0.75)"""
args_params["hline"]["y_pos"]="""The y position of the horizontal line."""
details["func_params"]["hline"]["linewidth"]="""Default in config_plotting."""    
details["func_params"]["hline"]["dashes"]="""List of on/off point sizes of dashes. Default in config_plotting ([])."""    
    
function_params["vspan"]="""The vertical rectangle creation and configuration function."""
args_params["vspan"]["legend"]="""The legend associated with the plot function."""
args_params["vspan"]["type"]="""The type of plot function: 'vspan'."""
args_params["vspan"]["y_axis_prop_range"]="""The height of the rectangle in proportion of the y axis, defined by start,end couple.\n If not given, covers whole axis length.\n E.G.: (0.25,0.75)"""
args_params["vspan"]["x_min"]="""The x postion of the left vertical edge."""
args_params["vspan"]["x_max"]="""The x postion of the right vertical edge."""
details["func_params"]["vspan"]["alpha"]="""Transparence of the span. Defaults in config (0.5)."""    

function_params["hspan"]="""The horizontal rectangle creation and configuration function."""
args_params["hspan"]["legend"]="""The legend associated with the plot function."""
args_params["hspan"]["type"]="""The type of plot function: 'hspan'."""
args_params["hspan"]["x_axis_prop_range"]="""The height of the rectangle in proportion of the x axis, defined by start,end couple.\n If not given, covers whole axis length.\n E.G.: (0.25,0.75)"""
args_params["hspan"]["y_min"]="""The x postion of the bottom horizontal edge."""
args_params["hspan"]["y_max"]="""The x postion of the top horizontal edge."""    
details["func_params"]["hspan"]["alpha"]="""Transparence of the span. Defaults in config (0.5)."""    

    
function_params["annotate"]="""Add a positionned annotation on the plot."""
args_params["annotate"]["legend"]="""The legend associated with the plot function."""
args_params["annotate"]["type"]="""The type of plot function: 'annotate'."""
args_params["annotate"]["text"]="""The annotation"""
args_params["annotate"]["pos"]="""The x,y position of the annotated point."""
details["func_params"]["annotate"]["size"]="""Font size. Defaults in config (tick label size)."""    


function_params["imshow"]="""Add an image based on a matrix of colors."""
args_params["imshow"]["legend"]="""The legend associated with the plot function."""
args_params["imshow"]["type"]="""The type of plot function: 'imshow'."""
args_params["imshow"]["matrix_colors"]="""The matrix of colors"""
details["func_params"]["imshow"]["interpolation"]="""Interpolation method of the matrix. Defaults in config (nearest)."""    
details["func_params"]["imshow"]["aspect"]="""Aspect. Defaults in config (auto)."""    
details["func_params"]["imshow"]["origin"]="""Matrix origin position. Defaults in config (lower)."""    

function_params["bar"]="""Add a (vertical) bar."""
args_params["bar"]["legend"]="""The legend associated with the plot function."""
args_params["bar"]["type"]="""The type of plot function: 'bar'."""
args_params["bar"]["center"]="""The center position of the bar."""
args_params["bar"]["height"]="""The y height of the bar"""
args_params["bar"]["width"]="""The x width of the bar"""
args_params["bar"]["bottom"]="""The bottom position of the bar, default 0."""

function_params["text"]="""Add a positionned text on the plot."""
args_params["text"]["legend"]="""The legend associated with the plot function."""
args_params["text"]["type"]="""The type of plot function: 'text'."""
args_params["text"]["text"]="""The text"""
args_params["text"]["x"]="""The x position of the annotated point."""
args_params["text"]["y"]="""The y position of the annotated point."""
details["func_params"]["text"]["fontdict"]="""Font config dict for the text. Defaults in config (Arial, tick label size)."""    

function_params["table"]="""Add a positionned table on the plot."""
args_params["table"]["legend"]="""The legend associated with the plot function."""
args_params["table"]["type"]="""The type of plot function: 'table'."""
args_params["table"]["matrix"]="""The data matrix of the table."""
args_params["table"]["rows"]="""The list of row labels."""
args_params["table"]["cols"]="""The list of column labels."""

args_params["table"]["line_width_prop"]="""Optional: the proportion of the x axis occupied by the data matrix."""
args_params["table"]["col_height_prop"]="""Optional: the proportion of the y axis occupied by the data matrix."""
args_params["table"]["rowHeights"]="""Optional:  the list of row heights (cancells col_height_prop)."""
args_params["table"]["fontsize"]="""Optional: The font size for the data."""
args_params["table"]["label_params"]="""Optional: The parameters for the row and column labels."""
details["func_params"]["table"]["loc"]="""Position of the table. Defaults in config (center)."""    
details["func_params"]["table"]["cellLoc"]="""Position of the text in the cell. Defaults in config (center)."""    
details["func_params"]["table"]["rowLoc"]="""Position of the text in the row. Defaults in config (center)."""    
details["func_params"]["table"]["colLoc"]="""Position of the text in the column. Defaults in config (center)."""    
details["func_params"]["table"]["fontsize"]="""Defaults in config (tick label size)."""   
details["func_params"]["table"]["label_params"]="""Two params:\n
 edges_off: boolean to remove borders of label cells;
 ylab_height_prop: to set the height of col label cells (in proportion of the y axis).\n Not yet found any solution to control the width of row label cells."""   

for plot_type in plot_types:
    args_params[plot_type]["color_index"]="""Opt. argument giving the index of the color of the plot in the color list."""
    args_params[plot_type]["color"]="""Opt. argument giving the color of the plot/object/element."""
    #args_params[plot_type]["legend"]="""Opt. argument giving the legend/label of the plot."""
    details["func_params"][plot_type]["color_index"]="""color_index is cancelled by color"""
    details["func_params"][plot_type]["legend"]="""Legend are not supported automaticaly for all plot functions. If it does not work, use manual legend."""
    details["func_params"][plot_type]["kawargs"]="""Any other argument is considered as additional arg **kwargs for native function."""
        


def prepare_plots(plot_data):
    prepared_plots={}
    len_data=len(plot_data)
    prepared=0
    for plot in plot_data:
        prepared_plots[plot]={}
        
        keys_in_data=["colors",
                      "file_to_save",
                      "format_to_save",
                      "dir_to_save",
                      "x_axis_label",
                      "y_axis_label",
                      "twin_axis_label",
                      "title",
                      "titlepad",
                      "legends",
                      "x_ticks",
                      "y_ticks",
                      "extra_xtick_label_size",
                      "extra_ytick_label_size",
                      "xmin",
                      "xmax",
                      "ymin",
                      "ymax",
                      "axes_projection",
                      "no_padding",
                      "layout_padding",
                      "theta_min",
                      "theta_max",
                      "rmin",
                      "rmax",
                      "grid",
                      "axis_off",
                      "zoom_bbox",
                      "zoom_bbox_dpi",
                      "side_bar",
                      "color_bar",
                      "tight_layout"]
        for key in keys_in_data:
            if key in plot_data[plot]:
                prepared_plots[plot][key]=plot_data[plot][key]

        prepared_plots[plot]["plot_functions"]=prepare_idv_values(plot_data[plot]["values"])
        if "twinx_values" in plot_data[plot]:
            prepared_plots[plot]["twinx_plot_functions"]=prepare_idv_values(plot_data[plot]["twinx_values"])
        
        prepared+=1
        if (prepared%50==0):
        	print("prepared {0}/{1}".format(prepared,len_data))        
                        
            
    return prepared_plots

def prepare_idv_values(vals_dict):
    plot_functions_list=[]
    for cloud in vals_dict:
        ptype= vals_dict[cloud]["type"]
        plot_func={"func_name":ptype, "legend":""}
        
        prepared_params=["type"]
        
        if ptype in ["plot","semilogx","semilogy","loglog"]:
            if "x_values" in vals_dict[cloud]:
                plot_func["args"]=[vals_dict[cloud]["x_values"],vals_dict[cloud]["y_values"]]
            else:
                plot_func["args"]=[vals_dict[cloud]["y_values"]]       
            
            prepared_params+=["x_values","y_values"]
            
        
        if ptype=="polar":
            plot_func["args"]=[vals_dict[cloud]["theta_values"],vals_dict[cloud]["r_values"]]
            prepared_params+=["theta_values","r_values"]
        
        if ptype=="scatter":
            plot_func["args"]=[vals_dict[cloud]["x_values"],vals_dict[cloud]["y_values"]]
            #(x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, verts, edgecolors, hold, data)
            prepared_params+=["x_values","y_values"]
        
        if ptype=="boxplot":
            plot_func["args"]={"y_sets":vals_dict[cloud]["y_sets"],
                               "x_values":vals_dict[cloud]["x_values"],
                               "x_size":vals_dict[cloud]["x_size"]}
            bpvalues=["y_sets","x_values","x_size"]
            prepared_params+=bpvalues
        
        if ptype=="violinplot":
            plot_func["args"]={"y_sets":vals_dict[cloud]["y_sets"],
                               "x_values":vals_dict[cloud]["x_values"],
                               "x_size":vals_dict[cloud]["x_size"]}
            bpvalues=["y_sets","x_values","x_size"]
            prepared_params+=bpvalues

        if ptype=="vline":    
            if "y_axis_prop_range" in vals_dict[cloud]:
                plot_func["args"]=[vals_dict[cloud]["x_pos"],
                                   vals_dict[cloud]["y_axis_prop_range"][0],
                                   vals_dict[cloud]["y_axis_prop_range"][1]]
            else:
                plot_func["args"]=[vals_dict[cloud]["x_pos"]]
                
            prepared_params+=["y_axis_prop_range","x_pos"]
        
        if ptype=="hline":    
            if "x_axis_prop_range" in vals_dict[cloud]:
                plot_func["args"]=[vals_dict[cloud]["y_pos"],
                                   vals_dict[cloud]["x_axis_prop_range"][0],
                                   vals_dict[cloud]["x_axis_prop_range"][1]]
            else:
                plot_func["args"]=[vals_dict[cloud]["y_pos"]]
                
            prepared_params+=["x_axis_prop_range","y_pos"]
            
        if ptype=="vspan":    
            if "y_axis_prop_range" in vals_dict[cloud]:
                plot_func["args"]=[vals_dict[cloud]["x_min"],
                                   vals_dict[cloud]["x_max"],
                                   vals_dict[cloud]["y_axis_prop_range"][0],
                                   vals_dict[cloud]["y_axis_prop_range"][1]]
            else:
                plot_func["args"]=[vals_dict[cloud]["x_min"],vals_dict[cloud]["x_max"]]
                
            prepared_params+=["x_axis_prop_range","x_min", "x_max"]
        
        if ptype=="hspan":    
            if "x_axis_prop_range" in vals_dict[cloud]:
                plot_func["args"]=[vals_dict[cloud]["y_min"],vals_dict[cloud]["y_max"],
                                   vals_dict[cloud]["x_axis_prop_range"][0],
                                   vals_dict[cloud]["x_axis_prop_range"][1]]
            else:
                plot_func["args"]=[vals_dict[cloud]["y_min"],vals_dict[cloud]["y_max"]]
                
            prepared_params+=["x_axis_prop_range","y_min","y_max"]
        
        if ptype=="annotate": 
            plot_func["args"]=[vals_dict[cloud]["text"], vals_dict[cloud]["pos"]]
            prepared_params+=["text","pos"]                
        
        if ptype=="imshow":   
            plot_func["args"]=vals_dict[cloud]["matrix_colors"]
            prepared_params+=["matrix_colors"]

        if ptype=="pcolormesh":   
            plot_func["args"]=vals_dict[cloud]["array"]
            plot_func["cmap_list"]=vals_dict[cloud]["cmap_list"]
            plot_func["xmin"]=vals_dict[cloud]["xmin"]
            plot_func["xmax"]=vals_dict[cloud]["xmax"]
            plot_func["ymin"]=vals_dict[cloud]["ymin"]
            plot_func["ymax"]=vals_dict[cloud]["ymax"]
            plot_func["vmin"]=vals_dict[cloud]["vmin"]
            plot_func["vmax"]=vals_dict[cloud]["vmax"]
            prepared_params+=["array"]                

                     
        
        if ptype=="bar":   
            plot_func["args"]=[vals_dict[cloud]["center"],
                               vals_dict[cloud]["height"],
                               vals_dict[cloud]["width"],
                               vals_dict[cloud]["bottom"] if "bottom" in vals_dict[cloud] else 0]
#                 plot_func["args"]={"left":vals_dict[cloud]["left"],
#                                    "height":vals_dict[cloud]["height"],
#                                    "width":vals_dict[cloud]["width"],
#                                    "bottom":vals_dict[cloud]["bottom"] if "bottom" in vals_dict[cloud] else 0}
            prepared_params+=["center","height","width","bottom"]
            
        if ptype=="text":
            plot_func["args"]=[vals_dict[cloud]["x"],
                               vals_dict[cloud]["y"],
                               vals_dict[cloud]["text"]]
            
            prepared_params+=["x","y","text"]
            
            
        if ptype=="table":
                            
            plot_func["cellText"]=vals_dict[cloud]["matrix"]
            plot_func["rowLabels"]=vals_dict[cloud]["rows"]
            plot_func["colLabels"]=vals_dict[cloud]["cols"]
            plot_func["args"]={"nb_rows":len(plot_func["rowLabels"]),
                               "nb_cols":len(plot_func["colLabels"])}                   
            
            if "line_width_prop" in vals_dict[cloud]:
                nb_cols=plot_func["args"]["nb_cols"]                    
                plot_func["colWidths"]=[1.*vals_dict[cloud]["line_width_prop"]/(nb_cols)]*nb_cols
#                 if "colWidths" in vals_dict[cloud]:
#                     plot_func["colWidths"]=vals_dict[cloud]["colWidths"]
            
            if "col_height_prop" in vals_dict[cloud]:
                nb_rows=plot_func["args"]["nb_rows"]                    
                plot_func["args"]["rowHeights"]=[1.*vals_dict[cloud]["col_height_prop"]/(nb_rows)]*nb_rows
            if "rowHeights" in vals_dict[cloud]:
                plot_func["args"]["rowHeights"]=vals_dict[cloud]["rowHeights"]
            
            if "fontsize" in vals_dict[cloud]:
                plot_func["args"]["fontsize"]=vals_dict[cloud]["fontsize"]
                
            if "label_params" in vals_dict[cloud]:
                plot_func["args"]["label_params"]=vals_dict[cloud]["label_params"]
            
            prepared_params+=["rows","cols","matrix","line_width_prop","col_height_prop","fontsize", "label_params", "rowHeights"]
            
                                            
                    
        for key in vals_dict[cloud]:
            if key not in prepared_params:
                plot_func[key]=vals_dict[cloud][key]
                        
        plot_functions_list.append(plot_func)
        del plot_func

    return(plot_functions_list)

def plot_functions(plot_functions,colors,zeplt,should_be_legended=False):
    func_id=0
    has_box_plots=False
    other_legend_handles=[]

    for plot_func in plot_functions:
        kawargs={"label":plot_func["legend"]}
        
        if "color_index" in plot_func: 
            kawargs["color"]=colors[plot_func["color_index"]]

        for key in plot_func:
            if key not in ["color_index","args","func_name","legend"]:
                kawargs[key]=plot_func[key]
        for key in conf.plot_params[plot_func["func_name"]]:
            if key not in kawargs:
                kawargs[key]=conf.plot_params[plot_func["func_name"]][key]
        
        if plot_func["func_name"]=="bar":
            zeplt.bar(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="plot":
            zeplt.plot(*plot_func["args"], **kawargs)
            #plt.semilogx(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="polar":
            plt.polar(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="semilogx":
            zeplt.semilogx(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="semilogy":
            zeplt.semilogy(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="loglog":
            zeplt.loglog(*plot_func["args"], **kawargs)
            
        if plot_func["func_name"]=="annotate":
            zeplt.annotate(*plot_func["args"], **kawargs)
            if 'label' in kawargs and len(kawargs['label'])>0:
                manual_label=mpl_lines.Line2D(
                            [],[],color=kawargs["color"] if "color" in kawargs else 'k',
                            linestyle='-', fillstyle='none',mew=0.6,ms=6,label=kawargs['label'])
                other_legend_handles.append(manual_label)
        
        if plot_func["func_name"]=="table":
            the_table=zeplt.table(**kawargs)
            
            nb_cols=plot_func["args"]["nb_cols"]
            nb_rows=plot_func["args"]["nb_rows"]
            
            for key, cell in the_table.get_celld().items():
                if key[0] in range(1,nb_rows+1) and key[1] in range(nb_cols):
                    if "rowHeights" in plot_func["args"]:
                        cell.set_height(plot_func["args"]["rowHeights"][key[0]-1])
                    if "fontsize" in plot_func["args"]:
                        cell._text.set_fontsize(plot_func["args"]["fontsize"])
                    if "color" in kawargs:
                        cell._text.set_color(kawargs["color"])                            
                 
                if key[0] in range(1,nb_rows+1) and key[1] == -1:
                    cell._text.set_text(' '+cell._text.get_text()+' ')
                    if "rowHeights" in plot_func["args"]:
                        cell.set_height(plot_func["args"]["rowHeights"][key[0]-1])
                    if "label_params" in plot_func["args"]:
                        if "edges_off" in plot_func["args"]["label_params"] and plot_func["args"]["label_params"]["edges_off"]:
                            cell.set_linewidth(0)
                if key[0] == 0: 
                    if "label_params" in plot_func["args"]:
                        if "ylab_height_prop" in plot_func["args"]["label_params"]:
                            cell.set_height(plot_func["args"]["label_params"]["ylab_height_prop"])
                        if "edges_off" in plot_func["args"]["label_params"] and plot_func["args"]["label_params"]["edges_off"]:
                            cell.set_linewidth(0)

        
        if plot_func["func_name"]=="text":
            zeplt.text(*plot_func["args"], **kawargs)
            
        if plot_func["func_name"]=="vline":
            zeplt.axvline(*plot_func["args"],**kawargs)
                
        if plot_func["func_name"]=="hline":
            zeplt.axhline(*plot_func["args"],**kawargs)
                
        if plot_func["func_name"]=="vspan":
            zeplt.axvspan(*plot_func["args"],**kawargs)
                
        if plot_func["func_name"]=="hspan":
            zeplt.axhspan(*plot_func["args"],**kawargs)
                
        if plot_func["func_name"]=="scatter":
            zeplt.scatter(*plot_func["args"], **kawargs)
        
        if plot_func["func_name"]=="imshow":
            zeplt.imshow(plot_func["args"], **kawargs)

        if plot_func["func_name"]=="pcolormesh":
            xmin=plot_func["xmin"]
            xmax=plot_func["xmax"]
            ymin=plot_func["ymin"]
            ymax=plot_func["ymax"]
            vmin=plot_func["vmin"]
            vmax=plot_func["vmax"]
            xstart=np.pi/180*xmin
            xstop=np.pi/180*xmax
            xrange=xmax-xmin
            ystart=np.pi/180*ymin
            ystop=np.pi/180*ymax
            yrange=ymax-ymin
            lon = np.linspace(xstart, xstop, xrange+1)
            lat = np.linspace(ystart, ystop, yrange+1)
            # lon = np.linspace(-np.pi, np.pi,317)
            # lat = np.linspace(-np.pi/6., np.pi/6.,63)
            Lon,Lat = np.meshgrid(lon,lat)
            print(plot_func["cmap_list"])
            color_list=plot_func["cmap_list"]
            zeplt.pcolormesh(
                Lon,
                Lat,
                plot_func["args"],
                cmap=mpl_colors.ListedColormap(color_list),
                vmin=vmin,vmax=vmax,
                rasterized=True,
                shading='auto'
            )
            #edgecolor='none')#cmap=plt.cm.jet)

            
        my_box_plot={}
        if plot_func["func_name"]=="boxplot":
            has_box_plots=kawargs["manage_ticks"] if "manage_ticks" in kawargs else True
            my_box_plot[func_id]=zeplt.boxplot(plot_func["args"]["y_sets"], 
                positions = plot_func["args"]["x_values"],
                sym='o',#'bx',
                #whis = 1,#default 1.5
                whis=kawargs["whis"] if "whis" in kawargs else (0,100),
                widths=[plot_func["args"]["x_size"]]*len(plot_func["args"]["x_values"]), #(4.2, 4.2),
                showfliers=kawargs["showfliers"] if "showfliers" in kawargs else False,
                showcaps=kawargs["showcaps"] if "showcaps" in kawargs else True,
                patch_artist = True,
                manage_ticks=kawargs["manage_ticks"] if "manage_ticks" in kawargs else True)
            

            # print(my_box_plot[func_id].keys())#dict_keys(['whiskers', 'caps', 'boxes', 'medians', 'fliers', 'means'])
            not_legended=True
            for element in my_box_plot[func_id]['medians']:
                if should_be_legended and not_legended:
                    element.set_label(plot_func["legend"])# label
                    not_legended=False
                if "color" in kawargs:
                    element.set_color(kawargs["color"])#conf.colors[plot_func["color_index"]]
#                    element.set_linestyle('solid')#('dashed')
                element.set_linestyle(kawargs["linestyle"])#('dashed')
                element.set_linewidth(kawargs["linewidth"])

            elt_id=0
            for element in my_box_plot[func_id]['boxes']:
                if "color" in kawargs:
                    element.set_edgecolor(kawargs["color"])
                element.set_facecolor(kawargs["fill_color"])
                if "box_edge_width" in kawargs:
                    element.set_linewidth(kawargs["box_edge_width"])
                else:
                    element.set_linewidth(kawargs["linewidth"])
                # element.set_linestyle('solid')#('dashed')
                element.set_linestyle(kawargs["linestyle"])#('dashed')
                element.set_fill(kawargs["fill"])
                #element.set_hatch('/')
                if "fill_map" in kawargs:
                    # element.set_fill(False)
                    vert=element.get_path().vertices

                    if "cmap_list" in kawargs:
                        nb_colors=1+len(kawargs["cmap_list"])
                        colormap=mpl_colors.ListedColormap(kawargs["cmap_list"])
                    else:
                        nb_colors=256
                        colormap=plt.cm.viridis

                    
                    if "clip_on_box" in kawargs:
                        
                        extent=[vert[0][0],vert[1][0],kawargs["fill_map"][0],kawargs["fill_map"][1]]
                        # gradient = np.linspace(0, 1, len(kawargs["cmap_list"]))
                        # gradient = np.vstack((gradient, gradient)).T
                        # imb = plt.imshow(gradient, cmap=mpl_colors.ListedColormap(kawargs["cmap_list"]),#plt.cm.viridis,
                        #                origin='lower', extent=extent,
                        #                clip_path=element, clip_on=True)
                        # imb.set_clip_path(element)
                            
                        imb = plt.pcolormesh(
                            (extent[0], extent[1]), 
                            np.linspace(extent[2],extent[3],nb_colors),
                            np.linspace((0,0),(nb_colors-1,nb_colors-1),nb_colors),
                            cmap=colormap,
                            clip_path=element, clip_on=True,rasterized=True,
                            shading='auto'
                            )

                    else:

                        extent=[vert[0][0],vert[1][0],min(plot_func["args"]["y_sets"][elt_id]),max(plot_func["args"]["y_sets"][elt_id])]

                        pmin=(extent[2]-kawargs["fill_map"][0])/(kawargs["fill_map"][1]-kawargs["fill_map"][0])*nb_colors
                        pmax=(extent[3]-kawargs["fill_map"][0])/(kawargs["fill_map"][1]-kawargs["fill_map"][0])*nb_colors

                        imb = plt.pcolormesh(
                            (extent[0], extent[1]), #X
                            np.linspace(extent[2],extent[3],nb_colors),#Y
                            np.linspace(pmin,pmax,nb_colors-1).reshape((nb_colors-1,1)),
                            vmin=0,
                            # vmax=nb_colors,
                            vmax=nb_colors-1,
                            cmap=colormap, 
                            rasterized=True,
                            shading='flat'
                            # shading='gouraud'
                            # shading='nearest'
                            # shading='auto'
                            )

                    elt_id+=1




            for element in my_box_plot[func_id]['whiskers']:
                if "color" in kawargs:
                    element.set_color(kawargs["color"])#conf.colors[plot_func["color_index"]]
                element.set_linewidth(kawargs["linewidth"])
                element.set_linestyle(kawargs["linestyle"])#('dashed')

            for element in my_box_plot[func_id]['caps']:
                if "color" in kawargs:
                    element.set_color(kawargs["color"])#(colors[sheet_names.index(sheet)])#('blue')
                element.set_linewidth(kawargs["linewidth"])
                element.set_linestyle(kawargs["linestyle"])#('dashed')

            for element in my_box_plot[func_id]['fliers']: # https://stackoverflow.com/questions/32480988/matplotlib-fliers-in-boxplot-object-not-setting-correctly
                element.set_markerfacecolor("None")#(colors[sheet_names.index(sheet)])#('blue')
                element.set_alpha(0.6)
                # element.set_color("None")#(colors[sheet_names.index(sheet)])#('blue')
                if "color" in kawargs:
                    element.set_markeredgecolor(kawargs["color"])#(colors[sheet_names.index(sheet)])#('blue')
                else:
                    element.set_markeredgecolor("purple")#(colors[sheet_names.index(sheet)])#('blue')

                element.set_markeredgewidth(kawargs["linewidth"])
                element.set_markersize(kawargs["fliersize"] if "fliersize" in kawargs else 12*plot_func["args"]["x_size"])#('dashed')   
                # element.set_marker('d')#  overrides sym


        if plot_func["func_name"]=="violinplot":
            considered_widths=[plot_func["args"]["x_size"]]*len(plot_func["args"]["x_values"])

            if "custom_x_size" in kawargs:
                maxwidth=plot_func["args"]["x_size"]
                dyel=kawargs["custom_x_size"]["delta_y"]

                mdw=0
                wimax=[]
                for yes in plot_func["args"]["y_sets"]:
                    ywidth=0
                    current_y_range=min(yes)
                    ymin=min(yes)
                    ymax=max(yes)
                    rows={i:[] for i in range(int((ymax-ymin)/dyel)+1)}
                    for i in sorted(yes):
                        rows[int((i-ymin)/dyel)].append(i)

                    ywidth=max(len(rows[i]) for i in rows) #in dots
                    wimax.append(ywidth)
                    mdw=max(mdw,ywidth)

                dxel=maxwidth/mdw

                considered_widths=[j*dxel for j in wimax]

            if "scattered" in kawargs:
                if not ("custom_x_size" in kawargs):
                    dyel=1
                    dxel=plot_func["args"]["x_size"]/10

                xind=0
                for yes in plot_func["args"]["y_sets"]:
                    xind+=1

                    ymin=min(yes)
                    ymax=max(yes)
                    rows={i:[] for i in range(int((ymax-ymin)/dyel)+1)}
                    for i in sorted(yes):
                        rows[int((i-ymin)/dyel)].append(i)

                    xax=[]
                    for row in rows:
                        nel=len(rows[row])
                        for ptind in range(nel):
                            xval=plot_func["args"]["x_values"][xind-1]+(ptind*dxel - dxel*nel/2 + dxel - ((nel)%2)*dxel/2 - ((nel+1)%2)*dxel/2 )
                            xax.append(xval)

                    plt.scatter(xax,sorted(yes), zorder=10, **(kawargs["scattered"]))



            violin_func=zeplt.violinplot(plot_func["args"]["y_sets"], 
                positions = plot_func["args"]["x_values"],
                widths=considered_widths,
                showmeans=True,
                showmedians=True,
                showextrema=True,
                bw_method=kawargs["bw_method"] if "bw_method" in kawargs else 'scott',
                ) #(4.2, 4.2),
            
            
            # print(violin_func.keys())#dict_keys(['bodies', 'cmeans', 'cmaxes', 'cmins', 'cbars', 'cmedians'])
            not_legended=True
            median_lines=violin_func['cmedians']
            if should_be_legended and not_legended:
                median_lines.set_label(plot_func["legend"])# label
                not_legended=False
            if "color" in kawargs:
                median_lines.set_color(kawargs["color"])
#                    element.set_linestyle('solid')#('dashed')
            median_lines.set_linestyle(kawargs["linestyle"])#('dashed')
            median_lines.set_linewidth(kawargs["linewidth"])
            cmin_lines=violin_func['cmins']
            if "color" in kawargs:
                cmin_lines.set_color(kawargs["color"])
            cmin_lines.set_linewidth(kawargs["linewidth"])
            cmin_lines.set_linestyle(kawargs["linestyle"])#('dashed')

            cbars_lines=violin_func['cbars']
            if "color" in kawargs:
                cbars_lines.set_color(kawargs["color"])
            cbars_lines.set_linewidth(kawargs["linewidth"])
            cbars_lines.set_linestyle(kawargs["linestyle"])#('dashed')

            cmeans_lines=violin_func['cmeans'] 
            cmeans_lines.set_alpha(0.6)
            if "color" in kawargs:
                cmeans_lines.set_color(kawargs["color"])#(colors[sheet_names.index(sheet)])#('blue')

            elt_id=0
            for element in violin_func['bodies']:
                element.set_facecolor(kawargs["fill_color"])
                if "violin_edge_width" in kawargs:
                    element.set_linewidth(kawargs["violin_edge_width"])
                else:
                    element.set_linewidth(kawargs["linewidth"])
                # element.set_linestyle('solid')#('dashed')
                element.set_linestyle(kawargs["linestyle"])#('dashed')

                if not kawargs["fill"]:
                    element.set_facecolor('white')
                    # element.set_alpha(0)

                if "color" in kawargs:
                    element.set_edgecolor(kawargs["color"])

                if "fill_map" in kawargs:
                    vert=element.get_paths()[0].vertices

                    if "cmap_list" in kawargs:
                        nb_colors=1+len(kawargs["cmap_list"])
                        colormap=mpl_colors.ListedColormap(kawargs["cmap_list"])
                    else:
                        nb_colors=256
                        colormap=plt.cm.viridis

                    patch_edgecolor=kawargs["color"] if "color" in kawargs else 'k'
                    patch=PathPatch(element.get_paths()[0], facecolor='none', edgecolor=patch_edgecolor, linestyle=kawargs["linestyle"])
                    plt.gca().add_patch(patch)

                    
                    if not ("indep_violin_fill" in kawargs):
                        extent=[min(vert[:,0]), max(vert[:,0]),kawargs["fill_map"][0],kawargs["fill_map"][1]]

                        imb = plt.pcolormesh(
                            (extent[0], extent[1]), 
                            np.linspace(extent[2],extent[3],nb_colors),
                            # np.linspace((0,0),(nb_colors-1,nb_colors-1),nb_colors),
                            np.linspace(0,nb_colors-1,nb_colors-1).reshape((nb_colors-1,1)),
                            cmap=colormap,
                            clip_path=patch, clip_on=True,rasterized=True,
                            shading='flat'
                            # shading='auto'
                            ) #element.get_transformed_clip_path_and_affine()

                        imb.set_clip_path(patch)
                    else:
                        extent=[min(vert[:,0]), max(vert[:,0]),min(plot_func["args"]["y_sets"][elt_id]),max(plot_func["args"]["y_sets"][elt_id])]

                        imb = plt.pcolormesh(
                            (extent[0], extent[1]), #X
                            np.linspace(extent[2],extent[3],nb_colors),#Y
                            np.linspace((0,0),(nb_colors-1,nb_colors-1),nb_colors),# color grid       
                            vmin=0,
                            vmax=nb_colors-1,
                            cmap=colormap, 
                            clip_path=patch, clip_on=True,
                            rasterized=True,
                            shading='auto'
                            )
                        imb.set_clip_path(patch)

                elt_id+=1
        func_id+=1

    return(func_id, has_box_plots, other_legend_handles)


def plot_indivs(prepared_plots,show=False,file_to_save=None,format_to_save=None,dir_to_save=None,PDF_to_add=None, from_page=False, in_ax=None,user_defined_dpi=conf.dpi):
    #figs
    zeplt=plt
    has_predef_axes=not(in_ax is None)
    if has_predef_axes:
        zeplt=in_ax
        zeplt.yaxis.tick_right()
        zeplt.set_xticks([])
        zeplt.set_yticks([])   


    other_legend_handles=[]                  
        
    for plot in prepared_plots:
        #this fig
        if not from_page:
            if has_predef_axes:
                fig=zeplt.get_figure()
            else:
                fig=zeplt.figure(num=plot, figsize=conf.figsize, dpi=conf.dpi)#, facecolor, edgecolor, frameon, FigureClass)
            if 'axes_projection' in prepared_plots[plot]:
                if prepared_plots[plot]['axes_projection']=='polar':
                    fig.add_subplot(111, polar=True)
        #titles
        if "x_axis_label" in prepared_plots[plot]:
            if has_predef_axes:
                zeplt.set_xlabel(prepared_plots[plot]["x_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)
            else:
                zeplt.xlabel(prepared_plots[plot]["x_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)
        if "y_axis_label" in prepared_plots[plot]:
            if has_predef_axes:
                zeplt.set_ylabel(prepared_plots[plot]["y_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font) 
                zeplt.yaxis.set_label_position("right")
            else:
                zeplt.ylabel(prepared_plots[plot]["y_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)
        if "title" in prepared_plots[plot]:
            fontdict={'fontsize': conf.title_font_size,'verticalalignment': 'baseline','horizontalalignment': "center"}
            if "titlepad" in prepared_plots[plot]:
                titlepad=prepared_plots[plot]["titlepad"]
                plt.title(prepared_plots[plot]["title"],fontdict=fontdict, pad=titlepad)
            elif 'axes.titlepad' in rcParams.keys():
                rcParams['axes.titlepad'] = conf.title_and_axes_labelpad 
                plt.title(prepared_plots[plot]["title"],fontdict=fontdict)
            else:
                #plt.title(prepared_plots[plot]["title"],fontdict=fontdict, y=1.+conf.title_and_axes_labelpad/(72.*fig.get_size_inches()[1]))
                plt.title(prepared_plots[plot]["title"],fontdict=fontdict, y=1.+conf.title_and_axes_labelpad/(72.*conf.figsize[1]))
    
        if "colors" in prepared_plots[plot]:
            colors=prepared_plots[plot]["colors"]
        else:
            colors=conf.colors
        

        should_be_legended="legends" in prepared_plots[plot]

        func_id, has_box_plots, other_legend_handles = plot_functions(prepared_plots[plot]["plot_functions"],colors,zeplt,should_be_legended=should_be_legended)

        if "twinx_plot_functions" in prepared_plots[plot]:

            # twinx_ax.tick_params(
            #     axis='y',          # changes apply to the y-axis
            #     which='both',      # both major and minor ticks are affected
            #     # pad=conf.title_and_axes_labelpad,
            #     labelsize=60) # labels along the bottom edge are off
            #     # labelsize=conf.ticks_labels_font_size+extra_ytick_label_size) # labels along the bottom edge are off

            if "y_ticks" in prepared_plots[plot]:
                ticks=prepared_plots[plot]["y_ticks"]
                for key in ticks:
                    if "params" in ticks[key]:
                        zeplt.tick_params(axis='y',which=key,**ticks[key]["params"])

            first_twinx_lines, first_twinx_labels = plt.gca().get_legend_handles_labels()
            # lines, labels = zeplt.get_legend_handles_labels()

            twinx_ax = plt.gca().twinx()

            if "twin_axis_label" in prepared_plots[plot]:
                twinx_ax.set_ylabel(prepared_plots[plot]["twin_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font) 


            func_id2, has_box_plots2, other_legend_handles2= plot_functions(prepared_plots[plot]["twinx_plot_functions"],colors,zeplt,should_be_legended=should_be_legended)
            has_box_plots= (has_box_plots or has_box_plots2)

            other_legend_handles+=other_legend_handles2
        
        #ticks
        extra_xtick_label_size=0
        if "extra_xtick_label_size" in prepared_plots[plot]:
            extra_xtick_label_size=prepared_plots[plot]["extra_xtick_label_size"]
        extra_ytick_label_size=0
        if "extra_ytick_label_size" in prepared_plots[plot]:
            extra_xtick_label_size=prepared_plots[plot]["extra_ytick_label_size"]   
                 
        #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html#matplotlib.axes.Axes.tick_params
        #default tick params
        zeplt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top=False,#'off',         # ticks along the top edge are off
            labelbottom='on',
            # pad=conf.title_and_axes_labelpad, #label pad
            labelsize=conf.ticks_labels_font_size+extra_xtick_label_size) # labels along the bottom edge are off
            
        zeplt.tick_params(
            axis='y',          # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            # pad=conf.title_and_axes_labelpad,
            labelsize=conf.ticks_labels_font_size+extra_ytick_label_size) # labels along the bottom edge are off
        
        #tick and labels
        if "x_ticks" in prepared_plots[plot]:
            ticks=prepared_plots[plot]["x_ticks"]
            for key in ticks:
                if "params" in ticks[key]:
                    zeplt.tick_params(axis='x',which=key,**ticks[key]["params"])
                if "range_step" in ticks[key]:
                    plt.gca().xaxis.set_ticks(np.arange(ticks[key]["from"],ticks[key]["to"],ticks[key]["range_step"]),minor=(key=="minor"))
                elif "positions" in ticks[key]:
                    plt.gca().xaxis.set_ticks(ticks[key]["positions"],minor=(key=="minor"))

                if "scalar" in ticks[key]:
                    mike=ScalarFormatter()
                    mike.set_powerlimits((-3, 4))
                    if key=="minor":
                        plt.gca().xaxis.set_minor_formatter(mike)
                    else:
                        plt.gca().xaxis.set_major_formatter(mike)
                    plt.gca().xaxis.get_offset_text().set_fontsize(conf.ticks_labels_font_size+extra_xtick_label_size)

                if "labels" in ticks[key]:
                    plt.gca().xaxis.set_ticklabels(ticks[key]["labels"],minor=(key=="minor"),fontsize=conf.ticks_labels_font_size+extra_xtick_label_size)
                else:
                    if has_box_plots:
                        plt.gca().xaxis.set_ticklabels([]) 
        
        if "y_ticks" in prepared_plots[plot]:
            ticks=prepared_plots[plot]["y_ticks"]
            for key in ticks:
                if "range_step" in ticks[key]:
                    plt.gca().yaxis.set_ticks(np.arange(ticks[key]["from"],ticks[key]["to"],ticks[key]["range_step"]),minor=(key=="minor"))
                elif "positions" in ticks[key]:
                    plt.gca().yaxis.set_ticks(ticks[key]["positions"],minor=(key=="minor"))

                if "scalar" in ticks[key]:
                    mike=ScalarFormatter()
                    mike.set_powerlimits((-3, 4))
                    if key=="minor":
                        plt.gca().yaxis.set_minor_formatter(mike)
                    else:
                        plt.gca().yaxis.set_major_formatter(mike)
                    plt.gca().yaxis.get_offset_text().set_fontsize(conf.ticks_labels_font_size+extra_ytick_label_size)

                if "labels" in ticks[key]:
                    plt.gca().yaxis.set_ticklabels(ticks[key]["labels"],minor=(key=="minor"),fontsize=conf.ticks_labels_font_size+extra_ytick_label_size)
                    
                if "params" in ticks[key]:
                    zeplt.tick_params(axis='y',which=key,**ticks[key]["params"])

        for axis in ['top','bottom','left','right','polar', 'start', 'end', 'inner']:
            if axis in plt.gca().spines: 
                plt.gca().spines[axis].set_linewidth(conf.general_plots_linewidth/2)
                
        
        #lims
        if "xmin" in prepared_plots[plot]:
            plt.xlim(xmin=prepared_plots[plot]["xmin"])
        if "xmax" in prepared_plots[plot]:
            plt.xlim(xmax=prepared_plots[plot]["xmax"])
        if "ymin" in prepared_plots[plot]:
            plt.ylim(ymin=prepared_plots[plot]["ymin"])
        if "ymax" in prepared_plots[plot]:
            plt.ylim(ymax=prepared_plots[plot]["ymax"])
        
        #projection polar
        if 'axes_projection' in prepared_plots[plot]:
            if prepared_plots[plot]['axes_projection']=='polar':
                plt.gca().set_thetamin(0)
                plt.gca().set_thetamax(360)
                plt.gca().set_rmax(60)
                plt.gca().set_rmin(0)
                
                plt.tick_params(
                    axis='both',          # changes apply to the y-axis
                    which='both',      # both major and minor ticks are affected
                    pad=conf.title_and_axes_labelpad,
                )

            if prepared_plots[plot]['axes_projection']=='mollweide':
                plt.tick_params(
                    axis='both',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,         # ticks along the top edge are off
                    right=False,         # ticks along the top edge are off
                    # labelbottom=False # labels along the bottom edge are off
                    )


        if "theta_min" in prepared_plots[plot]:
            plt.gca().set_thetamin(prepared_plots[plot]["theta_min"]/np.pi*180)
        if "theta_max" in prepared_plots[plot]:
            plt.gca().set_thetamax(prepared_plots[plot]["theta_max"]/np.pi*180)
        if "rmin" in prepared_plots[plot]:
            plt.gca().set_rmin(prepared_plots[plot]["rmin"])
        if "rmax" in prepared_plots[plot]:
            plt.gca().set_rmax(prepared_plots[plot]["rmax"])
            
        
        #legends
        if "legends" in prepared_plots[plot]:
            leg=None
            leg_loc='best' #upper right
            
            legend_labels_font_size=prepared_plots[plot]["legends"]["legend_labels_font_size"] if "legend_labels_font_size"  in prepared_plots[plot]["legends"] else conf.legend_labels_font_size      
            legend_markerscale=prepared_plots[plot]["legends"]["legend_markerscale"] if "legend_markerscale"  in prepared_plots[plot]["legends"] else conf.legend_markerscale
            legend_linewidth=prepared_plots[plot]["legends"]["legend_linewidth"] if "legend_linewidth"  in prepared_plots[plot]["legends"] else conf.legend_linewidth
            legend_border_width=prepared_plots[plot]["legends"]["legend_border_width"] if "legend_border_width"  in prepared_plots[plot]["legends"] else conf.legend_border_width
            legend_border_color=prepared_plots[plot]["legends"]["legend_border_color"] if "legend_border_color"  in prepared_plots[plot]["legends"] else conf.legend_border_color

            legend_bbox_to_anchor=prepared_plots[plot]["legends"]["bbox_to_anchor"] if "bbox_to_anchor"  in prepared_plots[plot]["legends"] else (0,0,1,1)
            legend_args=prepared_plots[plot]["legends"]["legend_args"] if "legend_args"  in prepared_plots[plot]["legends"] else {}
                
            if "legend_loc"  in prepared_plots[plot]["legends"]:
                leg_loc=prepared_plots[plot]["legends"]["legend_loc"]
            if "italic_legends" in prepared_plots[plot]["legends"] and prepared_plots[plot]["legends"]["italic_legends"]:
                rcParams['font.style'] = 'italic'

            if "manual_legends" in prepared_plots[plot]["legends"]:  
                other_legend_handles+=prepared_plots[plot]["legends"]["manual_legends"]

            myhandles, mylabels = plt.gca().get_legend_handles_labels()
            if "twinx_plot_functions" in prepared_plots[plot]:
                myhandles+=first_twinx_lines
                mylabels+=first_twinx_labels

            if len(myhandles)!=0:
                other_legend_handles+=myhandles

            if len(other_legend_handles)>0:
                leg=zeplt.legend(
                    handles=other_legend_handles,
                    fontsize=legend_labels_font_size,
                    markerscale=legend_markerscale, 
                    loc=leg_loc,
                    bbox_to_anchor=legend_bbox_to_anchor,
                    **legend_args)
            
            if "italic_legends" in prepared_plots[plot]["legends"] and prepared_plots[plot]["legends"]["italic_legends"]:
                rcParams['font.style'] = 'normal'
                if leg:
                    for legend_element in leg.legendHandles:
                        legend_element.set_linewidth(legend_linewidth)   
            
            if leg:   
                leg.get_frame().set_linewidth(legend_border_width)
                leg.get_frame().set_edgecolor(legend_border_color)

            other_legend_handles=[]
            
        
        if "grid" in prepared_plots[plot]:
            zeplt.grid(**prepared_plots[plot]["grid"])
            plt.gca().set_axisbelow(True)
        
        if "axis_off" in prepared_plots[plot] and prepared_plots[plot]["axis_off"]:
            plt.gca().set_axis_off()
            #zeplt.gca().xaxis.set_visible(False)

        if "zoom_bbox" in prepared_plots[plot]:

            propx0,propx1,propy0,propy1=prepared_plots[plot]["zoom_bbox"]

            plt.gca().xaxis.set_ticklabels([]) 
            plt.gca().xaxis.label.set_visible(False)

            r = plt.gcf().canvas.get_renderer()#.get_renderer()
            mike=plt.gca().get_tightbbox(r)#,bbox_extra_artists=[])
            extent = plt.gca().get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted())

            oriposi=plt.gca().get_position(original=True)
            delta_x=extent.x1-extent.x0
            delta_y=extent.y1-extent.y0

            extent.x0=extent.x0+propx0*delta_x
            extent.x1=extent.x1+propx1*delta_x
            extent.y0=extent.y0+propy0*delta_y
            extent.y1=extent.y1+propy1*delta_y

            # plt.gca().figure.savefig('tototu.png',format="png", dpi=2000, bbox_inches=extent)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=min(prepared_plots[plot]["zoom_bbox_dpi"],10000/(delta_x*delta_y)**(1/2)) , bbox_inches=extent)# limit to reasonable dpi
            buf.seek(0)

            current_ax=plt.gca()

            inax_x_label_offset=0
            inax_y_label_offset=0.02
            inax_w_label_offset=-0.02 # potential side/color bar
            inax_h_label_offset=-0.03
            if 'axes_projection' in prepared_plots[plot]:
                if prepared_plots[plot]['axes_projection']=='mollweide':
                    inax_x_label_offset=0
                    inax_y_label_offset=0.02
                    inax_w_label_offset=-0.02
                    inax_h_label_offset=0

            # rect = (0.01, 0.01, .98, .98)
            # rect = (0.01, 0.12, .98, .86)
            rect=(oriposi.x0+inax_x_label_offset,oriposi.y0+inax_y_label_offset,oriposi.x1-oriposi.x0+inax_w_label_offset,oriposi.y1-oriposi.y0+inax_h_label_offset)

            ax2 = plt.Axes(plt.gcf(), rect)
            plt.gcf().add_axes(ax2)

            # ax.set_axis_off()
            # current_ax.set_visible(False)
            current_ax.remove()

            im = plt.imread(buf)
            buf.close()

            implot = ax2.imshow(im,**({"origin":"upper", "aspect":"auto", "interpolation":'spline36'}))

            if "x_axis_label" in prepared_plots[plot]:
                fontdict={'fontsize': conf.title_font_size,'verticalalignment': 'baseline','horizontalalignment': "center"}        
                plt.xlabel(prepared_plots[plot]["x_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)

            ax2.yaxis.set_ticklabels([]) 
            ax2.xaxis.set_ticklabels([]) 
            ax2.yaxis.set_ticks([]) 
            ax2.xaxis.set_ticks([]) 
            
            for child in ax2.get_children():
                if isinstance(child, mpl_spines.Spine):
                    # child.set_color('#dddddd')  #grey    
                    child.set_color('white')      


        #MUST BE LAST BECAUSE NEW AXES ARE CREATED
        if "side_bar" in prepared_plots[plot]:
            #print(prepared_plots[plot]["color_bar"])
            location="right"
            if "location" in prepared_plots[plot]["side_bar"]:
                location=prepared_plots[plot]["side_bar"]["location"]
                
            sb_size="5%"
            if "sb_size" in prepared_plots[plot]["side_bar"]:
                sb_size=prepared_plots[plot]["side_bar"]["sb_size"]
                                
            sb_pad="3%"
            if "sb_pad" in prepared_plots[plot]["side_bar"]:
                sb_pad=prepared_plots[plot]["side_bar"]["sb_pad"]

            divider = make_axes_locatable(plt.gca())
            # ax2 = divider.new_vertical("5%", pad="3%",axes_class=maxes.Axes)
            ax2 = divider.append_axes(location, sb_size, pad=sb_pad ,axes_class=maxes.Axes)
            # ax2 = divider.append_axes(location, "5%", pad="3%")
            
            sideplots=prepare_plots({0:prepared_plots[plot]["side_bar"]})
            plot_indivs(sideplots,in_ax=ax2)

                    
        #MUST BE LAST BECAUSE NEW AXES ARE CREATED
        elif "color_bar" in prepared_plots[plot]:
            #print(prepared_plots[plot]["color_bar"])
            location="right"
            if "location" in prepared_plots[plot]["color_bar"]:
                location=prepared_plots[plot]["color_bar"]["location"]

            cb_size="5%"
            if "cb_size" in prepared_plots[plot]["color_bar"]:
                cb_size=prepared_plots[plot]["color_bar"]["cb_size"]
                                
            cb_pad="3%"
            if "cb_pad" in prepared_plots[plot]["color_bar"]:
                cb_pad=prepared_plots[plot]["color_bar"]["cb_pad"]   
            
            color_list=conf.colorbar_colors
            color_bounds=np.array([])
            if "color_list" in prepared_plots[plot]["color_bar"]:
                color_list=prepared_plots[plot]["color_bar"]["color_list"]
            if "color_bounds" in prepared_plots[plot]["color_bar"]:
                color_bounds=np.array(prepared_plots[plot]["color_bar"]["color_bounds"])
            else:
                if "default_bounds" in prepared_plots[plot]["color_bar"] and prepared_plots[plot]["color_bar"]["default_bounds"]:
                    color_bounds=np.array(conf.colorbar_color_bounds)
                else:
                    color_bounds=np.linspace(0,1,len(color_list)+1,endpoint=True)
                    
            decade = 10**2#two decimals
            color_bounds=np.trunc(color_bounds*decade)/decade
                
            divider = make_axes_locatable(plt.gca())
            ax2 = divider.append_axes(location, cb_size, pad=cb_pad ,axes_class=maxes.Axes)
            #zeplt.colorbar(im, cax=cax)
            
            
            
            # Set the colormap and norm to correspond to the data for which
            # the colorbar will be used.
            cmap = mpl_colors.ListedColormap(color_list)#['r', 'orange', 'b', 'g'])
            color_bounds_crop=color_bounds[:cmap.N]
            color_bounds_crop=np.append(color_bounds_crop,1.)
            norm = mpl_colors.BoundaryNorm(color_bounds_crop, cmap.N)
            cb2 = mpl_colorbar.ColorbarBase(ax2, cmap=cmap,
                                            norm=norm,
                                            # to use 'extend', you must
                                            # specify two extra boundaries:
                                            boundaries=color_bounds_crop,
                                            #extend='both',
                                            ticks=color_bounds_crop,  # optional
                                            spacing='proportional',
                                            #orientation='vertical',
                                            #**kw
                                            )
            cb2.ax.tick_params(labelsize=conf.ticks_labels_font_size)
            #Label
            if "label" in prepared_plots[plot]["color_bar"]:
                cb2.set_label(prepared_plots[plot]["color_bar"]["label"])
            if "xlabel" in prepared_plots[plot]["color_bar"]:                
                cb2.ax.set_xlabel(prepared_plots[plot]["color_bar"]["xlabel"])
            if "title" in prepared_plots[plot]["color_bar"]:                
                cb2.ax.set_title(prepared_plots[plot]["color_bar"]["title"])
                    

        
        
        if not from_page and "tight_layout" in prepared_plots[plot] and prepared_plots[plot]["tight_layout"]:
            plt.tight_layout()

        if file_to_save and format_to_save:
            path_to_save=file_to_save
            if dir_to_save:
                path_to_save=dir_to_save+"/"+path_to_save
                if not os.path.exists(dir_to_save):
                    os.makedirs(dir_to_save)
            plt.savefig(path_to_save,format=format_to_save, dpi=user_defined_dpi,bbox_inches='tight')
            # plt.savefig(path_to_save,format=format_to_save, dpi=user_defined_dpi)
        elif (not from_page) and "file_to_save" in prepared_plots[plot] and "format_to_save" in prepared_plots[plot]:
            path_to_save=prepared_plots[plot]["file_to_save"]
            if "dir_to_save" in prepared_plots[plot]:
                path_to_save=prepared_plots[plot]["dir_to_save"]+"/"+path_to_save
                if not os.path.exists(prepared_plots[plot]["dir_to_save"]):
                    os.makedirs(prepared_plots[plot]["dir_to_save"])
            plt.savefig(path_to_save,format=prepared_plots[plot]["format_to_save"], dpi=user_defined_dpi)
        if PDF_to_add:
            plt.savefig(PDF_to_add,format="pdf", dpi=user_defined_dpi)
        if show:
            zeplt.show()
        else:
            if not (from_page or has_predef_axes):
                zeplt.close()
            
            
                
            
def plot_pages(
    prepared_plots, nb_plots_hor=3, nb_plots_vert=2, grid_specs=[], show=False,
    file_to_save=None,format_to_save=None,dir_to_save=None,
    PDF_to_add=None, user_defines_size=False,user_defined_size=conf.figsize,user_defined_dpi=conf.dpi,
    page_info="",
    user_defined_tlfs=-1,
    user_defined_alfs=-1
    ):
    
    global plot_has_been_shown
    
    if show:
        conf.set_fig("plot_show","landscape",nb_column_width=1)
        
    conf.update(max(nb_plots_vert,nb_plots_hor))

    if user_defines_size:
        conf.set_figsize(user_defined_size)

    if user_defined_tlfs!=-1:
        conf.update_ticks_labels_font_size(user_defined_tlfs)

    if user_defined_alfs!=-1:
        conf.update_axes_labels_font_size(user_defined_alfs)

    axes={}

    plots_per_grid=len(grid_specs)
    page_grid=grid_specs[:]
    if plots_per_grid==0:#no spec: isogrid 
        plots_per_grid=nb_plots_vert*nb_plots_hor
        for row in range(nb_plots_vert):
            for col in range(nb_plots_hor):
                page_grid.append((row,col))

    nb_pages=int(len(prepared_plots)/(plots_per_grid))
    if len(prepared_plots)%(plots_per_grid)!=0:
        nb_pages+=1        
    
    sppk=sorted(prepared_plots.keys())
    
    for page_id in range(nb_pages):
        print("setting page {0}/{1}... {2}".format(page_id+1,nb_pages,page_info))
        
        pfig=plt.figure(num=page_id, figsize=conf.figsize, dpi=user_defined_dpi)
        gs = pfig.add_gridspec(nb_plots_vert, nb_plots_hor)
        
        for plot_index in range(len(sppk)):
            plot=sppk[plot_index]
            # print(prepared_plots[plot])
            page=int(plot_index/plots_per_grid)
            plot_id=plot_index%(plots_per_grid)
            if page>page_id:
                break
            if page==page_id:
                if 'axes_projection' in prepared_plots[plot]:
                    if prepared_plots[plot]['axes_projection']=='polar':
                        axes[plot]=pfig.add_subplot(gs[page_grid[plot_id]],polar=True)
                    elif prepared_plots[plot]['axes_projection']=='mollweide':
                        axes[plot]=pfig.add_subplot(gs[page_grid[plot_id]],projection="mollweide")
                else:
                    axes[plot]=pfig.add_subplot(gs[page_grid[plot_id]],polar=False)
                
                if plot in prepared_plots:
                    plot_indivs({0:dict(prepared_plots[plot])},show=False,file_to_save=None,dir_to_save=None,PDF_to_add=None, from_page=True)
                else:
                    plt.plot(np.log(range(1,10)))
            
                try:
                    if (
                        not ("zoom_bbox" in prepared_plots[plot]) 
                        and not ("tight_layout" in prepared_plots[plot] and not prepared_plots[plot]["tight_layout"])):
                        if 'axes_projection' in prepared_plots[plot]: ##labels seem not to be considered by tight_layout in that case
                            plt.tight_layout(w_pad=1.5, h_pad=1.5)
                        elif 'no_padding' in prepared_plots[plot]:
                            plt.tight_layout(w_pad=0, h_pad=0, pad=0.)
                        else:
                            layout_padding=prepared_plots[plot]["layout_padding"] if "layout_padding" in prepared_plots[plot] else {}
                            plt.tight_layout(**layout_padding)
                except:
                    print("Tight Layout failed for page {0} plot {1}".format(page_id+1,plot_id))

                    # error:
                    # File "/home/guigui/anaconda3/lib/python3.7/site-packages/matplotlib/tight_layout.py", line 255, in get_subplotspec_list
                    # axes_or_locator ====> <mpl_toolkits.axes_grid1.axes_divider.AxesLocator object at 0x7fb2deca7400>
                    # subplotspec = axes_or_locator.get_subplotspec() =======> None
                    # subplotspec = subplotspec.get_topmost_subplotspec()
                    # AttributeError: 'NoneType' object has no attribute 'get_topmost_subplotspec'                    

            
        if file_to_save and format_to_save:
            path_to_save=file_to_save+'_{0}.{1}'.format(page_id,format_to_save)
            if dir_to_save:
                path_to_save=dir_to_save+"/"+path_to_save
                if not os.path.exists(dir_to_save):
                    os.makedirs(dir_to_save)
            plt.savefig(path_to_save,format=format_to_save, dpi=user_defined_dpi,bbox_inches='tight')
            # plt.savefig(path_to_save,format=format_to_save, dpi=user_defined_dpi)
        if PDF_to_add:
            plt.savefig(PDF_to_add,format="pdf", dpi=user_defined_dpi)
        if show:
            if not plot_has_been_shown:
                plot_has_been_shown=True
                plt.ion()
                plt.show()
                plt.pause(0.2)
                plt.pause(0.2)
                plt.clf()
            else:
                plt.draw()
                plt.pause(0.2)
                plt.clf()
        else:
            plt.close()
        
        axes={}        
        
#         try:
#             plt.savefig("totototo{0}.png".format(page_id))
#         except RuntimeError:
#             plt.savefig("totototo{0}.pdf".format(page_id),format='pdf')
#         plt.close()
#                 
#         
#     



def docu(specific_infos={},print_all=False,detailed=False):

    if len(specific_infos)==0:
        print("plot parameters:")
        for elt in plot_params:
            print(elt)
            print(plot_params[elt])
        print("function parameters:")   
        for elt in plot_types:
            print(elt)
            print(function_params[elt])
            if print_all:
                for func_param in args_params[elt]:
                    print(func_param)
                    print(args_params[elt][func_param])
    else:
        for requested in specific_infos:
            if requested=="list":
                print(plot_params.keys())
                print(plot_types)
            else:
                if requested in plot_params:
                    print(requested)
                    print(plot_params[requested])
                if requested in plot_types:
                    print(requested)
                    print(function_params[requested])
                    for elt in specific_infos[requested]:
                        if elt in args_params[requested]:
                            print('{0}: {1}'.format(elt,args_params[requested][elt]))
                if detailed:
                    if requested in details["plot_params"]:
                        print('Details on {0} plot_param: {1}'.format(requested, details["plot_params"][requested]))
                    if requested in plot_types:
                        print('Details on {0} {1}:'.format(requested, "func_params"))
    #                     for elt in details["func_params"][requested]:
    #                         print('{0}: {1}'.format(elt, details["func_params"][requested][elt]))
                        for elt in specific_infos[requested]:
    #                         if elt in args_params[requested]:
    #                             print('{0}: {1}'.format(elt,args_params[requested][elt]))
                            if elt in details["func_params"][requested]:
                                print('{0}: {1}'.format(elt,details["func_params"][requested][elt]))    
                            if elt=="list":
                                print(details["func_params"][requested].keys())   
                            
            print("\n")



if __name__ == '__main__':
    
#     conf.set_fig("Springer_journal", "landscape", 3)
#     conf.update()
    conf.set_fig("A4", "landscape")
    conf.update()
    
    
    #docu({"plot":{"type","color_index","list"},"x_axis_label":{}},detailed=True)
    
    legend_example=[]
    legend_example.append(mpl_lines.Line2D([],[],color='k',marker='+',linestyle='',fillstyle='none',mew=0.6,ms=8,label='bolos'))
    
    some_data={
        0:{"values":{
                0:{"type":"plot","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0','marker':'x','markersize':3},
                1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, },
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"the title of the plot",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
        42:{"values":{
                0:{"type":"plot","y_values":4000*(-3.2-.46*np.log(.00001+np.sinc((0.0003*np.arange(1,10000))**6)**2)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":10000*np.sin(np.linspace(1,10000,9)),"x_values":range(10000,1000,-1000),"linestyle":'--'},},
            "y_ticks":{"major":{"scalar":True}},    
            "xmin":3000,
            "ymin":-10200,                        
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.tif",
            "format_to_save":"tif", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "x_axis_label":"x label",
            "y_axis_label":"y label",
            "tight_layout":True,
            "title":"long axes - scalar y",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "side_bar":{"values":{0:{"type":"scatter",'x_values':[0,-.25,.25,.5,0],'y_values':[1,3,7,15,25], 'color':["red","blue","green","orange","purple"], 's':90, "marker":'*'}}, 
                      "xmin":-.5,
                      "xmax":.5,
                      "ymin":-1,          
                      "ymax":27,
                      "y_axis_label":"side bar plot label",
                      "x_axis_label":"Val",
                      "title":"side title",
                      "sb_size":"30%",
                      "sb_pad":"10%"
                  }},
        143:{"values":{
                0:{"type":"plot","y_values":4000*(-3.2-.46*np.log(.00001+np.sinc((0.0003*np.arange(1,10000))**6)**2)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":10000*np.sin(np.linspace(1,10000,9)),"x_values":range(10000,1000,-1000),"linestyle":'--'},},
            "zoom_bbox":(-0.066,-0.9,0.1,-0.55),    
            "zoom_bbox_dpi":200,
            "y_ticks":{"major":{"scalar":True}},    
            "xmin":3000,
            "ymin":-10200,                        
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.tif",
            "format_to_save":"tif", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "x_axis_label":"x label",
            "y_axis_label":"y label",
            "title":"long axes - scalar y",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "side_bar":{"values":{0:{"type":"scatter",'x_values':[0,-.25,.25,.5,0],'y_values':[1,3,7,15,25], 'color':["red","blue","green","orange","purple"], 's':90, "marker":'*'}}, 
                      "xmin":-.5,
                      "xmax":.5,
                      "ymin":-1,          
                      "ymax":27,
                      "y_axis_label":"side bar plot label",
                      "x_axis_label":"Val",
                      "title":"side title",
                      }},                              
        20:{"values":{
                0:{"type":"plot","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1], "linewidth":3}},
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"plot",
            "legends":{"manual_legends":legend_example},
            "no_padding":True, #for all plots in page being its last
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
        21:{"values":{
                0:{"type":"semilogx","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, },
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"semilogx and plot",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{
                "default_bounds":True,
                "color_list":["red","green","blue","purple","k","yellow","cyan"],
                "cb_size":"30%",
                "cb_pad":"10%"
            }},
        22:{"values":{
                0:{"type":"semilogy","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, },
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"semilogy and plot",
            "legends":{"manual_legends":legend_example},
            "x_ticks":{"major":{"params":{"pad":15,"length":15}}},
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
        23:{"values":{
                0:{"type":"loglog","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, },
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example1.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"loglog and plot",
            "titlepad":30,
            "legends":{
            	"manual_legends":legend_example,
                "legend_loc":"center",
                "legend_labels_font_size":13, 
                "legend_args":{"handlelength":4,"labelspacing":3,"ncol":5},
                "bbox_to_anchor":(0.51,1.08),
            },            
            "layout_padding":{"w_pad":0, "h_pad":2, "pad":5}, #inter plot in weight, inter plot in height, plot(s) to page for all plots in page being its last
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
        4:{"values":{
                3:{"type":"imshow","matrix_colors":[([0.3, 0.4, 1], [0.0, 0.0, 0.0]),([0.3, 1, 1], [0.3, 0.3, 1])]},
                4:{"type":"hline","y_pos":4.4, 'x_axis_prop_range':[0.1,0.6], 'color_index':0,"color":"red", "linewidth":4., "solid_capstyle":'round'},
                5:{"type":"hspan","y_min":1.7, "y_max":3.7, 'x_axis_prop_range':[0.1,0.6]},
                6:{"type":"bar","center":6.7, 'height':2., 'width':1.5, "bottom":1., "color":"red", "linewidth":4.,"edgecolor":'none'},
                7:{"type":"bar","center":4.75, 'height':1., 'width':1, "bottom":0.25, "color":"green", "linewidth":0.02,"edgecolor":'green',"facecolor":'none'},},
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example2.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"the title of the plot",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True}},
        5:{"values":{
                7:{"type":"text","x":3, 'y':4., "text":"Bonzai", "va":'center', "ha":'center',"bbox":dict(boxstyle="round4", fc="None", ec="blue")},
                8:{"type":"text","x":2, 'y':4.5, "text":"Bonzai",},
                9:{"type":"annotate","text":"Bonzai annotated","pos":(4.,4.)},},
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example3.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"the title of the plot",
            "legends":{"manual_legends":legend_example},
            "grid":{"which":'major',"axis":"both"},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]},
            "xmax":10,
            "ymax":10},
        6:{"values":{#10:{"type":"table","rows":['1', '2','3'], 'cols':['a', 'b'], "matrix":[['1a', '1b'], ['2a', '2b'], ['3a', '3b']],"line_width_prop":0.5,"col_height_prop":0.5}},
                11:{"type":"table","rows":['1', '2','3'], 'cols':['a', 'b'], "matrix":[['1a', '1b'], ['2a', '2b'], ['3a', '3b']],
                       "line_width_prop":0.5,"col_height_prop":0.5,"label_params":{"ylab_height_prop":0.1, "edges_off":True}}},
            "colors":["red","green","blue"],
            "plot_types":"example",
            "file_to_save":"example4.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"y label",
            "x_axis_label":"th x lbel",
            "title":"the title of the plot",
            "legends":{"manual_legends":legend_example},
            "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
        1:{"values":{
                0:{"type":"scatter",'x_values':[5,6,7],'y_values':[1,5,2], 'color_index':0, 's':60, 'legend':'black 128'},
                1:{"type":"scatter",'x_values':[4,5,3],'y_values':[1.5,5.5,1.6], 'color_index':1, 's':90, "marker":r'$\beta$', 'legend':'red scatter, no?'}}, 
            "plot_types":"scatter",
            "file_to_save":"scatter_example.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"scat y label",
            "x_axis_label":"scat x lbel",
            "title":"double scatter example 1",
            "legends":{"italic_legends":True}},
        2:{"values":{
                0:{"type":"boxplot",'x_values':[5,6,7],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.7, "color":"green", "linewidth":3., 'fill':True, 'legend':'AHAHAH?'},
                1:{"type":"boxplot",'x_values':[1,2,3],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.37, "color":"purple", 'legend':'red, no?'}, 
                2:{"type":"boxplot",
                    'x_values':[9,10,11],
                    'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                    'whis':(5,95), 
                    "showfliers":True,
                    "showcaps":False,
                    "manage_ticks":False, 
                    'x_size':0.7,                    
                    "fliersize":4.4,
                    "linewidth":2.2,
                    "box_edge_width":3.5,
                    "fill_map":(0,10),
                    "clip_on_box":True,                                
                    "color":'black',
                    },
                3:{"type":"boxplot",
                    'x_values':[13,14,15],
                    'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                    'whis':1.5, 
                    'x_size':0.7,                    
                    "fill_map":(0,30),
                    "cmap_list":conf.colorbar_colors[:-1],
                    "linestyle":':',
                    "linewidth":1.2,
                    },
                4:{"type":"boxplot",
                    'x_values':[17,18,19],
                    'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                    'whis':1.5, 
                    'x_size':0.7,                    
                    "fill_map":(0,30),
                    "clip_on_box":True,                                
                    "cmap_list":conf.colorbar_colors[:-1],
                    "linestyle":':',
                    "linewidth":1.2,
                    }},                            
            "plot_types":"boxplot",
            "file_to_save":"boxplot_example.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"bop y label",
            "x_axis_label":"ejhsrguezv x lbel",
            "title":"double boxplot example",
            "legends":{"italic_legends":True},
            "x_ticks":{"major":{"range_step":1, "from":1, "to":8,
                              "labels":["b",'a',2]+['']*4,
                              "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}},
                     "minor":{"range_step":1, "from":1.5, "to":8.5,
                              "labels":["c",'d',1]+['']*4,
                              "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}}},
            "y_ticks":{"major":{"positions":[3],
                              "labels":["baa"],
                              "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}},
                     "minor":{"positions":[4.5],
                              "labels":["ckzUGF"],
                              "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}}},
            "xmax":20,
            "ymax":20,
            "tight_layout":True},
        3:{"values":{
                0:{"type":"scatter",'x_values':[5,6,7],'y_values':[1,5,2], 'color_index':0, 'legend':'black 128'},
                1:{"type":"scatter",'x_values':[4,5,3],'y_values':[1.5,5.5,1.6], 'color_index':1, 'legend':'red scatter, no?'},
                2:{"type":"boxplot",'x_values':[5,6,7],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.7, 'fill':True, 'legend':'AHAHAH?'},
                3:{"type":"boxplot",'x_values':[1,2,3],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.37, "color":"purple", 'legend':'red, no?'},
                4:{"type":"plot","y_values":np.log(range(1,10))}}, 
            "plot_types":"multi",
            "file_to_save":"multi_example.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"scat y label",
            "x_axis_label":"scat x lbel",
            "title":"double scatter example 2",
            "legends":{"italic_legends":True,
                     "legend_loc":"best"}, #right, center left, upper right, lower right, best, center, lower left, center right, upper left, upper center, lower center
            "x_ticks":{"major":{"range_step":1, "from":0, "to":10}},
            "axis_off":True},
        10:{"values":{
                0:{"type":"annotate","text":"","pos":(3.,3.),'xytext':(6.3,6.3), 'horizontalalignment':'center', 'label':"Nice arrow",
                    "arrowprops":dict(arrowstyle="-|>,head_width=.6, head_length=1.2",connectionstyle="arc3,rad=0.4",
                        lw=3.5,#*nodeid, 
                        fc="purple", 
                        ec="green",
                        shrinkA=0,
                        shrinkB=8,
                        
                        ls="solid",
                        zorder=10
                        ),
                    "color":"orange"}}, 
            "plot_types":"as:kjghzlrbg",
            "file_to_save":"arrow.png",
            "format_to_save":"png", ##png, pdf, ps, eps or svg.
            "dir_to_save":"test_plots_gen",
            "y_axis_label":"arrow y label",
            "x_axis_label":"arrow x lbel",
            "title":"Jack Sp(ecial) arrow example",
            "xmax":10,
            "ymax":10,
            "legends":{"italic_legends":True,"legend_linewidth":3.}},}
    some_data[27]={"values":{
            0:{"type":"plot","y_values":[0, 20, 15], "x_values":[0,np.pi/4,np.pi/8],  'color':'purple', "linewidth":4., 'legend':'plot proj polar'},
            1:{"type":"plot","y_values":20+10*np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
            2:{"type":"polar","r_values":[0, 20, 15], "theta_values":[0,np.pi/4+1,np.pi/8+1],  'color_index':1, "linewidth":4., 'legend':'plt.polar'},
        }, 
        "plot_types":"aekufhqilruy",
        "axes_projection":"polar",
        "title":"Polar plots",
        "theta_min":-np.pi/4, 
        "theta_max":np.pi/2+1.,
        "rmax":50,
    }

    some_data[26]={
        "axes_projection":"polar",
        "rmax":7,
        "values":{
            0:{"type":"scatter",'x_values':[5,6,7],'y_values':[1,5,2], 'color_index':0, 'legend':'black 128'},
            1:{"type":"scatter",'x_values':[4,5,3],'y_values':[1.5,5.5,1.6], 'color_index':1, 'legend':'red scatter, no?'},
            2:{"type":"boxplot",'x_values':[5,6,7],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.7, 'fill':True, 'legend':'AHAHAH?'},
            3:{"type":"boxplot",'x_values':[1,2,3],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.37, "color":"purple", 'legend':'red, no?'},
            4:{"type":"plot","y_values":np.log(range(1,10))}}, 
        "plot_types":"multi",
        "file_to_save":"multi_example.png",
        "format_to_save":"png", ##png, pdf, ps, eps or svg.
        "dir_to_save":"test_plots_gen",
        "y_axis_label":"scat y label",
        "x_axis_label":"scat x lbel",
        "title":"double scatter example 2",
        "legends":{
            "italic_legends":True,
            "legend_loc":"best"}, #right, center left, upper right, lower right, best, center, lower left, center right, upper left, upper center, lower center
        "x_ticks":{"major":{"range_step":1, "from":0, "to":10}},
        "axis_off":True}

    some_data[25]={"values":{
            0:{"type":"violinplot",'x_values':[5,6,7],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.7, 
                "color":"green", "linewidth":3., 'fill':True, 'legend':'AHAHAH?'},
            1:{"type":"violinplot",'x_values':[1,2,3],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.37, 
                "color":"purple", 'legend':'red, no?',"violin_edge_width":8}, 
            2:{"type":"violinplot",
                'x_values':[9,10,11],
                'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                'x_size':0.7,                    
                "linewidth":2.2,
                "fill_map":(0,10),
                "indep_violin_fill":True,          #each violin has its own colormap                       
                "color":'black',
                },
            3:{"type":"violinplot",
                'x_values':[13,14,15],
                'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                'x_size':0.7,       #default same size if not custom
                'custom_x_size':{"delta_y":1},   #width of each violin as proportion of x_size w.r.t max numvals in y ranges of size delta_y
                "fill_map":(0,30),              #all violins share the same colormap
                "cmap_list":conf.colorbar_colors[:-1],
                "linestyle":':',
                "linewidth":1.2,
                },
            4:{"type":"violinplot",
                "bw_method":0.2, #default  'scott', 'silverman', scalar
                'x_values':[17,18,19],
                'y_sets': [[2,5,2],[3,7,2,15],[2,5,4]],
                'x_size':0.7,       
                'scattered':{'color':"orange", 's':50, "marker":'*'},        # dots. considers custom delta_y (or default 1, max 10 dots per row)
                "linewidth":1.2,
                'color':"blue",
                }},                            
        "plot_types":"violinplot",
        "file_to_save":"violinplot_example.png",
        "format_to_save":"png", ##png, pdf, ps, eps or svg.
        "dir_to_save":"test_plots_gen",
        "y_axis_label":"violinplot y label",
        "x_axis_label":"violin x lbel",
        "title":"multiple violinplot example",
        "legends":{"italic_legends":True},
        "x_ticks":{"major":{"range_step":1, "from":1, "to":8,
                          "labels":["b",'a',2]+['']*4,
                          "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}},
                 "minor":{"range_step":1, "from":1.5, "to":8.5,
                          "labels":["c",'d',1]+['']*4,
                          "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}}},
        "y_ticks":{"major":{"positions":[3],
                          "labels":["baa"],
                          "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}},
                 "minor":{"positions":[4.5],
                          "labels":["ckzUGF"],
                          "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}}},
        "xmax":20,
        "ymax":20,
        "tight_layout":True}            

    #twinx example
    some_data[44]={
        "values":{
            0:{"type":"plot","y_values":[0, 20, 15], "x_values":[0,np.pi/4,np.pi/8],  'color':'purple', "linewidth":4., 'legend':'plot'},
            1:{"type":"plot","y_values":20+10*np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
            9:{"type":"annotate","text":"4,4","pos":(4.,4.),"va":'center', "ha":'center', "color":'purple'},
        }, 
        "twinx_values":{
            0:{"type":"plot","y_values":[0, 20, 15], "x_values":[8,8-np.pi/4,8-np.pi/8],  'color':'red', "linewidth":4., 'legend':'twin'},
            9:{"type":"annotate","text":"4,4 twin","pos":(4.,4.),"va":'center', "ha":'center', 'color':'red'},
            # 1:{"type":"plot","y_values":20+10*np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
        },
        "plot_types":"aekufhqilruy",
        "title":"Twinx plots",        
        "legends":{"italic_legends":True},
    }

    #empty/blank plot
    some_data[45]={
        "values":{
        }, 
        "axis_off":True
    }

    len_data=len(some_data)
    some_data_keys=list(some_data.keys())
#    for plot_id in some_data_keys:
##        for val_id in some_data[plot_id]["values"]:
##            some_data[10*plot_id+val_id+len_data]=dict(some_data[plot_id])
##            some_data[10*plot_id+val_id+len_data]["side_bar"]=dict(some_data[plot_id])
#        some_data[10*plot_id+len_data]=dict(some_data[plot_id])
#        some_data[10*plot_id+len_data]["side_bar"]=dict(some_data[plot_id])
    
    prepared_plots=prepare_plots(some_data)
    plot_indivs(prepared_plots,show=False,file_to_save=None,dir_to_save=None,PDF_to_add=None,user_defined_dpi=100)

    pp1 = PdfPages('plottings.pdf')
    plot_pages(prepared_plots, nb_plots_hor=2, nb_plots_vert=2, grid_specs=[(0,slice(None,None)),(1,0),(1,1)], show=False, file_to_save="plottings", format_to_save='svg', dir_to_save="test_plots_gen", PDF_to_add=pp1,user_defined_dpi=100)
    pp1.close()
    
