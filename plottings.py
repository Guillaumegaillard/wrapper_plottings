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
from mpl_toolkits.axes_grid1 import make_axes_locatable




#from wrapper_plottings 
try:
	from . import config_plottings as conf
except ImportError:
	import config_plottings as conf



""" DOCUMENTATION PARAMETERS """

plot_params={}
function_params={}
plot_types=["plot","polar","semilogx","semilogy","loglog","scatter","boxplot","vline","hline","vspan","hspan","annotate","imshow","bar","text","table"]
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
args_params["bar"]["left"]="""The left position of the bar."""
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
                      "title",
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
                      "theta_min",
                      "theta_max",
                      "rmin",
                      "rmax",
                      "grid",
                      "axis_off",
                      "color_bar",
                      "tight_layout"]
        for key in keys_in_data:
            if key in plot_data[plot]:
                prepared_plots[plot][key]=plot_data[plot][key]
        
        prepared_plots[plot]["plot_functions"]=[]
        for cloud in plot_data[plot]["values"]:
            ptype= plot_data[plot]["values"][cloud]["type"]
            plot_func={"func_name":ptype, "legend":""}
            
            prepared_params=["type"]
            
            if ptype in ["plot","semilogx","semilogy","loglog"]:
                if "x_values" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["x_values"],plot_data[plot]["values"][cloud]["y_values"]]
                else:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["y_values"]]       
                
                prepared_params+=["x_values","y_values"]
                
            
            if ptype=="polar":
                plot_func["args"]=[plot_data[plot]["values"][cloud]["theta_values"],plot_data[plot]["values"][cloud]["r_values"]]
                prepared_params+=["theta_values","r_values"]
            
            if ptype=="scatter":
                plot_func["args"]=[plot_data[plot]["values"][cloud]["x_values"],plot_data[plot]["values"][cloud]["y_values"]]
                #(x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, verts, edgecolors, hold, data)
                prepared_params+=["x_values","y_values"]
            
            if ptype=="boxplot":
                plot_func["args"]={"y_sets":plot_data[plot]["values"][cloud]["y_sets"],
                                   "x_values":plot_data[plot]["values"][cloud]["x_values"],
                                   "x_size":plot_data[plot]["values"][cloud]["x_size"]}
                bpvalues=["y_sets","x_values","x_size"]
                prepared_params+=bpvalues
            
            if ptype=="vline":    
                if "y_axis_prop_range" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["x_pos"],
                                       plot_data[plot]["values"][cloud]["y_axis_prop_range"][0],
                                       plot_data[plot]["values"][cloud]["y_axis_prop_range"][1]]
                else:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["x_pos"]]
                    
                prepared_params+=["y_axis_prop_range","x_pos"]
            
            if ptype=="hline":    
                if "x_axis_prop_range" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["y_pos"],
                                       plot_data[plot]["values"][cloud]["x_axis_prop_range"][0],
                                       plot_data[plot]["values"][cloud]["x_axis_prop_range"][1]]
                else:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["y_pos"]]
                    
                prepared_params+=["x_axis_prop_range","y_pos"]
                
            if ptype=="vspan":    
                if "y_axis_prop_range" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["x_min"],
                                       plot_data[plot]["values"][cloud]["x_max"],
                                       plot_data[plot]["values"][cloud]["y_axis_prop_range"][0],
                                       plot_data[plot]["values"][cloud]["y_axis_prop_range"][1]]
                else:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["x_min"],plot_data[plot]["values"][cloud]["x_max"]]
                    
                prepared_params+=["x_axis_prop_range","x_min", "x_max"]
            
            if ptype=="hspan":    
                if "x_axis_prop_range" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["y_min"],plot_data[plot]["values"][cloud]["y_max"],
                                       plot_data[plot]["values"][cloud]["x_axis_prop_range"][0],
                                       plot_data[plot]["values"][cloud]["x_axis_prop_range"][1]]
                else:
                    plot_func["args"]=[plot_data[plot]["values"][cloud]["y_min"],plot_data[plot]["values"][cloud]["y_max"]]
                    
                prepared_params+=["x_axis_prop_range","y_min","y_max"]
            
            if ptype=="annotate": 
                plot_func["args"]=[plot_data[plot]["values"][cloud]["text"], plot_data[plot]["values"][cloud]["pos"]]
                prepared_params+=["text","pos"]                
            
            if ptype=="imshow":   
                plot_func["args"]=plot_data[plot]["values"][cloud]["matrix_colors"]
                prepared_params+=["matrix_colors"]                
            
            if ptype=="bar":   
                plot_func["args"]=[plot_data[plot]["values"][cloud]["left"],
                                   plot_data[plot]["values"][cloud]["height"],
                                   plot_data[plot]["values"][cloud]["width"],
                                   plot_data[plot]["values"][cloud]["bottom"] if "bottom" in plot_data[plot]["values"][cloud] else 0]
