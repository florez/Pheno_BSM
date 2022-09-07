from abc import ABC
from ROOT import (
    TLorentzVector,
    TVector3,
    TVector2,
    TMath
)

class Particle(ABC):
    def __init__(self,*args,**kwargs):
        self.TLV=TLorentzVector()
        self.Charge=kwargs.get("charge",0.0)
        self.Name=""
        self.Type=""
    
    
    #
    def GetCharge(self):
        charge=self.Charge
        return charge
    
    def GetTLV (self):    
        tlv=self.TLV
        return tlv

    def GetName(self):
        name=self.Name
        return name
    
    def SetName (self,newName):
        self.Name=newName
    
    def pt(self):
        # Returns transverse momentum
        TLV = self.TLV
        return TLV.Pt()
    
    def p(self):
        # Returns full momentum
        TLV = self.TLV
        return TLV.P()
    
    def pl(self):
        # Returns longitudinal momentum
        p = self.TLV.P()
        pt= self.TLV.Pt()
        return TMath.Sqrt((p-pt)*(p+pt))

    def eta(self):
        # Returns jet pseudorapidity
        TLV = self.TLV
        return TLV.Eta()

    def phi(self):
        # Returns jet pseudorapidity
        phi=self.TLV.Phi()
        return phi
    
    def m(self):
        # Returns jet pseudorapidity
        TLV = self.TLV
        return TLV.M()
    
    def energy(self):
        # Returns jet pseudorapidity
        TLV = self.TLV
        return TLV.Energy()

    def get_good_tag(self,cuts):
        jet_cuts=cuts.get(self.Type)
        pt_min_cut=jet_cuts.get("pt_min_cut")
        pt_max_cut=jet_cuts.get("pt_max_cut")#optional
        eta_min_cut=jet_cuts.get("eta_min_cut")
        eta_max_cut=jet_cuts.get("eta_max_cut")
        
        pt_cond= (self.pt()>= pt_min_cut)
        if pt_max_cut:
            if not (pt_max_cut>pt_min_cut):
                raise Exception("Error: pt_max must be major than pt_min")
            pt_cond = pt_cond and (self.pt()<= pt_min_cut)
        eta_cond = (self.eta()>= eta_min_cut) and (self.eta()<= eta_max_cut)
        
        if (pt_cond and eta_cond):
            self.GoodTag=1
        else:
            self.GoodTag=0
            
        return self.GoodTag
    
    ### Delta methods
    def DeltaR(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return TLV1.DeltaR(TLV2)

    def DeltaEta(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return (TLV1.Eta() - TLV2.Eta())

    def DeltaPhi(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return TLV1.DeltaPhi(TLV2)

    def sDeltaPT(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        return (TLV1.Pt() - TLV2.Pt())

    def vDeltaPT(self, v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        a=TVector2(TLV1.Px(), TLV1.Py())
        b=TVector2(TLV2.Px(), TLV2.Py())
        c=a-b
        return c.Mod()

    def vDeltaP(self,v2):
        TLV1 = self.TLV
        TLV2 = v2.GetTLV()
        a=TVector3(TLV1.Px(), TLV1.Py(), TLV1.Pz())
        b=TVector3(TLV2.Px(), TLV2.Py(), TLV2.Pz())
        c=a-b
        return c.Mag()