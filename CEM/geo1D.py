"""
1D Geometry Identifier
"""
import numpy as np
class Line(object):
    def __init__(self, Origin, Pointing, n):
        if not type(Origin) in {tuple, list, np.array}:
            raise TypeError("Origin must an array, tuple or list")
        if not len(Origin)==3:
            raise ValueError("Origin must be 3D")
            
        if not type(Pointing) in {tuple, list, np.array}:
            raise TypeError("Pointing vector must an array, tuple or list")
        if not len(Pointing)==3:
            raise ValueError("Pointing vector must be 3D")
            
        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
            
        self.__Origin=tuple(Origin)
        self.__Pointing=tuple(Pointing)
        self.__n=n
    def __repr__(self):
        return f"LINE\n{self.__Origin}\n{self.__Pointing}\n{self.__n}"

