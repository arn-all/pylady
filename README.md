# PyLaDy

## Usage


```py
  import pylady
  from glob import glob
  
  g2 = pylady.descriptors.G2(n_g2_eta=3, eta_max_g2=1.1)
  g3 = pylady.descriptors.Descriptor(type=2)
  
  mydb = pylady.Database()  
  
  mydb.add(pylady.Collection(name='bulk_300K', 
                             systems=[pylady.System(poscar="bulk_300K_01.poscar", weight_per_element=[1.0, 2.0]), 
                                      pylady.System(poscar="bulk_300K_02.poscar")],
                             w_energy = 1.e6, # enforce a value of weight instead of optimizing
                             w_force  = 1.e6,
                             test_size=0.33,
                             fit_forces=False,
                             fit_energies=True)) # defaults to True 
                                  
  mydb.add(pylady.Collection(name='some_defect',
                             systems=[pylady.System(poscar=p) for p in glob("some/pattern.poscar")],
                             w_energy = [1.e1, 1.e7],
                             w_force  = [1.e3, 1.e6], 
                             w_stress = [1.e2, 1.e6],
                             fit_with='efs')) # efs for 'energy, force, stress' 
  
  # some attributes of the Database
  print(mydb.get_global_number_systems())
  mydb["some_defect"].set_w_energy_range([1, 1e8])
  mydb["some_defect"].set_fit_with('e')
 
  # shows the db as a pandas.DataFrame with 1 system per line, and columns: 
  # name, system filename, w_energy_min, w_energy_max, ..., fit_with, weight_per_element 
  print(mydb.as_df())
  
  # save and reload DB
  mydb.as_df().to_json("mydb.json")
  df = pylady.Database(from_json="mydb.json").as_df()
  

  for desc in (g2, g3):

    mymodel = pylady.Model(ml_type=-1, descriptor=desc, database=mydb)
  
    # Run milady with -np 4, in a tmp dir and with additional kwargs
    mymodel.fit(njobs=4, dir="/tmp/milady_0001/", n_g3_lambda=3, seed=24)
  
    # results are accessible through the Model object.  
    print(mymodel.db["some_defect"][0].descriptors) # access descriptors of first system of the "some_defect" collection
    print(mymodel.design_matrix)
  
```

## Tools

**Available as CLI & python funcs**

- Plot train/test accuracy:

  ```bash
  pylady plot -d db_model.in --test "test_*.out" --train "train*.out" --save "graph.pdf"
  ```
  
  ```py
  import pylady.plot
  pylady.plot(dbfile="db_model.in", test_files="test*.out", train_files="train*.out")
  ```


- Save configurations found in MD outcar files matching the glob pattern `"file_*.outcar"`. Only save one configuration every 60 timesteps (default is 0, i.e. only save the first step). Saved files have the name `file_*_{step}.mlposcar`.

  ```bash
  pylady convert --in "file_*.outcar" --out "dir/" --read_every 60  
  ```
  
  ```py
  import pylady.convert
  pylady.convert(in="file_*.outcar", out="dir/", read_every=60)
  ```





