from delphes_reader.particle.abstract_particle import Particle
from delphes_reader.particle.electron_particle import ElectronParticle
from delphes_reader.particle.jet_particle import JetParticle
from delphes_reader.particle.met_particle import MetParticle
from delphes_reader.particle.muon_particle import MuonParticle


jets_names_dic = {
    'l_jet' : "j",
    'b_jet' : "b",
    'tau_jet' : "#tau",
    'other_jet' : "other"
}

leptons_names_dic = {
    'electron' : "e",
    'muon' : "#mu"
}

names_dic = jets_names_dic.copy()
names_dic.update(leptons_names_dic)

#CMS-detector Default Cuts
DEFAULT_CUTS={}
DEFAULT_CUTS["l_jet"]={
    "pt_min_cut":30.,
    "eta_min_cut":-5.,
    "eta_max_cut":+5.
}
DEFAULT_CUTS["b_jet"]={
    "pt_min_cut":30.,
    "eta_min_cut":-2.5,
    "eta_max_cut":+2.5
}
DEFAULT_CUTS["tau_jet"]={
    "pt_min_cut":20.,
    "eta_min_cut":-2.5,
    "eta_max_cut":+2.5
}

DEFAULT_CUTS["other_jet"]={
    "pt_min_cut":0.,
    "eta_min_cut":-5.,
    "eta_max_cut":+5.
}

DEFAULT_CUTS["electron"]={
    "pt_min_cut":25,
    "eta_min_cut":-2.3,
    "eta_max_cut":+2.3
}

DEFAULT_CUTS["muon"]=DEFAULT_CUTS["electron"]
def get_met(event):
    return MetParticle(event)

def get_unified(part_dic):
    unified=[]
    for key in part_dic.keys():
        unified+=part_dic[key].copy()
    part_dic[key].sort(reverse=True, key=Particle.pt)
    return {"all": unified}
    
def get_good_particles(particles_dic,kin_cuts=DEFAULT_CUTS):
    part_dic={}
    check=get_unified(particles_dic)["all"]
    for key in particles_dic.keys():
        if (key == "all"): continue
        name=names_dic[key]
        part_dic[key]=[]
        j=1
        particles_dic[key].sort(reverse=True, key=JetParticle.pt)
        for particle in particles_dic[key]:
            if not (particle.get_good_tag(kin_cuts)==1): continue
            crossed = False
            for check_particle in check:
                if (particle == check_particle) : continue 
                if (particle.DeltaR(check_particle) <= 0.3): 
                    crossed = True 
                    break
            if (crossed): continue
            particle.SetName(f"{name}_{{{j}}}")
            part_dic[key]+=[particle]
            j+=1
    return part_dic
    
def get_jets(event):
    jet_dic={}
    for key in jets_names_dic.keys():
        jet_dic[key]=[]
        
    for entry in range(event.Jet.GetEntries()):
        jet=JetParticle(event, entry)
        jet_dic[jet.Type]+=[jet].copy()
    
    for key in jet_dic.keys():
        jet_dic[key].sort(reverse=True, key=JetParticle.pt)
    
    return jet_dic

def get_good_jets(thing,kin_cuts=DEFAULT_CUTS):
    if type(thing) == dict :
        jets_dic=thing
    else:
        try:
            jets_dic=get_jets(thing)
        except:
            raise Exception("Error: A dictionary or an event was expected.")
    return get_good_particles(jets_dic,kin_cuts)

def get_muons(event):
    muons=[]    
    for entry in range(event.Muon.GetEntries()):
        muon=MuonParticle(event, entry)
        muons+=[muon].copy()
    return muons

def get_electrons(event):
    electrons=[]    
    for entry in range(event.Electron.GetEntries()):
        electron=ElectronParticle(event, entry)
        electrons+=[electron].copy()
    return electrons

def get_leptons(event):
    lepton_dic={
        'electron': get_electrons(event),
        'muon' : get_muons(event)
    }
    
    for key in lepton_dic.keys():
        lepton_dic[key].sort(reverse=True, key=Particle.pt)
    
    return lepton_dic

def get_good_leptons(thing,kin_cuts=DEFAULT_CUTS):
    if type(thing) == dict :
        leptons_dic=thing
    else:
        try:
            leptons_dic=get_leptons(thing)
        except:
            raise Exception("Error: A dictionary or an event was expected.")
    
    leptons=get_unified(get_good_particles(leptons_dic,kin_cuts))["all"]
    
    j=1
    for lepton in leptons:
        lepton.SetName(f"lep_{{{j}}}")
        j+=1
    return leptons