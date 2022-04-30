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
            self.__e1=self.__normalize(np.array(Basis_Vectors[0]))
            self.__e2=self.__normalize(np.array(Basis_Vectors[1]))
        else:
            self.__e1=np.array(Basis_Vectors[0])
            self.__e2=np.array(Basis_Vectors[1])
        self.__Origin=np.array(Origin)
        self.__objects=[]
    def __normalize(self, vec):
        return vec/np.linalg.norm(vec)
    
    def add(self, arg):
        _=type(arg)
        if (_==Rectangle or _==Circle):
            self.__objects.append(arg)
        elif _==list or _==tuple or _==set:
            self.__add_multiple(arg)
        else:
            raise TypeError("Only defined geometries are allowed to be added")
    
    def __add_multiple(self, argv):
        for n in argv:
            self.add(n)
        
    def get_elements(self):
        return self.__objects
    
    def info(self):
        return "PLANE", self.__Origin, (self.__e1, self.__e2)
    
    def mixtape(self):
        __=""
        for element in self.__objects:
            _=element.info()
            if _[0]=="RECTANGLE":
                __+=f"RECTANGLE\n{self.__Origin+_[1][0]*self.__e1+_[1][1]*self.__e2}\n{self.__Origin+_[2][0]*self.__e1+_[2][1]*self.__e2}\n{_[3].real}\n{_[3].imag}\n"#
            elif _[0]=="CIRCLE":
                __+=f"CIRCLE\n{self.__Origin+_[1][0]*self.__e1+_[1][1]*self.__e2}\n{_[2]}\n{_[3].real}\n{_[3].imag}\n"
        return __

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

    def info(self):
        return "RECTANGLE", self.__A, self.__B, self.__n 
        
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
         
    def info(self):
        return "CIRCLE",tuple(self.__C),self.__r,self.__n
