from abc import abstractclassmethod, abstractmethod, ABCMeta

import adjtor
import crossover
import data 
import outlier
import profiler

# define interface class
class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def dataload(self, path):
        pass 

    @abstractmethod
    def removeOutlier(self, datas):
        pass

    @abstractmethod
    def adjtor(self, datas):
        pass 

    @abstractmethod
    def crossover(self, datas):
        pass

    @abstractmethod
    def plot(self, datas):
        pass 

    @abstractmethod
    def profiler(self, datas):
        pass 

class LOLStrategy(Strategy):
    def removeOutlier(self, datas):
        return outlier.kmeans_filter(datas)


class Context:
    _strategy = None 

    def __init__(self, strategy):
        self._strategy = strategy
    
    def process(self, datas):
        self._strategy.removeOutlier(datas)