#!/usr/bin/python2.7
# -*- coding: utf8 -*-
'''
Created on 15 sept. 2017

@author: Guillaume Gaillard
'''

##########SPECIFIC PUBLICATIONS PARAMETERS
fig_profile="A4"
#fig_profile="Springer_journal"
#fig_profile="Springer_book"
#fig_profile="PDF_guigui"
#fig_profile="plot_show"

fig_orientation="landscape"
#fig_orientation="portrait"

fig_nb_column_width=1#2,3,4

def set_fig(profile,orientation,nb_column_width=2):
    global fig_profile,fig_orientation,fig_nb_column_width
    fig_profile=profile
    fig_orientation=orientation
    fig_nb_column_width=nb_column_width
    print(fig_profile)
    
#CONSTANTS
a4=(11.68,8.26)
show_prop=3
inch= 0.0393701 #one mm in inches

#FINAL SPRINGER PAPER CONSTANTS
#image sizes in mm
one_column_width=39
two_columns_width=84
three_columns_width=129
four_columns_width=174
journal_height=234

book_one_column_width=80
book_two_columns_width=122
book_height=198


#DEFAULT
figsize=(a4[0],a4[1])
dpi=300 #only for non-vector formats

hfont = {'fontname':'Helvetica'}
dfont = {'fontname':'DejaVu Sans'}
afont = {'fontname':'Arial'}
used_font=dfont

colors=['black','red']
#manage  colorbar colors
colorbar_colors=['g', 'b','cyan','magenta','yellow','orange', 'r','white']
colorbar_color_bounds=[0, 0.05, 0.1, 0.20, 0.4, 0.5, 0.8, 0.95, 1.0]

general_plots_linewidth=1.
scatter_size=50
        
axes_labels_font_size=10
legend_labels_font_size=10
ticks_labels_font_size=8
title_font_size=12
title_and_axes_labelpad=5

legend_markerscale=1.5
legend_border_width=1
legend_border_color='black'
legend_linewidth=2.0
    
    
plot_params={"plot":{"linewidth":general_plots_linewidth},
             "polar":{"linewidth":general_plots_linewidth},
             "semilogx":{"linewidth":general_plots_linewidth},
             "semilogy":{"linewidth":general_plots_linewidth},
             "loglog":{"linewidth":general_plots_linewidth},
             "vline":{"linewidth":general_plots_linewidth,"dashes":[]},
             "hline":{"linewidth":general_plots_linewidth,"dashes":[]},
             "scatter":{"s":scatter_size},
             "boxplot":{"linestyle":"solid","linewidth":0.75*general_plots_linewidth,"fill":False,"fill_color":'cyan'},
             "violinplot":{"linestyle":"solid","linewidth":0.75*general_plots_linewidth,"fill":False,"fill_color":'cyan'},
             "bar":{},
             "hspan":{"alpha":0.5},
             "vspan":{"alpha":0.5},
             "imshow":{"interpolation":'nearest',"aspect":'auto', "origin":'lower'},
             "pcolormesh":{},
             "simple_pcolormesh":{},
             "text":{"fontdict":{'fontname':used_font['fontname'],"fontsize":ticks_labels_font_size}},
             "annotate":{"size":ticks_labels_font_size},
             "table":{'loc':'center',"cellLoc":'center', "rowLoc":'center',"colLoc":'center','fontsize':ticks_labels_font_size},
             "fill_between":{"linewidth":general_plots_linewidth}
            }



def set_figsize(user_defined_fixed_size):   #Change figure setting
    global figsize
    figsize=user_defined_fixed_size

def set_title_and_axes_labelpad(user_defined_title_and_axes_labelpad):   #Change labelpad setting
    global title_and_axes_labelpad
    title_and_axes_labelpad=user_defined_title_and_axes_labelpad    

