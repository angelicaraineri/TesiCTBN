from PyCTBN import JsonImporter
from PyCTBN import SamplePath
from PyCTBN import NetworkGraph
from PyCTBN import ParametersEstimator
import glob
import os

class main():
    read_files = glob.glob(os.path.join('./data', "data.json")) #Take all json files in this dir
    #import data
    importer = JsonImporter(read_files[0], 'samples', 'dyn.str', 'variables', 'Time', 'Name')
    importer.import_data(0)
    #Create a SamplePath Obj passing an already filled AbstractImporter object
    s1 = SamplePath(importer)
    #Build The trajectries and the structural infos
    s1.build_trajectories()
    s1.build_structure()
    print(s1.structure.edges)
    print(s1.structure.nodes_values)
    #From The Structure Object build the Graph
    g = NetworkGraph(s1.structure)
    #Select a node you want to estimate the parameters
    node = g.nodes[2]
    print("Node", node)
    #Init the _graph specifically for THIS node
    g.fast_init(node)
    #Use SamplePath and Grpah to create a ParametersEstimator Object
    p1 = ParametersEstimator(s1.trajectories, g)
    #Init the peEst specifically for THIS node
    p1.fast_init(node)
    #Compute the parameters
    sofc1 = p1.compute_parameters_for_node(node)
    #The est CIMS are inside the resultant SetOfCIms Obj
    print(sofc1.actual_cims)