"""
# 
# Idealized example for new ABCOP
# (diagonal connection is allowed)
#
# By Daeho Jin
# 2022.02.14
#
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
    nx,ny= 40,40
    lonb= np.arange(nx+1)
    latb= np.arange(ny+1)
    X,Y= np.meshgrid(lonb,latb)
    arr0= np.zeros([ny,nx])

    ### 1st aggregation
    arr0[1:3,8:20]=1
    arr0[4:7,8:11]=1
    arr0[4:5,18:22]=1

    ### 2nd aggregation
    y1,x1= 33,6
    arr0[y1-1:y1+2,x1-1:x1+2]=1

    y2,x2= y1-7,x1-2
    arr0[y2,x2]=1

    y3,x3= y1+2,x1+7
    arr0[y3,x3]=1

    ### 3rd aggregation
    y4,x4= y1,33
    arr0[y4+1,x4-1]=1
    arr0[y4,x4-1]=1
    arr0[y4-1,x4]=1
    arr0[y4-2,x4+1]=1
    arr0[y4+3,x4]=1

    ### Case 2: Modify the 2nd aggregation
    arr1= np.copy(arr0)
    arr1[y1-3:y1+4,x1-3:x1+4]=1

    ### Case 3: Add one
    y5,x5= 14,x4+2
    arr2= np.copy(arr1)
    arr2[y5,x5]=1


    ### Gathering scenes
    arrs= [arr0,arr1,arr2]
    
    ### Make Plot
    fig= plt.figure()
    fig.set_size_inches(11,5)
    
    ### Page Title
    suptit= "Idealized Aggregates for Org. Metrics Comparison"
    fig.suptitle(suptit,fontsize=15,y=0.96)

    ### Parameters for subplot area
    left,right,top,bottom= 0.06, 0.94, 0.935, 0.06
    npnx,gapx,npny,gapy= 4, 0.038, 1.4, 0.05
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    props= dict(cmap='binary',vmin=0,vmax=1.5,shading='flat')
    oid_names=['SCAI','MCAI','COP','I_org','ABCOP','N','SZ']
    id_select=[2,3,4]

    ### Three idealized scenes
    for k,arr in enumerate(arrs):
        ## Get organization metrics
        oid=np.asarray(com.identify_aggregate_and_get_org_indices(arr,diag=True))
        
        ax1= fig.add_axes([ix,iy-ly,lx,ly])
        pic1= ax1.pcolormesh(X,Y,arr,**props)
        subtit='({}) Case{} (N= {:.0f})'.format(abc[k],k+1,oid[-2])
        plot_common(ax1,subtit)

        for i,(val,name) in enumerate(zip(oid[id_select],[oid_names[j] for j in id_select])):
            iyt= i*-5.2-6
            ax1.text(0,iyt,'{} = {:.5f}'.format(name,val),ha='left',va='top',fontsize=11)

        ix=ix+lx+gapx

    ### Simple Example
    k+=1
    ly2,gp = ly/2.75, 0.1
    ax2= fig.add_axes([ix,iy-ly2-gp,lx,ly2])
    props= dict(cmap='binary',vmin=0,vmax=1.5,shading='flat')
    nx,ny= 8,4
    lonb= np.arange(nx+1)
    latb= np.arange(ny+1)
    X,Y= np.meshgrid(lonb,latb)
    arr0= np.zeros([ny,nx])
    arr0[2,1]=1
    arr0[2,3]=1
    arr0[1:3,5:7]=1
    pic2= ax2.pcolormesh(X,Y,arr0,**props)
    ax2.grid()
    ax2.xaxis.set_major_locator(MultipleLocator(1))
    ax2.yaxis.set_major_locator(MultipleLocator(1))
    ax2.yaxis.set_ticks_position('both')

    ax2.set_title('({}) Simple Example'.format(abc[k]),ha='left',x=0.,fontsize=12)
    for i,(y,x) in enumerate([(2,1),(2,3),(2,5)]):
        ax2.text(x+0.5,y+0.5,'{}'.format(abc[i].upper()),color='0.99',ha='center',va='center',fontsize=12)
    texts= ['A-B: r= 0.564, 0.564',r'       d= 2.000; $d_2$= 1.000',r'       V= 0.564; $V_{area}$= 0.177',' ',
            'B-C: r= 0.564, 1.128',r'       d= 2.550; $d_2$= 1.000',r'       V= 0.664; $V_{area}$= 0.442',
    ]
    buffer=0
    for j,txt in enumerate(texts):

        iyt= -0.37-j*0.24+buffer
        if len(txt)==1: buffer=0.15
        ax2.annotate(txt,(0.,iyt),ha='left',va='top',fontsize=11,xycoords='axes fraction')

        
    ###--- Save or Show
    fnout = './Pics/Fig03_Idealized_example_40x40.png'
    plt.savefig(fnout,bbox_inches='tight',dpi=150) 
    print(fnout)    
    plt.show()
    return

def plot_common(ax,subtit):
    ax.set_title(subtit,ha='left',x=0.,fontsize=12)

    ax.grid()
    ax.set_aspect(1)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_ticks_position('both')
    return





    
if __name__=='__main__':
    main()
