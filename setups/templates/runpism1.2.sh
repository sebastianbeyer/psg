#!/usr/bin/env bash
## PISM runscript created by psg on {{ timestamp  }}
## git revision: {{ psg_revision }}
##
## {{ exp_name }}
##

#### -list_diagnostics \
####

mpiexec -n {{ n_procs }} --use-hwthread-cpus pismr \
  -i {{ netcdfIn }} \
  -config_override {{ config_override }} \
  -timestep_hit_multiplies 1 \
  -bootstrap {{ bootstrap }} \
{% block output %}
  -o {{ output.base }} \
  -ts_file {{ output.ts_file }} \
  -extra_file {{ output.extra_file }} \
{% endblock %}
