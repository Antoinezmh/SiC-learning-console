import numpy as np

ANCHORS={
 "Multi-epi":{5:0.75,10:1.50},
 "TFE":{5:0.23,10:0.29},
 "MeV implantation":{5:0.20,10:0.45},
 "Channeling":{5:0.08,10:0.21},
}
def interpolate_cycle_time(route,depth_um):
    """Linear interpolation/extrapolation through Harada 5/10 um anchors. Extrapolation is engineering model."""
    a,b=ANCHORS[route][5],ANCHORS[route][10]
    return a+(depth_um-5)*(b-a)/5

def crossover(route_a,route_b,lo=3,hi=25):
    xs=np.linspace(lo,hi,2000)
    d=np.array([interpolate_cycle_time(route_a,x)-interpolate_cycle_time(route_b,x) for x in xs])
    idx=np.where(np.sign(d[:-1])!=np.sign(d[1:]))[0]
    return None if not len(idx) else float(xs[idx[0]])
