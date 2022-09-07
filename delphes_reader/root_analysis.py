import ROOT

def get_kinematics_row(*args):
    particles=list(args)
    co_particles=particles.copy()
    row = {} #{'header': value}
    for particle in particles:
        name=particle.Name
        row[f"pT_{{{name}}}(GeV)"]=particle.pt()
        row[f"#eta_{{{name}}}"]=particle.eta()
        row[f"#phi_{{{name}}}"]=particle.phi()
        row[f"Energy_{{{name}}}(GeV)"]=particle.energy()
        row[f"Mass_{{{name}}}(GeV)"]=particle.m()
        co_particles.pop(0)
        for co_particle in co_particles:
            co_name=co_particle.Name
            row[f"#Delta{{R}}_{{{name}{co_name}}}"]=particle.DeltaR(co_particle)
            row[f"#Delta{{#eta}}_{{{name}{co_name}}}"]=particle.DeltaEta(co_particle)
            row[f"#Delta{{#phi}}_{{{name}{co_name}}}"]=particle.DeltaPhi(co_particle)
            row[f"#Delta{{pT}}_{{{name}{co_name}}}(GeV)"]=particle.sDeltaPT(co_particle)
            row[f"#Delta{{#vec{{pT}}}}_{{{name}{co_name}}}(GeV)"]=particle.vDeltaPT(co_particle)
            row[f"#Delta{{#vec{{p}}}}_{{{name}{co_name}}}(GeV)"]=particle.vDeltaP(co_particle)
    return row

hist_bins_dict_default={
    "#Delta{R}":[8,0,7],
    "#Delta{#eta}":[20,-5,5],
    "#Delta{#phi}":[13,-3.25,3.25],
    "#Delta{pt}":[15, 0.0, 1500.0],
    "#Delta{#vec{pT}}":[30, 0.0, 3000.0],
    "#Delta{#vec{p}}":[30, 0.0, 3000.0],
    "MET(GeV)":[20, 0.0, 1000.0],
    "pT_": [40, 0.0, 2000.0],
    "#eta_":[20, -5, 5],
    "#phi_":[64, -3.2, 3.2],
    "Mass_":[40, 0.0, 1000.0]
}

def make_histograms(df,integral=1.0,hist_bins_dict=hist_bins_dict_default):
    hist_dict={}
    for key in dict(df).keys():
        for hist_key in hist_bins_dict.keys():
            if hist_key in key:
                bins=hist_bins_dict.get(hist_key,False)
                break
        if not (bins): 
            print("No Histogram Dictionary for ",key)
        else: 
            h=ROOT.TH1F(
                key,f"; {key}; Events",
                bins[0],bins[1],bins[2]
            )
            h.SetDirectory(0)
            for value in df[key]:
                h.Fill(value)
            h.Scale(integral/h.Integral())
            hist_dict.update({key : h})
    return hist_dict

class Quiet:
    """Context manager for silencing certain ROOT operations.  Usage:
    with Quiet(level = ROOT.kInfo+1):
       foo_that_makes_output

    You can set a higher or lower warning level to ignore different
    kinds of messages.  After the end of indentation, the level is set
    back to what it was previously.
    """
    def __init__(self, level=ROOT.kError+1):
        self.level = level

    def __enter__(self):
        self.oldlevel = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = self.level

    def __exit__(self, type, value, traceback):
        ROOT.gErrorIgnoreLevel = self.oldlevel