import os
import re
import csv
import wget
from pathlib import Path
from ROOT import TChain

URL = "https://media.githubusercontent.com/media/cfrc2694/Pheno_BSM/main/SimulationsPaths.csv"

def parent_lib_path():
    name="Pheno_BSM"
    import sys
    return os.path.join(sys.path[0].split(name)[0],name,"SimulationsPaths.csv")
    
DEF_PATHS=parent_lib_path()

class DelphesLoader():
    def __init__(self, name_signal, path=DEF_PATHS):
        
        self.name = name_signal
        
        data = self._read_simulation_path(path)
        
        # verify dictionary path
        try:
            path_to_signal = data[self.name][0] # Path
        except KeyError:
            raise Exception("Error: " + name_signal + " Signal not defined")
        #Cross Section
        self.xs = data[self.name][1]
        
        #get the delphes root outputs
        self.Forest = self._get_forest(path_to_signal)
        
        load=self.name+" imported with\n"
        load+=str(len(self.Forest)) + " trees!"
        load+=path_to_signal+"\n"
        print(load, flush=True)

    def _read_simulation_path(self, path):
        temp=False
        if not (os.path.exists(path)):
            temp=True
            print(f"sim path {path} dont exist", flush=True)
            path = os.path.join(os.getcwd(),DEF_PATHS)
            print(f"Downloading default File in {path}.", flush=True)
            if (os.path.exists(path)): os.remove(path)
            response = wget.download(URL, path)
         
        
        # Reading diccionary path
        data = {}
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if ( len(row)!=0 ):
                    name_signal_dict = row.pop(0)
                    data[name_signal_dict] = [*row]
        if temp :
            os.remove(path)
        return data
    
    def _get_forest(self,path_to_signal):
        def natural_sort(l): 
            convert = lambda text: int(text) if text.isdigit() else text.lower()
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            return sorted(l, key=alphanum_key)
        #Search for all root files in path to signal
        path_root = Path(path_to_signal)
        forest = [root_file.as_posix() for root_file in path_root.glob('**/*.root')]
        forest = natural_sort(forest)
        return forest
    
    
    def get_nevents(self,Forest):
        #get total number of events in Forest
        self.nevents=0
        for i,job in enumerate(Forest):
            tree=TChain("Delphes;1")
            tree.Add(job)
            self.nevents+=tree.GetEntries()
        return self.nevents