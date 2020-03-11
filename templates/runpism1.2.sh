#!/usr/bin/env bash
## PISM runscript created by psg on {{ timestamp  }}
##
## {{ exp_name }}
##

{% block mpi %}
  mpiexec -n {{ n_procs }} --use-hwthread-cpus pismr \
{% endblock %}
{% block general %}
  -i {{ netcdfIn }} \
  -config_override {{ config_override }} \
  -timestep_hit_multiplies 1 \
{% if setup.do_bootstrap %}
  -bootstrap \
{% endif %}
{% endblock %}
{% block grid %}
  -Mx {{ grid.Mx }} -My  {{ grid.My }} \
  -Mz {{ grid.Mz }} -Mbz {{ grid.Mbz }} \
  -Lz {{ grid.Lz }} -Lbz {{ grid.Lbz }} \
  -z_spacing {{ grid.zspacing }} \
  -grid.recompute_longitude_and_latitude {{ grid.recomputeLatLon }} \
  -periodicity {{ grid.periodicity }} \
{% endblock %}
{% block surf_atmo %}
  -temp_lapse_rate 5 \
{% if setup.do_atmGiven %}
  -atmosphere given \
  -atmosphere_given_file {{ atm_given_file }} \
{% endif %}
{% if setup.do_pdd %}
  -surface pdd \
  -surface pdd \
  -surface.pdd.air_temp_all_precip_as_rain 275.15 \
  -surface.pdd.air_temp_all_precip_as_snow 273.15\
  -surface.pdd.factor_ice 0.0088 \
  -surface.pdd.factor_snow 0.0033 \
  -surface.pdd.refreeze 0.6 \
{% endif %}
{% if setup.do_glacialIndex %}
  -atmosphere index \
  -atmosphere.index.precip_decay_rate 0.75 \
  -atmosphere_index_file $glacialIndex \
  -atmosphere_indexindex_file $glacialIndexIndex \
{% endif %}
{% endblock %}
{% block calving %}
  -calving eigen_calving,thickness_calving  \
  -thickness_calving_threshold 200 \
{% endblock %}
{% block ocean %}
  -front_retreat_file ./NHEM_ocean_kill_40km.nc \
{% if setup.do_sealevel %}
  -sea_level constant,delta_sl \
  -ocean_delta_sl_file {{ ocean.sealevelFile }} \
{% endif %}
  -ocean pik \
  -meltfactor_pik 0.01 \
{% endblock %}
{% block iceDynamics %}
  -sia_e {{ iceDynamics.siaE }} \
  -ssa_e {{ iceDynamics.ssaE }} \
  -stress_balance {{ iceDynamics.stressBalance }} \
  -topg_to_phi {{ iceDynamics.topgToPhi }} \
  -pseudo_plastic \
  -pseudo_plastic_q {{ iceDynamics.pseudoPlasticQ }}	\
  -till_effective_fraction_overburden {{ iceDynamics.tillFracOver }} \
  -tauc_slippery_grounding_lines \
  -hydrology_tillwat_max {{ iceDynamics.hydroTillWatMax }} \
{% endblock %}
{% block time %}
  -ys {{ time.ys }} -ye {{ time.ye }} \
  -ts_times {{ time.ts}} \
  -extra_times {{ time.extra }} \
{% endblock %}
{% block output %}
  -o nhem40km_paleo120k_gi.nc \
  -ts_file ts_nhem40km_paleo120k_gi.nc \
  -extra_file ex_nhem40km_paleo120k_gi.nc \
  -extra_vars velsurf_mag,mask,thk,topg,usurf,climatic_mass_balance,ice_surface_temp,air_temp_snapshot,surface_accumulation_flux,surface_melt_flux,surface_runoff_flux \
{% endblock %}


  # -list_diagnostics \
  #
  # -pdd_sd_file $netcdfIn \
  # -pdd_sd_period 1 \
