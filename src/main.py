#!/usr/bin/env python3

import os
import sys
import argparse

import paths
import spec
import experiment
import expenv
import version

# get location of this stuff and add the paths, so no install is necessary
psg_file = os.path.realpath(os.path.expanduser(__file__))
psg_prefix = os.path.dirname(os.path.dirname(psg_file))

# print(psg_prefix)
spack_src_path = os.path.join(psg_prefix, "src")
sys.path.insert(0, spack_src_path)

# load all the stuff
grids = spec.Spec('grid', paths.gridsfile)
times = spec.Spec('time', paths.timesfile)
icedyns = spec.Spec('icedynamic', paths.icedynfile)
oceans = spec.Spec('ocean', paths.oceansfile)
climates = spec.Spec('climate', paths.climatesfile)
exps = spec.Spec('exp', paths.expsfile)


def listCmd(args):
    if args.type == 'exps':
        exps.print_overview()
    # print(exps)


def rsync_command(args):
    import subprocess
    experiment = args.experiment
    remote = args.remote
    if remote == 'cluster':
        path = '/home/sbeyer'
    else:
        path = '/work/sbeyer'
    source = remote + ":" + path + "/psg/experiments/" + experiment + "/*.nc"
    destination = os.path.join(paths.exp_envs_path, experiment)
    subprocess.call(["rsync", "--progress", "-avzh", source, destination])
    # rsync --progress -avzh k19:/work/sbeyer/psg/experiments/LGM-NHEM-40km-constant-siaEtuning/ts_LGM-NHEM-40km-constant-siaEtuning_sia_e_3.nc .


def generate_command(args):
    # load the fragments from the experiment spec
    exp = exps.get_spec(args.exp)
    time = times.get_spec(exp['time'])
    grid = grids.get_spec(exp['grid'])
    icedyn = icedyns.get_spec(exp['icedynamic'])
    ocean = oceans.get_spec(exp['ocean'])
    climate = climates.get_spec(exp['climate'])

    # assemble
    exp = experiment.Experiment(exp, time, grid, icedyn, ocean, climate)
    print(exp)

    expEnv = expenv.ExperimentEnvironment(exp)
    exp.write_to_file(expEnv.runfile, 'runpism1.2.sh')


parser = argparse.ArgumentParser(description='Generate pism runs')
# parser.add_argument('exp', help='name of the experiment', type=str)

subparsers = parser.add_subparsers()

parser_list = subparsers.add_parser('list')
parser_list.add_argument('type', choices=['exps', 'sub'])
parser_list.set_defaults(func=listCmd)

parser_generate = subparsers.add_parser('generate')
parser_generate.add_argument('exp')
parser_generate.set_defaults(func=generate_command)

parser_rsync = subparsers.add_parser('rsync')
parser_rsync.add_argument('experiment')
parser_rsync.add_argument('--remote',
                          default='k19',
                          choices=['k19', 'cluster'])
parser_rsync.set_defaults(func=rsync_command)

args = parser.parse_args()
args.func(args)
