import math
import os
import sys
from pathlib import Path

from utils.area import get_macro_dimensions

################################################################################
# MEMORY CLASS
#
# This class stores the infromation about a specific memory that is being
# generated. This class takes in a process object, the information in one of
# the items in the "sram" list section of the json configuration file, and
# finally runs cacti to generate the rest of the data.
################################################################################

class Memory:

  def __init__( self, process, sram_data , output_dir = None, cacti_dir = None):

    self.process           = process
    self.name              = str(sram_data['name'])
    self.width_in_bits     = int(sram_data['width'])
    self.depth             = int(sram_data['depth'])
    self.num_banks         = int(sram_data['banks'])
    self.cache_type        = str(sram_data['type']) if 'type' in sram_data else 'cache'
    self.write_mode        = str(sram_data['write_mode']) if 'write_mode' in sram_data else 'write_first'

    # Dynamic number ports
    self.r  = int(sram_data['r'][0]) if ('r' in sram_data and isinstance(sram_data['r'], (list, tuple)) and len(sram_data['r']) > 0) else 0
    self.w  = int(sram_data['w'][0]) if ('w' in sram_data and isinstance(sram_data['w'], (list, tuple)) and len(sram_data['w']) > 0) else 0  
    self.rw = int(sram_data['rw'][0]) if ('rw' in sram_data and isinstance(sram_data['rw'], (list, tuple)) and len(sram_data['rw']) > 0) else 0

    self.write_granularity = int(sram_data['write_granularity']) if 'write_granularity' in sram_data else self.width_in_bits
    self.has_write_mask    = True if 'write_granularity' in sram_data else False
    if self.has_write_mask:
        if (self.width_in_bits % self.write_granularity == 0):
            self.wmask = self.width_in_bits // self.write_granularity
            print("Has write mask: True")
            print("Write granularity: ", self.write_granularity)
        else:
            raise Exception(f"Invalid write_granularity: width_in_bits ({self.width_in_bits}) is not divisible by write_granularity ({self.write_granularity}).")
    else:
        self.wmask = 0  # No write mask
  
    # Defatuls to left
    self.r_portside     = str(sram_data['r'][1]) if ('r' in sram_data and isinstance(sram_data['r'], (list, tuple)) and len(sram_data['r']) > 1 and sram_data['r'][1] is not None) else 'left'
    self.w_portside     = str(sram_data['w'][1]) if ('w' in sram_data and isinstance(sram_data['w'], (list, tuple)) and len(sram_data['w']) > 1 and sram_data['w'][1] is not None) else 'left'
    self.rw_portside    = str(sram_data['rw'][1]) if ('rw' in sram_data and isinstance(sram_data['rw'], (list, tuple)) and len(sram_data['rw']) > 1 and sram_data['rw'][1] is not None) else 'left'

    self.is_both_sides = True if (self.r_portside == 'right' or self.w_portside == 'right' or self.rw_portside == 'right') else False
    self.total_ports    = self.r + self.w + self.rw
    if self.total_ports == 0:
      raise Exception("SRAM needs at least one port.")
    else:
       print('Total Ports: ',self.total_ports)
       print('Port R     : ',self.r)
       print('Port W     : ',self.w)
       print('Port RW    : ',self.rw)
       print('Has right port side %s'%self.is_both_sides)
       print('Port sides %s,%s,%s'%(self.r_portside,self.w_portside,self.rw_portside))
       if self.has_write_mask:
        print('Port Wmask : ',self.wmask)
        # print('Wmask side : ',self.wmask_portside)

    self.width_in_bytes = math.ceil((self.width_in_bits / 8.0))
    self.total_size     = self.width_in_bytes * self.depth
    if output_dir: # Output dir was set by command line option
      p = str(Path(output_dir).expanduser().resolve(strict=False))
      self.results_dir = os.sep.join([p, self.name])
    else:
      self.results_dir = os.sep.join([os.getcwd(), 'results', self.name])
    if not os.path.exists( self.results_dir ):
      os.makedirs( self.results_dir )
   
    self.tech_node_nm                = 7 
    self.associativity               = 1  
    
    self.height_um, self.width_um    = get_macro_dimensions(process, sram_data, self.r, self.w, self.rw, self.is_both_sides)
    self.area_um2 		     = self.width_um * self.height_um 
  
    self.tech_node_um = self.tech_node_nm / 1000.0

    # Adjust to snap
    self.width_um = (math.ceil((self.width_um*1000.0)/self.process.snap_width_nm)*self.process.snap_width_nm)/1000.0
    self.height_um = (math.ceil((self.height_um*1000.0)/self.process.snap_height_nm)*self.process.snap_height_nm)/1000.0
    print("Total Bitcell Height is", self.height_um) 
    print("Total Bitcell Width is", self.width_um) 
    
    ## DUMMY (FOR NOW) VALUES FOR LIB CREATION
    self.t_setup_ns = 0.050  ;# arbitrary 50ps setup
    self.t_hold_ns  = 0.050  ;# arbitrary 50ps hold
    self.standby_leakage_per_bank_mW =  0.1289
    self.access_time_ns = 0.2183
    self.pin_dynamic_power_mW = 0.0013449
    self.cap_input_pf = 0.005
    self.cycle_time_ns = 0.2566
    self.fo4_ps = 9.0632
