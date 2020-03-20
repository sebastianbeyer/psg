#!/usr/bin/env bash
## PISM runscript created by psg on {{ timestamp  }}
## git revision: {{ psg_revision }}
##
## {{ exp_name }}
##

#### -list_diagnostics \
####
#### -pdd_sd_file $netcdfIn \
#### -pdd_sd_period 1 \
####
#### -extra_vars velsurf_mag,mask,thk,topg,usurf,climatic_mass_balance,ice_surface_temp,air_temp_snapshot,surface_accumulation_flux,surface_melt_flux,surface_runoff_flux \

mpiexec -n {{ n_procs }} --use-hwthread-cpus pismr \
  -i {{ netcdfIn }} \
  -config_override {{ config_override }} \
  -timestep_hit_multiplies 1 \
  -bootstrap {{ bootstrap }} \
{% block calving %}
  calving eigen_calving,thickness_calving  \
  -thickness_calving_threshold 200 \
{% endblock %}
  -front_retreat_file ./NHEM_ocean_kill_40km.nc \
  -ocean pik \
  -meltfactor_pik 0.01 \
{% block output %}
  -o {{ output.base }} \
  -ts_file {{ output.ts_file }}.nc \
  -extra_file {{ output.extra_file }}.nc \
  -extra_vars {{ output.extra_vars }} \
{% endblock %}