#                 plot_func["args"]={"left":plot_data[plot]["values"][cloud]["left"],
#                                    "height":plot_data[plot]["values"][cloud]["height"],
#                                    "width":plot_data[plot]["values"][cloud]["width"],
#                                    "bottom":plot_data[plot]["values"][cloud]["bottom"] if "bottom" in plot_data[plot]["values"][cloud] else 0}
                prepared_params+=["left","height","width","bottom"]
                
            if ptype=="text":
                plot_func["args"]=[plot_data[plot]["values"][cloud]["x"],
                                   plot_data[plot]["values"][cloud]["y"],
                                   plot_data[plot]["values"][cloud]["text"]]
                
                prepared_params+=["x","y","text"]
                
                
            if ptype=="table":
                                
                plot_func["cellText"]=plot_data[plot]["values"][cloud]["matrix"]
                plot_func["rowLabels"]=plot_data[plot]["values"][cloud]["rows"]
                plot_func["colLabels"]=plot_data[plot]["values"][cloud]["cols"]
                plot_func["args"]={"nb_rows":len(plot_func["rowLabels"]),
                                   "nb_cols":len(plot_func["colLabels"])}                   
                
                if "line_width_prop" in plot_data[plot]["values"][cloud]:
                    nb_cols=plot_func["args"]["nb_cols"]                    
                    plot_func["colWidths"]=[1.*plot_data[plot]["values"][cloud]["line_width_prop"]/(nb_cols)]*nb_cols
#                 if "colWidths" in plot_data[plot]["values"][cloud]:
#                     plot_func["colWidths"]=plot_data[plot]["values"][cloud]["colWidths"]
                
                if "col_height_prop" in plot_data[plot]["values"][cloud]:
                    nb_rows=plot_func["args"]["nb_rows"]                    
                    plot_func["args"]["rowHeights"]=[1.*plot_data[plot]["values"][cloud]["col_height_prop"]/(nb_rows)]*nb_rows
                if "rowHeights" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]["rowHeights"]=plot_data[plot]["values"][cloud]["rowHeights"]
                
                if "fontsize" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]["fontsize"]=plot_data[plot]["values"][cloud]["fontsize"]
                    
                if "label_params" in plot_data[plot]["values"][cloud]:
                    plot_func["args"]["label_params"]=plot_data[plot]["values"][cloud]["label_params"]
                
                prepared_params+=["rows","cols","matrix","line_width_prop","col_height_prop","fontsize", "label_params", "rowHeights"]
                
                                                
                        
            for key in plot_data[plot]["values"][cloud]:
                if key not in prepared_params:
                    plot_func[key]=plot_data[plot]["values"][cloud][key]
                        
            prepared_plots[plot]["plot_functions"].append(plot_func)
            del plot_func
                                
        
        prepared+=1
        if (prepared%50==0):
        	print("prepared {0}/{1}".format(prepared,len_data))        
                        
            
    return prepared_plots

