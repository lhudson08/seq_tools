#!/usr/bin/env python

"""
fasta_rename: rename sequences in a fasta file (fuzzy matches allowed)

Usage:
  fasta_rename [options] <fasta_file> <mapping_file>
  fasta_rename -h | --help
  fasta_rename --version

Options:
  <fasta_file>     Fasta file.
  <mapping_file>   Mapping file (old_name<tab>new_name).
  --quiet          Limit warnings. 
  --version        Show version.
  --debug          Debug mode (no parallel processing).
  -h --help        Show this screen.

Description:
  Re-name a fasta file using a mapping file (old_name -> new_name).

  If there is no exact match between a sequence name and a name in
  the 'old_name' column, then fuzzy matching is used (a warning will
  be given with the fuzzy match score).

  Output written to STDOUT.
"""

from docopt import docopt
import sys,os
from functools import partial
import pyfasta
import pandas as pd
from fuzzywuzzy import process


def load_mapping(inFile):
    maps = {}
    with open(inFile, 'rb') as inFH:
        for x in inFH:
            y = x.rstrip().split('\t')
            msg = 'Mapping file must have 2 columns!'
            assert len(y) >= 2, msg
            maps[y[0]] = y[1]
    return maps


def main(uargs):
    # load
    fasta = pyfasta.Fasta(uargs['<fasta_file>'])
    maps = load_mapping(uargs['<mapping_file>'])

    # rename
    msg = 'Fuzzy match: "{}" <-> "{}" (score: {})\n'
    for name in fasta.keys():
        try:
            new_name = maps[name]
        except KeyError:
            (m,score) = process.extractOne(name, maps.keys())
            if not uargs['--quiet']:
                sys.stderr.write(msg.format(name, m, score))
            new_name = maps[m]

        print '>{}\n{}'.format(new_name, fasta[name])
    

if __name__ == '__main__':
    uargs = docopt(__doc__, version='0.1')
    main(uargs)

