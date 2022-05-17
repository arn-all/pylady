# PyLaDy

## Usage


```py
  import pylady
  import ase
  from glob import glob
  
  # Choose a descriptor
  g2 = pylady.descriptors.G2(n_g2_eta=3, eta_max_g2=1.1)
  g3 = pylady.descriptors.Descriptor(type=2)
  
  # create some dummy ase systems
  ase_system1 = ase.Atoms([Atom('N', (0, 0, 0)), Atom('C', (0, 0, 1))])
  ase_system2 = ase.Atoms([Atom('N', (0, 0, 0)), Atom('O', (0, 0, 1))])

  # Systems can be passed as ase.atoms objects or .poscar file paths

  mydb = pylady.Database()  
  
  mydb.add(pylady.Collection(name='bulk_300K', 
                             systems=[pylady.System(ase_atoms=ase_system1, weight_per_element=[1.0, 2.0]), 
                                      pylady.System(ase_atoms=ase_system2)],
                             w_energy_range = [1.e2, 1.e6],
                             w_force_range  = [1.e2, 1.e6], 
                             fit_with='ef'))
                                  
  mydb.add(pylady.Collection(name='some_defect',
                             systems=[pylady.System(poscar=p) for p in glob("some/pattern.poscar")],
                             w_energy_range = [1.e1, 1.e7],
                             w_force_range  = [1.e3, 1.e6], 
                             w_stress_range = [1.e2, 1.e6],
                             fit_with='efs')) # efs for 'energy, force, stress' 
  
  print(mydb.get_global_number_systems())
  mydb["some_defect"].set_w_energy_range([1, 1e8])
  mydb["some_defect"].set_fit_with('e')
 
  for desc in g2, g3:

    mymodel = pylady.Model(ml_type=-1, descriptor=desc, database=mydb)
  
    # Run milady with -np 4, in a tmp dir and with additional args
    mymodel.fit(njobs=4, dir="/tmp/milady_0001/", args=("n_g3_lambda=3", "seed=24"))
  
    # results are accessible through the Model object.  
    print(mymodel.db["some_defect"][0].descriptors) # access descriptors of first system of the "some_defect" collection
    print(mymodel.design_matrix)
  
```
