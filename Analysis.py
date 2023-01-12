import numpy
from numpy import ndarray
import scipy.stats


class Analysis:

    @staticmethod
    def listToArray(_x: list):
        ''' list to numpy array '''
        if _x is list:
            return numpy.array(_x)

    @staticmethod
    def pearsonCoefficient(_x:list, _y:list):
        ''' Pearson's R '''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)
        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.pearsonr(_x,_y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")

    @staticmethod
    def spearmanCoefficient(_x:list, _y:list):
        ''' Spearman's Rho'''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)

        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.spearmanr(_x, _y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")

    @staticmethod
    def kendallCoefficient(_x:list, _y:list):
        ''' Kendall's Tau'''
        _x = Analysis.listToArray(_x)
        _y = Analysis.listToArray(_y)
        if _x is ndarray and _y is ndarray:
            coef, p = scipy.stats.kendalltau(_x, _y)
            return coef
        else:
            raise Exception("Invalid argument(s) type for correlationCoefficient() of Analysis class")
