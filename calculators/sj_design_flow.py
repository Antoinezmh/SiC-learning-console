import itertools, math
from calculators.sj_physics import idealized_sj

def initial_structure(vb_v, route, margin=0.12, eps_r=9.7, mu_n=900., ec_vertical=2.5e6, ec_lateral=2.0e6):
    """Engineering initializer, not sign-off geometry."""
    target=vb_v*(1+margin)
    width_defaults={"Channeling":1.25,"MeV implantation":1.5,"Multi-epi":2.0,"TFE":2.5}
    wn=width_defaults[route]
    phy=idealized_sj(target,wn,eps_r,mu_n,ec_vertical,ec_lateral)
    return {"target_with_margin_v":target,"column_um":phy["column_um"],"wn_um":wn,"wp_um":wn,
            "nd_cm3":phy["nd_max_cm3"],"na_cm3":phy["nd_max_cm3"],"rdrift_ohm_cm2":phy["ron_ohm_cm2"]}

def ron_budget(rdrift_ohm_cm2,rch_mohm_cm2=.04,rjfet_mohm_cm2=0.,rsub_mohm_cm2=.10,other_mohm_cm2=0.):
    vals={"Rch":rch_mohm_cm2,"RJFET":rjfet_mohm_cm2,"Rdrift":rdrift_ohm_cm2*1e3,"Rsub":rsub_mohm_cm2,"Other":other_mohm_cm2}
    vals["Total"]=sum(vals.values())
    return vals

def mesh_hints(wn_um,column_um):
    return {"pillar_lateral_max_um":wn_um/10,"junction_refine_um":min(wn_um/25,.05),
            "vertical_bulk_max_um":max(column_um/80,.05),
            "note":"Generic starting mesh only; refine by field/impact-ionization convergence."}
