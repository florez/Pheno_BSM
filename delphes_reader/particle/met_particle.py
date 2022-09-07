from delphes_reader.particle.abstract_particle import Particle
from ROOT import TLorentzVector

class MetParticle(Particle):
    def __init__(self, event):
        super().__init__()
        self.TLV=TLorentzVector(0,0,0,0)
        n_met=event.MissingET.GetEntries()
        partMet=TLorentzVector()
        for j in range(n_met):
            partMet.SetPtEtaPhiM(
                event.GetLeaf("MissingET.MET").GetValue(j), 
                event.GetLeaf("MissingET.Eta").GetValue(j), 
                event.GetLeaf("MissingET.Phi").GetValue(j), 
                0.00 #GeV
            )
            self.TLV+=partMet
        self.Charge = 0.0
        self.Name="MET"
        self.Type="MET"