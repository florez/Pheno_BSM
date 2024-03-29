from delphes_reader.particle.abstract_particle import Particle

class ElectronParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Electron.PT").GetValue(j), 
            event.GetLeaf("Electron.Eta").GetValue(j), 
            event.GetLeaf("Electron.Phi").GetValue(j), 
            0.000511 #GeV
        )
        self.Charge = event.GetLeaf("Electron.Charge").GetValue(j)
        self.Name="e"
        self.Type="electron"