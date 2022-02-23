"""
#
# This is for sample CPR map to compare Org. Metrics
# Fig. 5 of White et al. (2018)
#
# By Daeho Jin 
# 2022.02.14
"""

import numpy as np
import sys
import os.path
import math
import calc_org_metrics_module as com

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator,AutoMinorLocator,FixedLocator

def main():
    ### Initialize
    nx,ny= 20,20
    lonb= np.arange(nx+1)
    latb= np.arange(ny+1)
    X,Y= np.meshgrid(lonb,latb)
    arr0= np.zeros([ny,nx])

    centers= [(5,5), (5,14), (14,5), (14,14)]
    arr_settings= [(1,1,1,1),(3,3,3,3),(5,5,5,5),(7,7,7,7),(3,5,5,5),(1,5,5,5),(3,7,1,7),(1,7,1,7)]

    
    ###----
    ### Make a plot
    fig= plt.figure()
    fig.set_size_inches(9.6,6)
    
    ### Page Title
    suptit= "Examples from Fig. 5 of White et al. (2018)"
    fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')

    ### Parameters for subplot area
    left,right,top,bottom= 0.06, 0.94, 0.935, 0.18
    npnx,gapx,npny,gapy= 4, 0.024, 2, 0.18
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    props= dict(cmap='binary',vmin=0,vmax=1.5,shading='flat')
    oid_names=['SCAI','MCAI','COP','I_org','ABCOP','N','SZ']
    id_select=[2,3,4]
    
    for i,arr_set in enumerate(arr_settings):
        ## Build a sample scene
        arr= get_array(arr0,centers,arr_set)

        ## Get organization metrics
        oid=np.asarray(com.identify_aggregate_and_get_org_indices(arr,diag=False))
        
        ax1= fig.add_axes([ix,iy-ly,lx,ly])
        pic1= ax1.pcolormesh(X,Y,arr,**props)
        subtit= '({})'.format(abc[i])
        plot_common(ax1,subtit)

        for i,(val,name) in enumerate(zip(oid[id_select],[oid_names[j] for j in id_select])):
            iyt= i*-2.4-2.1
            ax1.text(0,iyt,'{} = {:.5f}'.format(name,val),ha='left',va='top',fontsize=11)

        ix=ix+lx+gapx
        if ix+lx>right:
            ix=left
            iy=iy-ly-gapy
        
    ###--- Save or Show
    fnout = './Pics/FigS08_20x20_example.ideal_8.png'
    plt.savefig(fnout,bbox_inches='tight',dpi=150) 
    print(fnout)
    
    plt.show()
    return

def get_array(arr0,centers,arr_set):
    arr= np.copy(arr0)
    for center,sz in zip(centers,arr_set):
        fill_box(arr,center,sz)
    return arr

def fill_box(arr,center,size):
    y,x= center
    nx= ny= (size-1)//2
    arr[y-ny:y+ny+1, x-nx:x+nx+1]=1

def plot_common(ax,subtit):
    ax.set_title(subtit,ha='left',x=0.,fontsize=12)

    ax.grid(which='both')
    #ax.set_aspect(1)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.set_xticklabels('')
    ax.set_yticklabels('')
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='both',which='major',labelsize=10)
    
    return

   
if __name__=='__main__':
    main()
