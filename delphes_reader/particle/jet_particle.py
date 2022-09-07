from delphes_reader.particle.abstract_particle import Particle
JET_TYPES={
        "BTag0_TauTag0":"l_jet",
        "BTag1_TauTag0":"b_jet",
        "BTag0_TauTag1":"tau_jet"
    }

class JetParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.TLV.SetPtEtaPhiM(
            event.GetLeaf("Jet.PT").GetValue(j), 
            event.GetLeaf("Jet.Eta").GetValue(j), 
            event.GetLeaf("Jet.Phi").GetValue(j), 
            event.GetLeaf("Jet.Mass").GetValue(j)
        )
        self.BTag   = int(event.GetLeaf("Jet.BTag").GetValue(j))
        self.TauTag = int(event.GetLeaf("Jet.TauTag").GetValue(j))
        self.Charge = event.GetLeaf("Jet.Charge").GetValue(j)
        self.Type=self._jet_type()
        self.Name=f'{self.Type}_{{{j}}}'
        
    def _jet_type(self):
        return JET_TYPES.get(f'BTag{self.BTag}_TauTag{self.TauTag}',"other_jet")