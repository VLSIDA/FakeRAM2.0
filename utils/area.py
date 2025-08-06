import os
import sys
import math 

def get_macro_dimensions(process, sram_data, num_rports, num_wports, num_rwports, is_both_sides):
  R_SCALING = W_SCALING = 1
  RW_SCALING = 1
  X_ASYMMETRIC_SRAM_SCALING = 1
  Y_ASYMMETRIC_SRAM_SCALING = 1/4 # Adjusts to number of pins anyways

  # DYNAMIC SIZING
  if is_both_sides:
    xfactor = ((num_rports + num_wports) * R_SCALING + num_rwports * RW_SCALING) * X_ASYMMETRIC_SRAM_SCALING
    yfactor = ((num_rports + num_wports) * 1 + num_rwports * RW_SCALING) * Y_ASYMMETRIC_SRAM_SCALING
  else:
    xfactor = (num_rports + num_wports) * R_SCALING + num_rwports * RW_SCALING
    yfactor = (num_rports + num_wports) * 1 + num_rwports * RW_SCALING

  contacted_poly_pitch_um = process.contacted_poly_pitch_nm / 1000
  column_mux_factor       = process.column_mux_factor
  fin_pitch_um            = process.fin_pitch_nm / 1000
  width_in_bits           = int(sram_data['width'])
  depth                   = int(sram_data['depth'])
  num_banks               = int(sram_data['banks'])

  # Corresponds to the recommended 122 cell in asap7
  bitcell_height = 10 * fin_pitch_um
  bitcell_width = 2 * contacted_poly_pitch_um

  all_bitcell_height =  bitcell_height * depth
  all_bitcell_width =  bitcell_width * width_in_bits

  if num_banks == 2 or num_banks == 4:
    all_bitcell_height = all_bitcell_height / num_banks
    all_bitcell_width = all_bitcell_width * num_banks
  elif num_banks != 1:
    raise Exception("Unsupported number of banks: {}".format(num_banks))

  all_bitcell_height = all_bitcell_height / column_mux_factor
  all_bitcell_width = all_bitcell_width * column_mux_factor

  total_height = all_bitcell_height * 1.2
  total_width = all_bitcell_width * 1.2

  # total_area = (total_height * total_width) * bitcell_area_factor
  # aspect_ratio = total_width / total_height
  # final_height = math.sqrt(total_area / aspect_ratio)
  # final_width = total_area / final_height

  # return math.ceil(final_height), math.ceil(final_width)

  return total_height * yfactor, total_width * xfactor