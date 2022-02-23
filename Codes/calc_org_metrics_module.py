'''
Common module for calculating organization metrics

By Daeho Jin
2022.02.14
'''

import numpy as np
import math

def identify_aggregate_and_get_org_indices(amap0,diag=False,channel=False):
    """
    For a given 2d or 3d array (amap0; objects are marked by True), 
        identify aggregates and 
        call the function to calculate Org. Metrics
    """

    ## Check input array
    data_dim= amap0.shape
    if len(data_dim)==2:
        amap0= amap0[np.newaxis,:,:]  ## Supposed to be [time, y-axis, x-axis]
    nt,ny,nx= amap0.shape
    print_dt= 1000 if nt<10000 else 5000
    
    ## Identify aggregates
    metrics=[] 
    for t1 in range(nt):
        amap= np.copy(amap0[t1,:])
        if t1==0: print(amap.shape)
        
        c_info=[]
        while amap.sum()>0:
            cluster=[]
            bns= np.where(amap==True)
            init_xy= (bns[0][0],bns[1][0])

            cluster.append(init_xy)
            amap[init_xy[0],init_xy[1]]=False
            find_neighbor(init_xy,cluster,amap,diag=diag,channel=channel)

            cluster=np.asarray(cluster)
            if channel and (cluster[:,1].max()-cluster[:,1].min())>nx/2:
                cluster[cluster[:,1]>nx/2,1]-=nx
            center_yx= np.mean(cluster,axis=0)
            c_info.append((*center_yx,cluster.shape[0]))

        ## Get org. metrics based on identified aggregates above
        metrics.append(calc_org_indexes(c_info,(ny,nx),channel=channel))
        if (t1+1)%print_dt==0:
            print(t1+1,np.round(metrics[-1],3))

    metrics= np.asarray(metrics)
    if nt==1:
        metrics=metrics.squeeze()
    return metrics


def find_neighbor(ixy,clst,amap,diag=False,channel=False):
    """ 
    Find neighbor for 4-direction (diag==False) or 8-direction (diag=True); Recursive
    Once found, the grid cell info is stored in clst, and marked as False
    ixy: tuple, (iy,ix)
    amap: an index map for a day, T/F
    clist: xys for one group
    """
    
    ny,nx=amap.shape
    nxys=neighbor_info(ixy,ny,nx,diag=diag,channel=channel)
    for y1,x1 in nxys:
        if amap[y1,x1]:
            clst.append((y1,x1))
            amap[y1,x1]=False
            find_neighbor((y1,x1),clst,amap,diag=diag,channel=channel)
    return 

def neighbor_info(lxy,ny,nx,diag=False,channel=False):
    """
    Input: co-ordinate of 1 point, (y,x)
    Output: a list of co-ordinate which is neighboring to input. 
    if "diag"==False: check 4-direction
    else:           : check 8-direction including diagonal direction
    """

    ly,lx=lxy
    if diag:
        tmpmap= np.ones([3,3])
    else:
        tmpmap= np.zeros([3,3])
        tmpmap[1,:]=1; tmpmap[:,1]=1
    tmpmap[1,1]=0  ## Exclude Self
    
    if ly==0:
        tmpmap[0,:]=0
    elif ly==ny-1:
        tmpmap[2,:]=0

    if not channel:
        if lx==0:
            tmpmap[:,0]=0
        elif lx==nx-1:
            tmpmap[:,2]=0

    tmplist=np.where(tmpmap==1)
    nlist=[]
    for ty,tx in zip(*tmplist):
        x1= tx+lx-1
        if x1>=nx: x1-=nx
        nlist.append((ty+ly-1,x1))

    return nlist


def calc_org_indexes(c_info,domain_size,channel=False):
    '''
    c_info: list cotains aggregate info, (center_y, center_x, size)
    L_gridcells: characteristic length in terms of number of grid cells
    domain_size: [ny,nx]

    Calculate SCAI, MCAI, COP, Iorg, ABCOP
    ABCOP min_crt of d2=1
    1. Change distance from dist to d2=dist-r1-r2
    2. Select Maximum Interaction Potential instead of nearest distance

    '''
        
    ny,nx=domain_size
    A_domain= nx*ny
    L_domain= math.sqrt(A_domain) # Length of domain
    r_domain= math.sqrt(A_domain/math.pi) # nominal radius of domain

    ci = np.asarray(c_info)
    
    N = ci.shape[0]  # Total number of aggregates
    N_tot = (N*(N-1)/2)  # Total number of combination
    if N>1: rr = np.sqrt(ci[:,-1]/math.pi)  # Estimated radius
    
    D0 = 1.; D2= 0.
    scai=mcai=99.9
    cop = 0.
    abcop= 0.
    abcop_crt=1
    Iorg=0.
    tsz=0.

    if N>=2:
        ### Build distance matrix
        dd_mtx= np.empty([N,N],dtype=float)
        for i in range(N):
            dd_mtx[i,:]= np.sqrt(np.power(ci[:,:2]-ci[i,:2].reshape([1,2]),2).sum(axis=1))
            dd_mtx[i,i]= 1.e7  ## In order to exclude self

        ### In the case of channel condition
        if channel:
            dd_mtx2= np.empty_like(dd_mtx)
            half_idx= ci[:,1]>=nx/2
            ci[half_idx,1]-=nx        
            for i in range(N):
                dd_mtx2[i,:]= np.sqrt(np.power(ci[:,:2]-ci[i,:2].reshape([1,2]),2).sum(axis=1))
                dd_mtx2[i,i]= 1.e7
            dd_mtx= np.minimum(dd_mtx,dd_mtx2)

        
        ### Parameters for SCAI and MCAI
        N_max= L_domain**2/2
        scai_norm= N_max*L_domain
        
        ### For all pairs
        for i in range(N-1):
            for j in range(i+1,N):
                # COP
                cop+=(rr[i]+rr[j])/dd_mtx[i,j]/N_tot

                # SCAI
                D0*=math.pow(dd_mtx[i,j],1/N_tot)

                # MCAI
                D2+=max((dd_mtx[i,j]-rr[i]-rr[j]),0)/N_tot
        scai = N/scai_norm*D0*1000
        mcai = N/scai_norm*D2*1000


        ### For each aggregate
        nnd = np.empty([N,])  ## nearest neighbor distance for Iorg
        for i in range(N):
            dd = dd_mtx[i,:]

            # ABCOP
            ddv2= dd-rr-rr[i]
            ddv2[ddv2<abcop_crt]=abcop_crt
            V2max= ((ci[i,-1]+ci[:,-1])/2/A_domain/(ddv2/L_domain)).max()
            abcop+= V2max

            # For Iorg
            nnd[i] = dd.min()                
                
        ### Iorg
        #ref_dist0 = np.linspace(0,L_domain*1.5,501)
        ref_dist0= np.arange(0,L_domain*1.5,0.1)  ## Iorg value change by "step" value
        ref_dist = (ref_dist0[1:]+ref_dist0[:-1])/2.
        nnd_random = 1-np.exp(-N/L_domain**2*math.pi*ref_dist**2)
        nnd = np.cumsum(np.histogram(nnd,bins=ref_dist0)[0]/N)
        Iorg = np.trapz(nnd,x=nnd_random)

        tsz= ci[:,-1].mean()
    elif N==1:
        rr = np.sqrt(ci[0,-1]/math.pi)
        ad= ci[0,-1]/A_domain
        abcop= np.sqrt(np.pi)/2*ad/(2-np.sqrt(ad))
        
    return scai,mcai,cop,Iorg,abcop,N,tsz
