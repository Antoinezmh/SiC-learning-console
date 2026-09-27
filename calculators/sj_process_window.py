import numpy as np

def charge_ratio_grid(nd, na, wn_nom, wp_nom, width_tol_pct=5, dose_tol_pct=5, ionization=1.0, points=81):
    """First-order Monte-Carlo-free process-window grid for QP/QN. Teaching model."""
    w=np.linspace(-width_tol_pct,width_tol_pct,points)/100
    d=np.linspace(-dose_tol_pct,dose_tol_pct,points)/100
    W,D=np.meshgrid(w,d)
    qn=nd*(1+D)*wn_nom*(1+W)
    qp=na*(1-D)*wp_nom*(1-W)*ionization
    return w*100,d*100,qp/qn

def within_window(ratio, tolerance_pct=5):
    lo=1-tolerance_pct/100
    hi=1+tolerance_pct/100
    return (ratio>=lo)&(ratio<=hi)