def plot_indivs(prepared_plots,show=False,file_to_save=None,format_to_save=None,dir_to_save=None,PDF_to_add=None, from_page=False):
    #figs
    
    for plot in prepared_plots:
        #this fig
        if not from_page:
            fig=plt.figure(num=plot, figsize=conf.figsize, dpi=conf.dpi)#, facecolor, edgecolor, frameon, FigureClass)
            if 'axes_projection' in prepared_plots[plot]:
                if prepared_plots[plot]['axes_projection']=='polar':
                    polax = fig.add_subplot(111, polar=True)
        #titles
        if "x_axis_label" in prepared_plots[plot]:
            plt.xlabel(prepared_plots[plot]["x_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)
        if "y_axis_label" in prepared_plots[plot]:
            plt.ylabel(prepared_plots[plot]["y_axis_label"],fontsize=conf.axes_labels_font_size,labelpad=conf.title_and_axes_labelpad,**conf.used_font)
        if "title" in prepared_plots[plot]:
            fontdict={'fontsize': conf.title_font_size,'verticalalignment': 'baseline','horizontalalignment': "center"}
            if 'axes.titlepad' in rcParams.keys():
                rcParams['axes.titlepad'] = conf.title_and_axes_labelpad 
                plt.title(prepared_plots[plot]["title"],fontdict=fontdict)
            else:
                #plt.title(prepared_plots[plot]["title"],fontdict=fontdict, y=1.+conf.title_and_axes_labelpad/(72.*fig.get_size_inches()[1]))
                plt.title(prepared_plots[plot]["title"],fontdict=fontdict, y=1.+conf.title_and_axes_labelpad/(72.*conf.figsize[1]))
                
        if "colors" in prepared_plots[plot]:
            colors=prepared_plots[plot]["colors"]
        else:
            colors=conf.colors
        
                
        func_id=0
        has_box_plots=False
        for plot_func in prepared_plots[plot]["plot_functions"]:
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
                plt.bar(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="plot":
                plt.plot(*plot_func["args"], **kawargs)
                #plt.semilogx(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="polar":
                plt.polar(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="semilogx":
                plt.semilogx(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="semilogy":
                plt.semilogy(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="loglog":
                plt.loglog(*plot_func["args"], **kawargs)
                
            if plot_func["func_name"]=="annotate":
                plt.annotate(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="table":
                the_table=plt.table(**kawargs)
                
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
                plt.text(*plot_func["args"], **kawargs)
                
            if plot_func["func_name"]=="vline":
                plt.axvline(*plot_func["args"],**kawargs)
                    
            if plot_func["func_name"]=="hline":
                plt.axhline(*plot_func["args"],**kawargs)
                    
            if plot_func["func_name"]=="vspan":
                plt.axvspan(*plot_func["args"],**kawargs)
                    
            if plot_func["func_name"]=="hspan":
                plt.axhspan(*plot_func["args"],**kawargs)
                    
            if plot_func["func_name"]=="scatter":
                plt.scatter(*plot_func["args"], **kawargs)
            
            if plot_func["func_name"]=="imshow":
                plt.imshow(plot_func["args"], **kawargs)

                
            my_box_plot={}
            if plot_func["func_name"]=="boxplot":
                has_box_plots=True
                my_box_plot[func_id]=plt.boxplot(plot_func["args"]["y_sets"], 
                    positions = plot_func["args"]["x_values"],
                    sym='bx',
                    #whis = 1,#default 1.5
                    widths=[plot_func["args"]["x_size"]]*len(plot_func["args"]["x_values"]), #(4.2, 4.2),
                    showfliers=False,
                    patch_artist = True)
                
                
                not_legended=True
                for element in my_box_plot[func_id]['medians']:
                    if "legends" in prepared_plots[plot] and not_legended:
                        element.set_label(plot_func["legend"])# label
                        not_legended=False
                    if "color" in kawargs:
                        element.set_color(kawargs["color"])#conf.colors[plot_func["color_index"]]
#                    element.set_linestyle('solid')#('dashed')
                    element.set_linestyle(kawargs["linestyle"])#('dashed')
                    element.set_linewidth(kawargs["linewidth"])
                for element in my_box_plot[func_id]['boxes']:
                    if "color" in kawargs:
                        element.set_edgecolor(kawargs["color"])
                    element.set_facecolor(kawargs["fill_color"])
                    element.set_linewidth(kawargs["linewidth"])
#                    element.set_linestyle('solid')#('dashed')
                    element.set_linestyle(kawargs["linestyle"])#('dashed')
                    element.set_fill(kawargs["fill"])
                    #element.set_hatch('/')
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
                    
                
            func_id+=1
        
        #ticks
        extra_xtick_label_size=0
        if "extra_xtick_label_size" in prepared_plots[plot]:
            extra_xtick_label_size=prepared_plots[plot]["extra_xtick_label_size"]
        extra_ytick_label_size=0
        if "extra_ytick_label_size" in prepared_plots[plot]:
            extra_xtick_label_size=prepared_plots[plot]["extra_ytick_label_size"]   
                 
        #https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html#matplotlib.axes.Axes.tick_params
        #default tick params
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='on',
            labelsize=conf.ticks_labels_font_size+extra_xtick_label_size) # labels along the bottom edge are off
            
        plt.tick_params(
            axis='y',          # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            labelsize=conf.ticks_labels_font_size+extra_ytick_label_size) # labels along the bottom edge are off
        
        #tick and labels
        if "x_ticks" in prepared_plots[plot]:
            ticks=prepared_plots[plot]["x_ticks"]
            for key in ticks:
                if "params" in ticks[key]:
                    plt.tick_params(axis='x',which=key,**ticks[key]["params"])
                if "range_step" in ticks[key]:
                    plt.gca().xaxis.set_ticks(np.arange(ticks[key]["from"],ticks[key]["to"],ticks[key]["range_step"]),minor=(key=="minor"))
                elif "positions" in ticks[key]:
                    plt.gca().xaxis.set_ticks(ticks[key]["positions"],minor=(key=="minor"))
                
                if "labels" in ticks[key]:
                    plt.gca().xaxis.set_ticklabels(ticks[key]["labels"],minor=(key=="minor"))
                else:
                    if has_box_plots:
                        plt.gca().xaxis.set_ticklabels([]) 
        
        if "y_ticks" in prepared_plots[plot]:
            ticks=prepared_plots[plot]["y_ticks"]
            for key in ticks:
                if "params" in ticks[key]:
                    plt.tick_params(axis='y',which=key,**ticks[key]["params"])
                if "range_step" in ticks[key]:
                    plt.gca().yaxis.set_ticks(np.arange(ticks[key]["from"],ticks[key]["to"],ticks[key]["range_step"]),minor=(key=="minor"))
                elif "positions" in ticks[key]:
                    plt.gca().yaxis.set_ticks(ticks[key]["positions"],minor=(key=="minor"))
                
                if "labels" in ticks[key]:
                    plt.gca().yaxis.set_ticklabels(ticks[key]["labels"],minor=(key=="minor"))
                    

                
        
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
            if "legend_loc"  in prepared_plots[plot]["legends"]:
                leg_loc=prepared_plots[plot]["legends"]["legend_loc"]
            if "italic_legends" in prepared_plots[plot]["legends"] and prepared_plots[plot]["legends"]["italic_legends"]:
                rcParams['font.style'] = 'italic'
                if "manual_legends" in prepared_plots[plot]["legends"]:  
                    leg=plt.legend(handles=prepared_plots[plot]["legends"]["manual_legends"],fontsize=conf.legend_labels_font_size,markerscale=conf.legend_markerscale, loc=leg_loc)        
                else:
                    myhandles, mylabels = plt.gca().get_legend_handles_labels()
                    #print(myhandles,mylabels)
                    if len(myhandles)!=0:
                        leg=plt.legend(fontsize=conf.legend_labels_font_size,markerscale=conf.legend_markerscale, loc=leg_loc)            
                rcParams['font.style'] = 'normal'
                if leg:
                    for legend_element in leg.legendHandles:
                        legend_element.set_linewidth(conf.legend_linewidth)   
            else:
                if "manual_legends" in prepared_plots[plot]["legends"]:  
                    leg=plt.legend(handles=prepared_plots[plot]["legends"]["manual_legends"],fontsize=conf.legend_labels_font_size,markerscale=conf.legend_markerscale, loc=leg_loc)
                else:
                    myhandles, mylabels = plt.gca().get_legend_handles_labels()
                    #print(myhandles,mylabels)
                    if len(myhandles)!=0:
                        #myhandles[0].set_linewidth(28)
                        leg=plt.legend(fontsize=conf.legend_labels_font_size,markerscale=conf.legend_markerscale, loc=leg_loc)   
            
            if leg:   
                leg.get_frame().set_linewidth(conf.legend_border_width)
                leg.get_frame().set_edgecolor(conf.legend_border_color)
            #prepared_plots[plot]["plot_legends"]
            
        
        if "grid" in prepared_plots[plot]:
            plt.grid(**prepared_plots[plot]["grid"])
        
        if "axis_off" in prepared_plots[plot] and prepared_plots[plot]["axis_off"]:
            plt.gca().set_axis_off()
            #plt.gca().xaxis.set_visible(False)
        
        #MUST BE LAST BECAUSE NEW AXES ARE CREATED
        if "color_bar" in prepared_plots[plot]:
            #print(prepared_plots[plot]["color_bar"])
            location="right"
            if "location" in prepared_plots[plot]["color_bar"]:
                location=prepared_plots[plot]["color_bar"]["location"]
                
            
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
            ax2 = divider.append_axes(location, "5%", pad="3%")
            #plt.colorbar(im, cax=cax)
        
            # Set the colormap and norm to correspond to the data for which
            # the colorbar will be used.
            cmap = mpl_colors.ListedColormap(color_list)#['r', 'orange', 'b', 'g'])
            norm = mpl_colors.BoundaryNorm(color_bounds, cmap.N)
            cb2 = mpl_colorbar.ColorbarBase(ax2, cmap=cmap,
                                            norm=norm,
                                            # to use 'extend', you must
                                            # specify two extra boundaries:
                                            boundaries=color_bounds,
                                            #extend='both',
                                            ticks=color_bounds,  # optional
                                            spacing='proportional',
                                            #orientation='vertical',
                                            #**kw
                                            )
            cb2.ax.tick_params(labelsize=conf.ticks_labels_font_size)
            #Label
            if "label" in prepared_plots[plot]["color_bar"]:
                cb2.set_label(prepared_plots[plot]["color_bar"]["label"])
                        

        
        
        if not from_page and "tight_layout" in prepared_plots[plot] and prepared_plots[plot]["tight_layout"]:
            plt.tight_layout()

        
        if file_to_save and format_to_save:
            path_to_save=file_to_save
            if dir_to_save:
                path_to_save=dir_to_save+"/"+path_to_save
                if not os.path.exists(dir_to_save):
                    os.makedirs(dir_to_save)
            plt.savefig(path_to_save,format=format_to_save)
        elif (not from_page) and "file_to_save" in prepared_plots[plot] and "format_to_save" in prepared_plots[plot]:
            path_to_save=prepared_plots[plot]["file_to_save"]
            if "dir_to_save" in prepared_plots[plot]:
                path_to_save=prepared_plots[plot]["dir_to_save"]+"/"+path_to_save
                if not os.path.exists(prepared_plots[plot]["dir_to_save"]):
                    os.makedirs(prepared_plots[plot]["dir_to_save"])
            plt.savefig(path_to_save,format=prepared_plots[plot]["format_to_save"])
        if PDF_to_add:
            plt.savefig(PDF_to_add,format="pdf")
        if show:
            plt.show()
        else:
            if not from_page:
                plt.close()
            
            
                
            
def plot_pages(prepared_plots, nb_plots_hor=3, nb_plots_vert=2, show=False,file_to_save=None,format_to_save=None,dir_to_save=None,PDF_to_add=None):
    
    conf.update(max(nb_plots_vert,nb_plots_hor))
    
    
    axes={}
    nb_pages=int(len(prepared_plots)/(nb_plots_vert*nb_plots_hor))
    if len(prepared_plots)%(nb_plots_vert*nb_plots_hor)!=0:
        nb_pages+=1
    
    sppk=sorted(prepared_plots.keys())
    
    for page_id in range(nb_pages):
        print("setting page {0}/{1}...".format(page_id+1,nb_pages))
        plt.figure(num=page_id, figsize=conf.figsize, dpi=conf.dpi)
        
        for plot_index in range(len(sppk)):
            plot=sppk[plot_index]
            # print(prepared_plots[plot])
            page=int(plot_index/(nb_plots_vert*nb_plots_hor))
            plot_id=plot_index%(nb_plots_vert*nb_plots_hor)
            if page>page_id:
                break
            if page==page_id:
                polar=False
                if 'axes_projection' in prepared_plots[plot]:
                    if prepared_plots[plot]['axes_projection']=='polar':
                        polar=True
                        
                axes[plot]=plt.subplot(nb_plots_vert,nb_plots_hor,plot_id+1,polar=polar)
                
                if plot in prepared_plots:
                    plot_indivs({0:dict(prepared_plots[plot])},show=False,file_to_save=None,dir_to_save=None,PDF_to_add=None, from_page=True)
                else:
                    plt.plot(np.log(range(1,10)))
        plt.tight_layout()
        
        if file_to_save and format_to_save:
            path_to_save=file_to_save+'{0}.{1}'.format(page_id,format_to_save)
            if dir_to_save:
                path_to_save=dir_to_save+"/"+path_to_save
                if not os.path.exists(dir_to_save):
                    os.makedirs(dir_to_save)
            plt.savefig(path_to_save,format=format_to_save)
        if PDF_to_add:
            plt.savefig(PDF_to_add,format="pdf")
        if show:
            plt.show()
        else:
            plt.close()
                
        
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
        0:{"values":{0:{"type":"plot","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                            1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                            2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, 
                            },
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
              20:{"values":{0:{"type":"plot","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                            1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                            2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, 
                            },
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
              21:{"values":{0:{"type":"semilogx","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                            1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                            2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, 
                            },
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
                  "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
              22:{"values":{0:{"type":"semilogy","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                            1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                            2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, 
                            },
                  "colors":["red","green","blue"],
                  "plot_types":"example",
                  "file_to_save":"example1.png",
                  "format_to_save":"png", ##png, pdf, ps, eps or svg.
                  "dir_to_save":"test_plots_gen",
                  "y_axis_label":"y label",
                  "x_axis_label":"th x lbel",
                  "title":"semilogy and plot",
                  "legends":{"manual_legends":legend_example},
                  "grid":{"which":'major',"axis":"both"},
                  "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
              23:{"values":{0:{"type":"loglog","y_values":np.log(range(1,10)), 'color_index':0, 'legend':'plot 0'},
                            1:{"type":"plot","y_values":np.log(range(1,10)),"x_values":range(10,1,-1),"linestyle":'--'},
                            2:{"type":"vline","x_pos":4.4, 'y_axis_prop_range':[0.1,0.6], "dashes":[5,1]}, 
                            },
                  "colors":["red","green","blue"],
                  "plot_types":"example",
                  "file_to_save":"example1.png",
                  "format_to_save":"png", ##png, pdf, ps, eps or svg.
                  "dir_to_save":"test_plots_gen",
                  "y_axis_label":"y label",
                  "x_axis_label":"th x lbel",
                  "title":"loglog and plot",
                  "legends":{"manual_legends":legend_example},
                  "grid":{"which":'major',"axis":"both"},
                  "color_bar":{"default_bounds":True,"color_list":["red","green","blue"]}},
               4:{"values":{
                            3:{"type":"imshow","matrix_colors":[([0.3, 0.4, 1], [0.0, 0.0, 0.0]),([0.3, 1, 1], [0.3, 0.3, 1])]},
                            4:{"type":"hline","y_pos":4.4, 'x_axis_prop_range':[0.1,0.6], 'color_index':0,"color":"red", "linewidth":4., "solid_capstyle":'round'},
                            5:{"type":"hspan","y_min":1.7, "y_max":3.7, 'x_axis_prop_range':[0.1,0.6]},
                            6:{"type":"bar","left":6.7, 'height':2., 'width':1.5, "bottom":1., "color":"red", "linewidth":4.,"edgecolor":'none'},
                            },
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
               5:{"values":{7:{"type":"text","x":3, 'y':4., "text":"Bonzai", "va":'center', "ha":'center',"bbox":dict(boxstyle="round4", fc="None", ec="blue")},
                            8:{"type":"text","x":2, 'y':4.5, "text":"Bonzai",},
                            9:{"type":"annotate","text":"Bonzai annotated","pos":(4.,4.)},
                            },
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
               1:{"values":{0:{"type":"scatter",'x_values':[5,6,7],'y_values':[1,5,2], 'color_index':0, 's':60, 'legend':'black 128'},
                            1:{"type":"scatter",'x_values':[4,5,3],'y_values':[1.5,5.5,1.6], 'color_index':1, 's':90, "marker":r'$\beta$', 'legend':'red scatter, no?'}}, 
                  "plot_types":"scatter",
                  "file_to_save":"scatter_example.png",
                  "format_to_save":"png", ##png, pdf, ps, eps or svg.
                  "dir_to_save":"test_plots_gen",
                  "y_axis_label":"scat y label",
                  "x_axis_label":"scat x lbel",
                  "title":"double scatter example 1",
                  "legends":{"italic_legends":True}},
               2:{"values":{0:{"type":"boxplot",'x_values':[5,6,7],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.7, "color":"green", "linewidth":3., 'fill':True, 'legend':'AHAHAH?'},
                            1:{"type":"boxplot",'x_values':[1,2,3],'y_sets':[[1,5,2],[1,7,2],[1,5,4]], 'x_size':0.37, "color":"purple", 'legend':'red, no?'}}, 
                  "plot_types":"boxplot",
                  "file_to_save":"boxplot_example.png",
                  "format_to_save":"png", ##png, pdf, ps, eps or svg.
                  "dir_to_save":"test_plots_gen",
                  "y_axis_label":"bop y label",
                  "x_axis_label":"ejhsrguezv x lbel",
                  "title":"double boxplot example",
                  "legends":{"italic_legends":True},
                  "x_ticks":{"major":{"range_step":1, "from":1, "to":8,
                                      "labels":["b",'a',2],
                                      "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}},
                             "minor":{"range_step":1, "from":1.5, "to":8.5,
                                      "labels":["c",'d',1],
                                      "params":{"direction":'out',"bottom":'off',"top":'off',"labelbottom":'on'}}},
                  "y_ticks":{"major":{"positions":[3],
                                      "labels":["baa"],
                                      "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}},
                             "minor":{"positions":[3.5],
                                      "labels":["ckzUGF"],
                                      "params":{"direction":'out',"left":'on',"right":'off',"labelleft":'on'}}},
                  "xmax":20,
                  "tight_layout":True},
               3:{"values":{0:{"type":"scatter",'x_values':[5,6,7],'y_values':[1,5,2], 'color_index':0, 'legend':'black 128'},
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
               10:{"values":{0:{"type":"annotate","text":"","pos":(3.,3.),'xytext':(6.3,6.3), 'horizontalalignment':'center', 'label':"Nice arrow",
                                "arrowprops":dict(arrowstyle="-|>,head_width=.6, head_length=1.2",connectionstyle="arc3,rad=0.4",
                                            lw=3.5,#*nodeid, 
                                            fc="purple", 
                                            ec="green",
                                            shrinkA=0,
                                            shrinkB=8,
                                            
                                            ls="solid",
                                            zorder=10
                                            )}}, 
                  "plot_types":"as:kjghzlrbg",
                  "file_to_save":"arrow.png",
                  "format_to_save":"png", ##png, pdf, ps, eps or svg.
                  "dir_to_save":"test_plots_gen",
                  "y_axis_label":"arrow y label",
                  "x_axis_label":"arrow x lbel",
                  "title":"Jack Sp(ecial) arrow example",
                  "xmax":10,
                  "ymax":10,
                  "legends":{"italic_legends":True}},}
    some_data[25]={
          "values":{
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


    
    prepared_plots=prepare_plots(some_data)
    plot_indivs(prepared_plots,show=False,file_to_save=None,dir_to_save=None,PDF_to_add=None)
    pp1 = PdfPages('plottings.pdf')
    plot_pages(prepared_plots, nb_plots_hor=2, nb_plots_vert=2, show=False, file_to_save="plottings", format_to_save='eps', dir_to_save="test_plots_gen", PDF_to_add=pp1)
    pp1.close()
    
