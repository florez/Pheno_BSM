from ROOT import TCanvas, THStack, TH1F, TFile
from ROOT import kBlue, kRed, kBlack
from bcml4pheno import bcml_model
from bsm_ml import *
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


part_dic={
    "b_tau_tau_hadronic":[
        "#tau_{1}",
        "#tau_{2}",
        "b_{1}"
        ],

    "b_b_tau_tau_hadronic" :[
        "#tau_{1}",
        "#tau_{2}",
        "b_{1}",
        "b_{2}"
        ],

    "b_tau_tau_semileptonic" :[
        "#tau_{1}",
        "lep_{1}",
        "b_{1}"
        ],

    "b_b_tau_tau_semileptonic" :[
        "#tau_{1}",
        "lep_{1}",
        "b_{1}",
        "b_{2}"
        ]
}


class LQ_Log_Reg(bcml_model):
    def __init__(self,mass,ch,csv_files_path):
        self.mass=mass
        self.channels=ch
        self.path=csv_files_path
        self._fit_log_reg_model()

    def _get_signal_names(self):
        if self.mass < 1000:
            name=f"LQ_LQ_0{self.mass}"
            name2=f"Tau_LQ_0{self.mass}"
        else :
            name=f"LQ_LQ_{self.mass}"
            name2=f"Tau_LQ_{self.mass}"
        self.signal_names=[name, name2]
        self.bkg_names=[
            "ttbar",
            "stop",
            "z_jets",
            "w_jets",
            "ww",
            "wz",
            "zz"
        ]
    
    def _get_features_by_key(self,key):
        lep_a=part_dic[key][0]
        lep_b=part_dic[key][1]
        features=[
            'MET(GeV)',
            '#phi_{MET}',
            f"Q_{{{lep_a}}}Q_{{{lep_b}}}",
            'light_jets_multiplicity'
        ]
        for particle in part_dic[key]:
            features+=[
                f'Energy_{{{particle}}}(GeV)',
                f'pT_{{{particle}}}(GeV)',
                f'#phi_{{{particle}}}',
                f'#eta_{{{particle}}}'
            ]
        return features
    
    def _get_features(self,channels):
        sets=[set(self._get_features_by_key(channel)) for channel in channels]
        common_features=sets[0]
        for set_ in sets:
            common_features = common_features.intersection(set_)
        self.features=list(common_features)

        
    def _prepare_data(self):
        self._get_features(self.channels)
        self._get_signal_names()
        self.signal_data=concat_channels(
            self.path,
            self.signal_names,
            self.channels,
            self.features
        )
        self.bkg_data=concat_channels(
            self.path,
            self.bkg_names,
            self.channels,
            self.features
        )
        
        pred1 , labels1= prepare_to_train(self.signal_data,self.bkg_data)
        trainPred, testPred, trainLab, testLab = train_test_split(pred1, labels1, test_size=0.30)
        self.trainPred=trainPred
        self.testPred=testPred
        self.trainLab=trainLab
        self.testLab=testLab
    
    def _fit_log_reg_model(self):
        self._prepare_data()
        self.logreg_model = bcml_model(
            make_pipeline(
                StandardScaler(), 
                LogisticRegression()
            )
        )

        self.logreg_model.fit(self.trainPred, self.trainLab)
    
    def get_log_reg_model(self):
        return self.logreg_model
    
    def _draw_discrtiminator(self,name,images_folder):
        c1 = TCanvas( f'c-{name}', '', 0, 0, 1280, 720)
        c1.SetGrid()
        c1.SetLogy()
        hs = THStack(name,name)
        colors = [kBlue,kRed,3, 7, 6, kBlack, 2,  9, 1, 43, 97, 38, 3, 7, 6, kBlack, 2, 4, 8]
        hist_dict={}
        for i, channel in enumerate(self.channels):
            h = TH1F(
                f"{name}_{channel}",
                f"{name};ML-score;nevents(137/fb)", 
                100, 0.0,1.0
            )
            h.SetLineWidth(1)
            h.SetLineColor(kBlack)
            h.SetFillColor(colors[i])
            for score in self.logreg_model.predict_proba(concat_channels(self.path,[name],self.channels,self.features)):
                h.Fill(score)
            h.Scale(get_yield(self.path,[name],channel)/h.Integral())
            hist_dict[channel]=h
            hs.Add(h)
        hs.Draw("HIST")
        c1.SaveAs(os.path.join(os.getcwd(),images_folder,f"{name}.png"))
        return (name,hist_dict)
    
    def get_discriminator_histograms(self,images_folder):
        self.logreg_model.save_model(os.path.join(images_folder,"log_reg_model"))
        def mapping(name):
            return self._draw_discrtiminator(name,images_folder)
        self.histograms = dict(map(mapping , self.signal_names + self.bkg_names))
        
        f = TFile(os.path.join(images_folder,"Logistic_Regresion.root"),"RECREATE")
        for signal in self.histograms:
            h=self.histograms[signal][self.channels[0]]
            h.Write(h.GetName().removesuffix(f"_{self.channels[0]}"))
        return self.histograms
        
    