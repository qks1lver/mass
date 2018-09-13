#!/usr/bin/env python3

# Import
import os
import cobra
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from multiprocessing import Pool

# Classes
class Model:

    def __init__(self, p_model='', verbose=False):

        self.p_model = p_model
        self.verbose = verbose

        self.model = None

    def load(self, p_data=''):

        if p_data:
            self.p_model = p_data

        if not self.p_model:
            raise ValueError('Missing data path, self.p_data={}'.format(self.p_model))

        if self.p_model.endswith('.xml'):
            # Load SBML
            if self.verbose:
                print('Loading SBML: %s ...' % self.p_model)
            self.model = cobra.io.read_sbml_model(self.p_model)
            if self.verbose:
                print('Loaded SBML: %s' % self.p_model)

        else:
            raise ValueError('Cannot identify file type for %s' % self.p_model)

        return

    def analyze(self, fva_fractions=None):

        if not fva_fractions:
            fva_fractions = [1., 0.95]

        if self.verbose:
            print('Performing flux balance analysis (pFBA) ...')
        df = pd.DataFrame({'flux': cobra.flux_analysis.pfba(self.model).x[:10]})

        if self.verbose:
            print('Performing flux variability analysis (FVA) ...')
        with Pool(processes=os.cpu_count()) as pool:
            res = pool.map(self._fva, fva_fractions)
        fva_min, fva_max = zip(*res)
        df['min'] = fva_min
        df['max'] = fva_max

        print(df.head())

        sns.set()
        sns.scatterplot(data=df)
        plt.show()

        return

    def _fva(self, fraction):
        fva = cobra.flux_analysis.flux_variability_analysis(self.model, reaction_list=self.model.reactions[:10], fraction_of_optimum=fraction, loopless=True)
        return fva['minimum'], fva['maximum']
