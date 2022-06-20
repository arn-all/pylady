# PyLaDy

## Usage


```py
  import pylady as pl
  from glob import glob
```

**Descriptor selection**

```py
  g2 = pl.descriptors.G2(n_g2_eta=3, eta_max_g2=1.1)
  g3 = pl.descriptors.Descriptor(desc_type=2)
```

**Database definition**

- Each atomic configuration is stored in a `pl.System` object
- Related `pl.System` objects are gathered in `pl.Collection`
- The `pl.Database` gathers a set of `Collection` objects.

```py
  mydb = pl.Database(weight_per_element=[1.0, 2.0])  
  
  mydb.add(pl.Collection(name='bulk_300K', 
                             systems=[pl.System(poscar="bulk_300K_01.poscar"), 
                                      pl.System(poscar="bulk_300K_02.poscar")],
                             w_energy = 1.e6, # enforce a value of weight instead of optimizing
                             w_force  = 0,    # do not fit forces
                             test_size=0.33)) # size of the test set

  mydb.add(pl.Collection(name='some_defect',
                             systems=[pl.System(poscar=p) for p in glob("some/pattern.poscar")],
                             w_energy = [1.e1, 1.e7], # range for fitting weight
                             w_force  = [1.e3, 1.e6], 
                             w_stress = [1.e2, 1.e6])) # efs for 'energy, force, stress' 
 
  # shows the db as a pandas.DataFrame with 1 system per line, and columns: 
  # name, system filename, w_energy_min, w_energy_max, ..., fit_with, weight_per_element 
  print(mydb.as_df())
  
  # save and reload DB
  mydb.as_df().to_json("mydb.json")
  df = pylady.Database.from_json("mydb.json").as_df()
```

**Model training**
```py
  for desc in (g2, g3):

    mymodel = pl.Model(ml_type=-1, descriptor=desc, database=mydb)
  
    # Run milady with -np 4, in a tmp dir and with additional kwargs
    mymodel.fit(njobs=4, save_directory="milady/run_01", n_g3_lambda=3, seed=24)
  
    # results are accessible through the Model object.  
    # To access descriptors of first system of the "some_defect" collection :
    print(mymodel.db["some_defect"][0].descriptors) 
    print(mymodel.design_matrix)
```

## Tools

**Available as CLI & python funcs**

- Configure the path to Milady binary in `~/.config/milady_config.json`

  ```sh
  pylady create-config
  ```
  ```py
  pylady.cli.create_config(set_env_cmd, run_milady_cmd, force, location)
  ```

- Check a valid path to Milady binary is set in `~/.config/milady_config.json` and the file is accessible

  ```sh
  pylady check-config
  ```
  ```py
  pylady.cli.check_config()
  ```

- Plot train/test accuracy:

  ```bash
  pylady plot -db_in_file db_model.in --test "test_*.out" --train "train*.out" --save "graph.pdf"

  pylady plot --db db.json --fit_data fit.h5 --save "graph.pdf"
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

## CI/CD

- Tested on python `3.6` to `3.9`

