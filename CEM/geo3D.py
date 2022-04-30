"""
3D Geometry processor
"""
import numpy as np
class RecPrism(object):
    def __init__(self, A, B, n):
        if not type(A) in {tuple, list, np.array}:
            raise TypeError("A must an array, tuple or list")
        if not len(A)==3:
            raise ValueError("A must be 3D")
        
        if not type(B) in {tuple, list, np.array}:
            raise TypeError("B must an array, tuple or list")
        if not len(B)==3:
            raise ValueError("B must be 3D")

        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
            
        self.__A=np.array(A)
        self.__B=np.array(B)
        self.__n=n

    def isIn(self, P):
        
        if not type(P) in {tuple , list, np.array}:
            raise TypeError("Point must be an array, tuple or list")
        if not len(P)==3:
            raise ValueError("Point must be 3D")
        
        for i in range(3):
            if not ((self.__A[i]<P[i]<self.__B[i]) ^ (self.__B[i]<P[i]<self.__A[i])):
                return False
        return True

    def __repr__(self):
        return f"RECTPRISM\n{self.__A}\n{self.__B}\n{self.__n.real}\n{self.__n.imag}\n"    
    
class Sphere(object):
    def __init__(self, C, r, n):
        if not type(C) in {tuple, list, np.array}:
            raise TypeError("C(Center) must be an array, tuple or list")
        if not len(C)==3:
            raise ValueError("Center must be 3D")
        if not type(r) in {float, int}:
            raise TypeError("r(radius) must be a number")
            
        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
        self.__C=np.array(C)
        self.__r=float(r)
        self.__n=n
    
    def isIn(self, P):
         if not len(P)==3:
             raise ValueError("Point must be 3D")
         if not type(P) in {tuple , list, np.array}:
             raise TypeError("Point must be an array, tuple or list")
         if np.linalg.norm(np.array(P)-self.__C)<self.__r:
             return True
         else:
             return False
         
    def __repr__(self):
        return f"SPHERE\n{self.__C}\n{self.__r}\n{self.__n.real}\n{self.__n.imag}\n"
        
             
class Cylinder(object):
    def __init__(self, CB, r, h, n):
        if not type(CB) in {tuple, list, np.array}:
            raise TypeError("CB(Center of Base) must be an array, tuple or list")
        if not len(CB)==3:
            raise ValueError("Center of Base must be 3D")
            
        if not type(r) in {float, int}:
            raise TypeError("r(radius) must be a number")
        if not type(h) in {float, int}:
            raise TypeError("h(height) must be a number")
        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
        
        self.__CB=np.array(CB)
        self.__r=float(r)
        self.__h=float(h)
        self.__n=n
    
    def isIn(self, P):
         if not len(P)==3:
             raise ValueError("Point must be 3D")
         if not type(P) in {tuple , list, np.array}:
             raise TypeError("Point must be an array, tuple or list")
        
         if np.linalg.norm(np.array(P[:2])-self.__CB[:2])<self.__r:
             return True
         elif P[2]-self.CB[2]<self.__h:
             return True
         else:
             False
    def __repr__(self):
        return f"CYLINDER\n{self.__CB}\n{np.array((self.__r, self.__h))}\n{self.__n.real}\n{self.__n.imag}\n"
