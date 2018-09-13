#!/usr/bin/env python3

import argparse
import os
from src.core import Model

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Mass', description='Automate metabolic engineering')
    parser.add_argument('-m', dest='model', help='Model file')
    parser.add_argument('-v', dest='verbose', action='store_true', help='To verbose')

    args = parser.parse_args()

    if args.model:

        if not os.path.isfile(args.model):
            raise ValueError('Invalid model file path: %s' % args.model)

        m = Model(p_model=args.model, verbose=args.verbose)
        m.load()
        m.analyze()
