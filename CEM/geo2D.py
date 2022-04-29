"""
2D Geometry processor
"""
import numpy as np
class Plane(object):
    def __init__(self, Origin, Basis_Vectors, normalize=True):
        if not type(Origin) in {tuple, list, np.array}:
            raise TypeError("A must an array, tuple or list")

        
        if not type(Basis_Vectors) in {tuple, list,}:
            raise TypeError("Basis_Vectors must  be a tuple or list")
            
        if not len(Basis_Vectors)==2:
            raise ValueError("A plane must have 2 basis vectors")
            
        for i in range(2):
            if not type(Basis_Vectors[i]) in {tuple, list, np.array}:
                raise TypeError("Each basis vector must be an array, tuple or list")

        if not np.dot(Basis_Vectors[0], Basis_Vectors[1])==0:
            raise ValueError("Basis vectors must be orthagonal")
        
        if normalize:
            self.__e1=self.__normalize(Basis_Vectors[0])
            self.__e2=self.__normalize(Basis_Vectors[1])
        else:
            self.__e1=Basis_Vectors[0]
            self.__e2=Basis_Vectors[1]
        
        self.__objects=[]
    def __normalize(self, vec):
        return vec/np.linalg.norm(vec)
    
    def add(self, arg):
        _=type(arg)
        if not (_==Rectangle or _==Circle):
            raise TypeError("Only defined geometries are allowed to be added")
        else:
            self.__objects.append(arg)
            
    def get_elements(self):
        return self.__objects
class Rectangle(object):
    def __init__(self, A, B, n):
        
        if not type(A) in {tuple, list, np.array}:
            raise TypeError("A must an array, tuple or list")
        if not len(A)==2:
            raise ValueError("A must be 2D")
        
        if not type(B) in {tuple, list, np.array}:
            raise TypeError("B must be an array, tuple or list")
        if not len(B)==2:
            raise ValueError("B must be 2D")
        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
        self.__A=np.array(A)
        self.__B=np.array(B)
        self.__n=n
    def __repr__(self):
        return f"RECTANGLE\n{tuple(self.__A)}\n{tuple(self.__B)}\n{self.__n}\n" 
    
    def isIn(self, P):
        if not type(P) in {tuple , list, np.array}:
            raise TypeError("Point must be an array, tuple or list")
        if not len(P)==2:
            raise ValueError("Point must be 2D")
        
        for i in range(2):
            if not ((self.__A[i]<P[i]<self.__B[i]) ^ (self.__B[i]<P[i]<self.__A[i])):
                return False
        return True


class Circle(object):
    def __init__(self, C, r, n):
        if not type(C) in {tuple, list, np.array}:
            raise TypeError("C(Center) must be an array, tuple or list")
        if not len(C)==2:
            raise ValueError("Center must be 2D")
        if not type(r) in {float, int}:
            raise TypeError("r(radius) must be a number")
            
        if not type(n) in {complex, float, int}:
            raise TypeError("Refractive index must be a number")
        self.__C=np.array(C)
        self.__r=float(r)
        self.__n=n
    def isIn(self, P):
         if not len(P)==2:
             raise ValueError("Point must be 2D")
         if not type(P) in {tuple , list, np.array}:
             raise TypeError("Point must be an array, tuple or list")
         if np.linalg.norm(np.array(P)-self.__C)<self.__r:
             return True
         else:
             return False
         
    def __repr__(self):
        return f"CIRCLE\n{tuple(self.__C)}\n{self.__r}\n{self.__n}\n"