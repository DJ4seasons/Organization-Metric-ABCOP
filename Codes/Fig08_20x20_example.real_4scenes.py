"""
#
# This is for sample CPR map to compare Org. Metrics 
# Fig. 2 of Tobin et al. (2012), and reproduced later in Fig. 4 of White et al. (2018)
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
    nx,ny= 20,20
    lonb= np.arange(nx+1)
    latb= np.arange(ny+1)
    X,Y= np.meshgrid(lonb,latb)
    arr0= np.zeros([ny,nx])

    ### Case1
    temp0 = np.copy(arr0)
    temp0[11,12:16]=1
    temp0[12,[10,13,14,15]]=1
    temp0[14:16,6:12]=1
    temp0[16,12]=1
    temp0[17,10]=1
    temp0= temp0[::-1,:]

    ### Case2
    temp1 = np.copy(arr0)
    temp1[0:2,9]=1
    temp1[4,2]=1
    temp1[10,-1]=1
    temp1[11,11:13]=1
    temp1[12,11:16]=1
    temp1[-3,8:10]=1
    temp1[-2,6:11]=1
    temp1[-1,6:9]=1

    ### Case3
    temp2 = np.copy(arr0)
    temp2[3,-3:-1]=1
    temp2[8,[-4,-6,-7]]=1
    temp2[9,10:-3]=1
    temp2[10,8:14]=1
    temp2[11,7:13]=1
    temp2[13,3]=1
    temp2[14,2:5]=1
    temp2[15,1:4]=1
    temp2[16,1:3]=1
    
    ### Case4
    temp4 = np.copy(arr0)
    temp4[0,14:18]=1
    temp4[1,[8,13,14,15]]=1
    temp4[2,15]=1
    temp4[3,12]=1
    temp4[4,10:13]=1
    temp4[5,9:14]=1
    temp4[6,5:8]=1; temp4[6,10:15]=1
    temp4[7,6]=1
    temp4= temp4[::-1,:]


    arrs= [temp0,temp1,temp2,temp4]

    ###----
    ### Make a plot
    fig= plt.figure()
    fig.set_size_inches(6,7.5)
    
    ### Page Title
    suptit= "Examples from Fig. 2 of Tobin et al. (2012)"
    fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')

    ### Parameters for subplot area
    left,right,top,bottom= 0.06, 0.94, 0.935, 0.18
    npnx,gapx,npny,gapy= 2, 0.056, 2, 0.18
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    props= dict(cmap='binary',vmin=0,vmax=1.5,shading='flat')
    oid_names=['SCAI','MCAI','COP','I_org','ABCOP','N','SZ']
    id_select=[2,3,4]
    
    for i,arr in enumerate(arrs):
        ## Get organization metrics
        oid=np.asarray(com.identify_aggregate_and_get_org_indices(arr,diag=False))
        
        ax1= fig.add_axes([ix,iy-ly,lx,ly])
        pic1= ax1.pcolormesh(X,Y,arr,**props)
        subtit='({}) Case {} (N= {:.0f})'.format(abc[i],i+1,oid[-2])
        plot_common(ax1,subtit)

        for i,(val,name) in enumerate(zip(oid[id_select],[oid_names[j] for j in id_select])):
            iyt= i*-2.25-3
            ax1.text(0,iyt,'{} = {:.5f}'.format(name,val),ha='left',va='top',fontsize=11)

        ix=ix+lx+gapx
        if ix+lx>right:
            ix=left
            iy=iy-ly-gapy
        
    ###--- Save or Show
    fnout = './Pics/Fig8_20x20_example.real_4.png'
    plt.savefig(fnout,bbox_inches='tight',dpi=150) 
    print(fnout)
    
    plt.show()
    return

def plot_common(ax,subtit):
    ax.set_title(subtit,ha='left',x=0.,fontsize=12)

    ax.grid(which='both')
    ax.set_aspect(1)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='both',which='major',labelsize=10)
    
    return


    
if __name__=='__main__':
    main()
