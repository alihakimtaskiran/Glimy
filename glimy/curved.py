"""
Mach-Einstein-Dicke Law of Gravity Simulator
"""
import numpy as np

class SingularCelestial(object):
    def __init__(self, location, mass):
        if not isinstance(location, (tuple, list, np.array)):
            raise TypeError('Location must be a tuple, list or ndarray')

        if not isinstance(mass, (int, float)):
            raise TypeError('mass must be an int or float')

        self.__export=len(location),np.array(location), mass
        
    @property
    def export(self):
        return self.__export