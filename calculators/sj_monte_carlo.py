import numpy as np

def simulate(n=50000, nd=5e16, na=5e16, wn_um=2., wp_um=2.,
             sigma_nd_pct=5., sigma_na_pct=5., sigma_cd_um=0.05,
             ionization=1., angle_sigma_deg=0., angle_sensitivity_per_deg=0.,
             balance_limit_pct=10., seed=42):
    """Lightweight statistical sensitivity model; not a fab-qualified yield model."""
    rng=np.random.default_rng(seed)
    nd_s=nd*(1+rng.normal(0,sigma_nd_pct/100,n))
    na_s=na*(1+rng.normal(0,sigma_na_pct/100,n))
    wn_s=np.clip(wn_um+rng.normal(0,sigma_cd_um,n),1e-6,None)
    wp_s=np.clip(wp_um+rng.normal(0,sigma_cd_um,n),1e-6,None)
    angle=rng.normal(0,angle_sigma_deg,n)
    implant_factor=np.clip(1-angle_sensitivity_per_deg*np.abs(angle),0,None)
    ratio=na_s*wp_s*ionization*implant_factor/(nd_s*wn_s)
    ok=np.abs(ratio-1)<=balance_limit_pct/100
    return ratio,ok,angle
