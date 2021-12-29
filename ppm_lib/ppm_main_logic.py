from ppm_logger import logger as lg
from entity import project as pr
from entity import sequence as seq


projects = pr.Projects()
#proj.add_project("PECUECA", 24, "1920")
project = pr.Project("PECUECA")

sequences = seq.Sequences(project)
sequences.add_sequence("HHH")
sequence = seq.Sequence(project, "AAA")



    
lg.Logger.info(sequence.get_path())


"""
def pprint_dict(module_name, dict):
    for key in dict.keys():
        print (key)       
    

if __name__ == '__main__':

    pprint_dict(__name__, globals())
    
"""