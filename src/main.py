#!/usr/bin/env python3

import os
import sys
import argparse

import paths
import spec
import experiment

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
exps = spec.Spec('exp', paths.expsfile)

def listCmd(args):
    print(args)

parser = argparse.ArgumentParser(description='Generate pism runs')
parser.add_argument('exp', help='name of the experiment', type=str)

subparsers = parser.add_subparsers()
parser_list = subparsers.add_parser('list')
parser_list.add_argument('name')
parser_list.set_defaults(func=listCmd)

args = parser.parse_args()
args.func(args)



exp = exps.findSpec(args.exp)
time = times.findSpec(exp['time'])
grid = grids.findSpec(exp['grid'])
icedyn = icedyns.findSpec(exp['icedynamic'])

# assemble
exp = experiment.Experiment(exp, time, grid, icedyn)