def update(subp=1):   #FIGURE
    global figsize,dpi,axes_labels_font_size,legend_labels_font_size,ticks_labels_font_size,title_font_size,title_and_axes_labelpad
    global legend_markerscale,legend_border_width,legend_border_color,legend_linewidth,hfont,afont,used_font,colors,colorbar_colors
    global colorbar_color_bounds,plot_params    
    
    if fig_profile=="A4":
        if fig_orientation=="landscape":
            figsize=(a4[0],a4[1])    
        if fig_orientation=="portrait":
            figsize=(a4[1],a4[0])

    if fig_profile=="plot_show":
        if fig_orientation=="landscape":
            figsize=(a4[0]/show_prop,a4[1]/show_prop)      
        if fig_orientation=="portrait":
            figsize=(a4[1]/show_prop,a4[0]/show_prop)
    
    if fig_profile=="Springer_journal":
        if fig_orientation=="landscape":
            if fig_nb_column_width==1:
                figsize=(1.*one_column_width*inch,0.125*journal_height*inch)
            if fig_nb_column_width==2:
                figsize=(1.*two_columns_width*inch,0.25*journal_height*inch)
            if fig_nb_column_width==3:
                figsize=(1.*three_columns_width*inch,0.375*journal_height*inch)
            if fig_nb_column_width==4:
                figsize=(1.*four_columns_width*inch,0.5*journal_height*inch)
        if fig_orientation=="portait":
            if fig_nb_column_width==1:
                figsize=(1.*one_column_width*inch,0.25*journal_height*inch)
            if fig_nb_column_width==2:
                figsize=(1.*two_columns_width*inch,0.5*journal_height*inch)
            if fig_nb_column_width==3:
                figsize=(1.*three_columns_width*inch,0.75*journal_height*inch)
            if fig_nb_column_width==4:
                figsize=(1.*four_columns_width*inch,1.*journal_height*inch)
                
    if fig_profile=="Springer_book":
        if fig_orientation=="landscape":
            if fig_nb_column_width==1:
                figsize=(1.*book_one_column_width*inch,0.125*book_height*inch)
            if fig_nb_column_width==2:
                figsize=(1.*book_two_columns_width*inch,0.25*book_height*inch)
        if fig_orientation=="portait":
            if fig_nb_column_width==1:
                figsize=(1.*book_one_column_width*inch,0.25*book_height*inch)
            if fig_nb_column_width==2:
                figsize=(1.*book_two_columns_width*inch,0.5*book_height*inch)
                        
    if fig_profile=="ACM-sigconf":
        if fig_orientation=="portait":
            if fig_nb_column_width==1:
                figsize=(541.295/72,0.16*book_height*inch)
            if fig_nb_column_width==2:
                figsize=(241.14749/72,0.75*241.14749/72)


    hfont = {'fontname':'Helvetica'}
    dfont = {'fontname':'DejaVu Sans'}
    afont = {'fontname':'Arial'}
    used_font=dfont
    
    colors=['black','red']
    #manage  colorbar colors
    colorbar_colors=['g', 'b','cyan','magenta','yellow','orange', 'r','white']
    colorbar_color_bounds=[0, 0.05, 0.1, 0.20, 0.4, 0.5, 0.8, 0.95, 1.0]#[0, 0.02, 0.05, 0.1, 0.20, 0.4, 0.8, 0.95, 1.0]
    
    general_plots_linewidth=subp**(-1)*1.
    scatter_size=subp**(-1)*50
    ticks_labels_font_size=subp**(-1)*12
    
    if fig_profile=="A4":
        dpi=300 #only for non-vector formats
        
        axes_labels_font_size=subp**(-1)*25
        legend_labels_font_size=subp**(-1)*25
        ticks_labels_font_size=subp**(-1)*22
        title_font_size=subp**(-1)*30
        title_and_axes_labelpad=subp**(-1)*15
        
        legend_markerscale=1.+subp**(-1)*.5
        legend_border_width=subp**(-1)*1
        legend_border_color='black'
        legend_linewidth=subp**(-1)*2.0
        
        scatter_size=subp**(-1)*50
        general_plots_linewidth=subp**(-1)*1.

    if fig_profile=="plot_show":
        dpi=300 #only for non-vector formats
        
        axes_labels_font_size=subp**(-1)*25/show_prop
        legend_labels_font_size=subp**(-1)*25/show_prop
        ticks_labels_font_size=subp**(-1)*22/show_prop
        title_font_size=subp**(-1)*30/show_prop
        title_and_axes_labelpad=subp**(-1)*15
        
        legend_markerscale=1.+subp**(-1)*.5
        legend_border_width=subp**(-1)*1
        legend_border_color='black'
        legend_linewidth=subp**(-1)*2.0
        
        scatter_size=subp**(-1)*50
        general_plots_linewidth=subp**(-1)*1.

    
    if fig_profile=="Springer_journal":
        dpi=600 #only for non-vector formats
        
        axes_labels_font_size=10
        legend_labels_font_size=10
        ticks_labels_font_size=8
        title_font_size=12
        title_and_axes_labelpad=5
        
        legend_markerscale=1.5
        legend_border_width=1
        legend_border_color='black'
        legend_linewidth=2.0
        
        scatter_size=25
        general_plots_linewidth=subp**(-1)*1.
        
    if fig_profile=="Springer_book":
        dpi=600 #only for non-vector formats
        
        axes_labels_font_size=10
        legend_labels_font_size=10
        ticks_labels_font_size=8
        title_font_size=12
        title_and_axes_labelpad=5
        
        legend_markerscale=1.5
        legend_border_width=1
        legend_border_color='black'
        legend_linewidth=2.0
        
        scatter_size=25
        general_plots_linewidth=subp**(-1)*1.

    if fig_profile=="ACM-sigconf":
        dpi=600 #only for non-vector formats
        
        axes_labels_font_size=5
        legend_labels_font_size=7
        ticks_labels_font_size=4
        title_font_size=12
        title_and_axes_labelpad=2
        
        legend_markerscale=1.
        legend_border_width=0.008
        legend_border_color='black'
        legend_linewidth=.4
        
        scatter_size=5
        general_plots_linewidth=.5#subp**(-1)*0.1    
    
    
    plot_params={"plot":{"linewidth":general_plots_linewidth},
                 "polar":{"linewidth":general_plots_linewidth},
                 "semilogx":{"linewidth":general_plots_linewidth},
                 "semilogy":{"linewidth":general_plots_linewidth},
                 "loglog":{"linewidth":general_plots_linewidth},
                 "vline":{"linewidth":general_plots_linewidth,"dashes":[]},
                 "hline":{"linewidth":general_plots_linewidth,"dashes":[]},
                 "scatter":{"s":scatter_size},
                 "boxplot":{"linestyle":"solid","linewidth":0.75*general_plots_linewidth,"fill":False,"fill_color":'cyan'},
                 "violinplot":{"linestyle":"solid","linewidth":0.75*general_plots_linewidth,"fill":False,"fill_color":'cyan'},
                 "bar":{},
                 "hspan":{"alpha":0.5},
                 "vspan":{"alpha":0.5},
                 "imshow":{"interpolation":'nearest',"aspect":'auto', "origin":'lower'},
                 "pcolormesh":{},
                 "simple_pcolormesh":{},
                 "text":{"fontdict":{'fontname':used_font['fontname'],"fontsize":ticks_labels_font_size}},
                 "annotate":{"size":ticks_labels_font_size},
                 "table":{'loc':'center',"cellLoc":'center', "rowLoc":'center',"colLoc":'center','fontsize':ticks_labels_font_size},
                 "fill_between":{"linewidth":general_plots_linewidth}
                 }


def update_ticks_labels_font_size(new_size):   #FIGURE
    global ticks_labels_font_size,plot_params    
    
    ticks_labels_font_size=new_size
    
    plot_params["text"]["fontdict"]["fontsize"]=ticks_labels_font_size
    plot_params["annotate"]["size"]=ticks_labels_font_size
    plot_params["table"]["fontsize"]=ticks_labels_font_size


def update_axes_labels_font_size(new_size):   #FIGURE
    global axes_labels_font_size

    axes_labels_font_size=new_size
    