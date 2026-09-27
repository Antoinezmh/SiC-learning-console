def tutorial_ron_sp(vb_v: float) -> float:
    """ICSCRM tutorial empirical SiC unipolar-limit relation; returns ohm*cm^2."""
    return 2.8e-11 * vb_v ** 2.28
