import glob
import os

from PyCTBN import JsonImporter
from PyCTBN import SamplePath
from PyCTBN import StructureConstraintBasedEstimator


def structure_constraint_based_estimation_example():
    # <read the json files in ./data path>
    read_files = glob.glob(os.path.join('./data', "*.json"))
    # <initialize a JsonImporter object for the first file>
    importer = JsonImporter(file_path=read_files[0], samples_label='samples',
                            structure_label='dyn.str', variables_label='variables',
                            time_key='Time', variables_key='Name')
    # <import the data at index 0 of the outer json array>
    importer.import_data(0)
    # construct a SamplePath Object passing a filled AbstractImporter object
    s1 = SamplePath(importer=importer)
    # build the trajectories
    s1.build_trajectories()
    # build the information about the net
    s1.build_structure()
    # construct a StructureEstimator object passing a correctly build SamplePath object and the
    # independence tests significance, if you have prior knowledge about the net structure create a list of tuples
    # that contains them and pass it as known_edges parameter
    se1 = StructureConstraintBasedEstimator(sample_path=s1, exp_test_alfa=0.1, chi_test_alfa=0.1,
                                            known_edges=[], thumb_threshold=25)
    # call the algorithm to estimate the structure
    se1.estimate_structure()
    # obtain the adjacency matrix of the estimated structure
    print(se1.adjacency_matrix())
    # save the estimated structure  to a json file (remember to specify the path AND the .json extension)....
    completeName =  os.path.join('./results' , "result66.json")
    se1.save_results(completeName)
    # ...or save it also in a graphical model fashion (remember to specify the path AND the .png extension)
    se1.save_plot_estimated_structure_graph(os.path.join('./results' , "result66.png"))

