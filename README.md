# FakeRAM2.0

FakeRAM2.0 aims to build a fake memory compiler which can be used by Physical Design research teams to get memory models (Liberty, LEF and Verilog) compatible with the PDK of their choice. <br/>

Inputs : configuration file eg. example_input_file.cfg <br/>
Run command : python run.py <example_input_file name> <br/>

### Example CFG
```
  "srams": [ 
    {
     "name": "<name>", 
     "width":<bits>,
     "depth": <depth>,
     "banks": 1,
     "write_mode": "<write_mode>",
     "write_granularity": <bits>,
     "r": [<num_ports>, "<left/right>"],
     "w": [<num_ports>, "<left/right>"],
     "rw": [<num_ports>, "<left/right>"]
    }
  ]
```

Defaults:
- Write mode defaults to write_first
- Ports defaults to left side

Manufacuring grid guide:
asap7     : 1nm
nangate45 : 2.5nm
sky130hd  : 5nm 