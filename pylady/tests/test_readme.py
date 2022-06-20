import pytest, inspect
from pathlib import Path
import pylady 

tests_dir = Path(inspect.getfile(pylady)).parent.joinpath("tests")


def test_readme_example():

    import pylady
    from glob import glob
    
    g2 = pylady.Descriptor.G2(n_g2_eta=3, eta_max_g2=1.1)
    g3 = pylady.Descriptor(desc_type=2)
    
    mydb = pylady.Database(weight_per_element=[1.0, 2.0])  
    
    mydb.add(pylady.Collection(name='bulk_300K', 
                                systems=[pylady.System(poscar=str(tests_dir.joinpath("valid.poscar"))), 
                                        pylady.System(poscar=str(tests_dir.joinpath("valid.poscar")))],
                                w_energy = 1.e6, # enforce a value of weight instead of optimizing
                                w_force  = 0,    # do not fit forces
                                test_size=0.33)) # size of the test set

    mydb.add(pylady.Collection(name='some_defect',
                                systems=[pylady.System(poscar=p) for p in glob(str(tests_dir.joinpath("valid.poscar")))],
                                w_energy = [1.e1, 1.e7], # range for fitting weight
                                w_force  = [1.e3, 1.e6], 
                                w_stress = [1.e2, 1.e6])) # efs for 'energy, force, stress' 
    
    # some attributes of the Database
    print(mydb.get_global_number_systems())
    
    # shows the db as a pandas.DataFrame with 1 system per line, and columns: 
    # name, system filename, w_energy_min, w_energy_max, ..., fit_with, weight_per_element 
    print(mydb.as_df())
    
    # save and reload DB
    # mydb.as_df().to_json("mydb.json")
    # df = pylady.Database.from_json("mydb.json").as_df()
    

    for desc in (g2, g3):

        mymodel = pylady.Model(ml_type=-1, descriptor=desc, database=mydb)
    
        # Run milady with -np 4, in a tmp dir and with additional kwargs
        mymodel.fit(n_jobs=4, save_directory="milady_0001/", n_g3_lambda=3, seed=24)
    
        # results are accessible through the Model object.  
        print(mymodel.database.collections["some_defect"].systems[0].descriptors) # access descriptors of first system of the "some_defect" collection
        print(mymodel.design_matrix)