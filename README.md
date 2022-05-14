# pylady

## Usage


```py
  import pylady
  import ase
  
  # Choose a descriptor
  g2 = pylady.descriptors.G2(n_g2_eta=3, eta_max_g2=1.1)
  
  # create some dummy ase systems
  ase_system1 = ase.Atoms([Atom('N', (0, 0, 0)), Atom('C', (0, 0, 1))])
  ase_system2 = ase.Atoms([Atom('N', (0, 0, 0)), Atom('O', (0, 0, 1))])

  # Systems can be passed as ase.atoms objects or .poscar file paths
  # each category is a list of pylady Systems
  categories = [[pylady.System(ase_atoms=ase_system1, weight_per_element=[1.0, 2.0]), 
                 pylady.System(ase_atoms=ase_system2)]  # using equal weight if not specified
                [pylady.System(poscar='file.poscar')]] 
  
  mydb = pylady.Database(categories, 
                         w_energy_range = [[1.e2, 1.e6],[1.e2, 1.e6]], # for each category
                         w_force_range  = [[1.e2, 1.e6],[1.e2, 1.e6]],
                         w_stress_range = [[1.e2, 1.e6],[1.e2, 1.e6]],
                         fit=['sfe', 'efs']) 
                         # whether to fit stress, force and energy or only a subset (eg. 'e', 'se'). Insensitive to order.
 
  # Put everything together
  mymodel = pylady.Model(ml_type=-1, descriptor=g2, database=mydb)
  
  # Run milady with -np 4  
  mymodel.run(njobs=4, dir="/tmp/milady_0001/")
  
  # results are accessible through the Model object.  
  print(mymodel.db.systems[2][0].descriptors) # access descriptors of first system of 2nd category
  
```
