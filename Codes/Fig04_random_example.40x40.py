"""
# 
# Generate random objects for comparing org. metrics
#
# Daeho Jin, 2022.02.14
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
    ## Parameters
    nx=ny= 40  ## grid size
    tgt_den= 0.05  ## target density
    
    max_cells= int(nx*ny*tgt_den)

    nSample=1000  ## Number of samples
    rg_seed=12321  ## random seed
    
    lonb= np.arange(nx+1)
    latb= np.arange(ny+1)
    X,Y= np.meshgrid(lonb,latb)

    ### Case1: Uniform over whole domain
    arr0= np.zeros([nSample,ny,nx])
    xx= X[:-1,:-1].reshape(-1)
    yy= Y[:-1,:-1].reshape(-1)
    rg= np.random.default_rng(rg_seed)
    
    for k in range(nSample):
        rg.shuffle(xx)
        rg.shuffle(yy)
        arr0[k,xx[:max_cells],yy[:max_cells]]=1
        
    ### Case2: Uniform over small areas (40% of x, 40% of y; two corners) 
    arr2= np.zeros([nSample,ny,nx])
    rg= np.random.default_rng(rg_seed)
    for k in range(nSample):
        rg.shuffle(xx)
        rg.shuffle(yy)
        cond1= np.logical_and(xx<nx*0.4,yy<ny*0.4)
        cond2= np.logical_and(xx>=nx*0.6,yy>=ny*0.6)
        cond= np.logical_or(cond1,cond2)
        arr2[k,xx[cond][:max_cells],yy[cond][:max_cells]]=1

    ### Case3: Gaussian over two corner areas
    arr3= np.zeros([nSample,ny,nx])
    rg= np.random.default_rng(rg_seed)
    ixy1,std1= (ny*0.2,nx*0.2), 3  ## Set Center and STD 
    ixy2,std2= (ny*0.8,nx*0.8), 4  ## Set Center and STD 

    for k in range(nSample):
        x0= rg.standard_normal(size=max_cells)
        y0= rg.standard_normal(size=max_cells)

        ### For one corner
        ct=i=0
        y1,x1= np.rint(std1*x0+ixy1[0]).astype(int), np.rint(std1*y0+ixy1[1]).astype(int)
        y1,x1= y1[y1>=0], x1[x1>=0]  ## Exclude negative values
        while(ct<=int(max_cells/2)):
            if arr3[k,y1[i],x1[i]]==0:
                arr3[k,y1[i],x1[i]]=1
                ct+=1
            i+=1

        ## For the other
        i=0
        y2,x2= np.rint(std2*x0+ixy2[1]).astype(int), np.rint(std2*y0+ixy2[0]).astype(int)
        y2,x2= y2[y2<ny],x2[x2<nx]  ## Exclude out of domain
        while(ct<=max_cells):
            if arr3[k,y2[i],x2[i]]==0:
                arr3[k,y2[i],x2[i]]=1
                ct+=1
            i+=1

    ### Case4: Add two grid cells on Case3
    arr4= np.copy(arr3)
    arr4[:,3,36]=1
    arr4[:,36,3]=1

    
    arrs= [arr0,arr2,arr3,arr4,]
    ois= []
    for arr in arrs:
        ois.append(com.identify_aggregate_and_get_org_indices(arr,diag=True)) #False))

    ###----
    ### Make a plot
    fig= plt.figure()
    fig.set_size_inches(11,9)
    
    ### Page Title
    suptit= "Random Aggregates for Metrics Comparison (Target_density={})".format(tgt_den)
    fig.suptitle(suptit,fontsize=16,y=0.98)

    ### Parameters for subplot area
    left,right,top,bottom= 0.06, 0.94, 0.935, 0.06
    npnx,gapx,npny,gapy= 4, 0.04, 2.8, 0.04
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    abc='abcdefgh'
    props= dict(cmap='binary',vmin=0,vmax=1.5,shading='flat')
    oid_names=['SCAI','MCAI','COP','I_org','ABCOP','N','SZ']
    id_select=[2,3,4] #[0,1] #
    
    for i in range(len(arrs)):
        idx=3  ## Index for selecting a sample scene
        arr= arrs[i][idx,:]
        oid= ois[i][idx]

        ax1= fig.add_axes([ix,iy-ly,lx,ly])
        pic1= ax1.pcolormesh(X,Y,arr,**props)
        subtit='({}) Case {} (N= {:.0f})'.format(abc[i],i+1,oid[-2])
        plot_common(ax1,subtit)

        if (i+1)%npnx==0:
            ax1.tick_params(labelright=True)
        for i,(val,name) in enumerate(zip(oid[id_select],[oid_names[j] for j in id_select])):
            iyt= i*-4.5-6
            ax1.text(0,iyt,'{} = {:.5f}'.format(name,val),ha='left',va='top',fontsize=12)

        ix=ix+lx+gapx
        if ix+lx>right:
            ix=left
            iy=iy-ly*1.3-gapy

    ### Draw box plot
    ly2= ly*0.75
    xloc= np.arange(len(arrs))
    wd= 0.7
    whiskerprops= dict(linewidth=1.5,alpha=0.8,linestyle='-',color='0.1')
    medianprops = dict(color='r',linewidth=1.5,alpha=0.8)
    boxprops= dict(linewidth=1.5,color='0.1',alpha=0.8) #,facecolor='0.8')
    i0=len(arrs)
    for i,idx in enumerate(id_select):
        box_data=[]
        for oid in ois:
            box_data.append(oid[:,idx])

        ax2= fig.add_axes([ix,iy-ly2,lx,ly2])
        box1= ax2.boxplot(box_data,positions=xloc,widths=wd,
                    whis=(5,95),showfliers=False,showmeans=False, medianprops=medianprops,
                    whiskerprops=whiskerprops, #meanprops=meanprops, #flierprops=flierprops,
                    showcaps=False,patch_artist=False,boxprops=boxprops,
                    )
        subtit='({}) {}'.format(abc[i+i0],oid_names[id_select[i]])
        xt_lab= ['Case{}'.format(val+1) for val in range(len(arrs))]
        plot_common_box(ax2,subtit,xt_lab)
        
        ix=ix+lx+gapx
        if ix+lx>right:
            ix=left
            iy=iy-ly*1.4-gapy
    ###--- Save or Show
    var_nm= ''.join([str(val) for val in id_select])
    fnout = './Pics/Fig04_random_example_40x40.tgt_den{}.{}.png'.format(tgt_den,var_nm)
    plt.savefig(fnout,bbox_inches='tight',dpi=150) 
    print(fnout)
    
    plt.show()
    return

def plot_common(ax,subtit):
    ax.set_title(subtit,ha='left',x=0.,fontsize=13)

    ax.grid()
    ax.set_aspect(1)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(labelsize=10)
    return
def plot_common_box(ax,subtit,xt_lab):
    ax.set_title(subtit,ha='left',x=0.,fontsize=13)
    ylim= ax.get_ylim()
    ax.set_ylim([0,ylim[1]])
    if ylim[1]<0.5:
        ax.yaxis.set_major_locator(MultipleLocator(0.05))

    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(axis='y',ls='--',lw=1.2,alpha=0.7)
    ax.grid(axis='x',which='minor',ls='--',lw=1.2,alpha=0.7)
    #ax.set_aspect(1)
    #ax.xaxis.set_major_locator(MultipleLocator(5))
    #
    #ax.yaxis.set_ticks_position('both')
    ax.set_xticklabels(xt_lab)
    ax.tick_params(labelsize=10)
    return


    
if __name__=='__main__':
    main()
