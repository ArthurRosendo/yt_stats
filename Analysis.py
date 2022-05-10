import numpy
from numpy import ndarray
import scipy.stats


class Analysis:

    @staticmethod
    def listToArray(_x):
        if _x is list:
            return numpy.array(_x)

    @staticmethod
    def correlationCoefficient(_x, _y):
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)

        if _x is ndarray and _y is ndarray:
            return numpy.corrcoef(_x, _y)
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")

    @staticmethod
    def pearsonCoefficient(_x, _y):
        ''' Pearson's R '''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)
        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.pearsonr(_x,_y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")

    @staticmethod
    def spearmanCoefficient(_x, _y):
        ''' Spearman's Rho'''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)

        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.spearmanr(_x, _y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")

    @staticmethod
    def kendallCoefficient(_x, _y):
        ''' Kendall's Tau'''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)
        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.kendalltau(_x, _y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")
