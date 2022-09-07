from delphes_reader.particle.abstract_particle import Particle

class MuonParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Muon.PT").GetValue(j), 
            event.GetLeaf("Muon.Eta").GetValue(j), 
            event.GetLeaf("Muon.Phi").GetValue(j), 
            0.1056583755 #GeV
        )
        self.Charge = event.GetLeaf("Muon.Charge").GetValue(j)
        self.Name="#mu"
        self.Type="muon"