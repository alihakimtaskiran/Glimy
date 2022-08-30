from numpy import array
class RectPrism(object):
    def __init__(self, A, B, layer=0, e=1, mu=1):
        if not isinstance(A, (tuple, list, array)):
            raise TypeError("A must be a tuple, list or array")

        if not isinstance(B, (tuple, list, array)):
            raise TypeError("B must be a tuple, list or array")

        if len(A)!=3:
            raise ValueError('A is defined in 3D')
    
        if len(B)!=3:
            raise ValueError('B is defined in 3D')

        for i in A:
	        if i<0:
		        raise ValueError("Each component of A must be >=0")
          
        for i in B:
	        if i<0:
		        raise ValueError("Each component of B must be >=0")
          
        if not isinstance(layer, int):
            raise TypeError("# of layer must be an int")
    
        if layer>1000:
            raise ValueError("# of layer must be <=1000")

        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")

        self.__A=A
        self.__B=B
        self.__layer=layer
        self.__e=e
        self.__mu=mu
    
    def __repr__(self):
        __="3 "
        for i in self.__A:
            __+=str(i)+" "
        for i in self.__B:
            __+=str(i)+" "
        return __+f"{self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
        
    def t(self):
        return 3
    
    def isIn(self, point):
        for i in range(3):
            if self.__A[i]<=point[i]<=self.__B[i] or self.__B[i]<=point[i]<=self.__A[i]:
                pass
            else:
                return False
        return True
                

class Sphere(object):
    def __init__(self, C, r, layer=0, e=1, mu=1):
        if not isinstance(C, (tuple, list, array)):
            raise TypeError("C(center) must be a tuple, list or array")
        
        if len(C)!=3:
            raise ValueError('C(center) is defined in 3D')
        for i in C:
	        if i<0:
		        raise ValueError("Each component of C(center) must be >=0")
        if not isinstance(r, (int, float)):
            raise TypeError("r (radius) must be an int or float")
        
        if r<0:
            raise ValueError("r (radius) must be >=0")

        if not isinstance(layer, int):
            raise TypeError("# of layer must be an int")

        if layer>1000:
            raise ValueError("# of layer must be <=1000")

        if not isinstance(e, (int, float, complex)):
            raise TypeError("Permittivity(e) must be an int, float or complex")
        
        if not isinstance(mu, (int, float, complex)):
            raise TypeError("Permeability(mu) must be an int, float or complex")

        self.__C=C
        self.__r=r
        self.__r_2=r**2
        self.__layer=layer
        self.__e=e
        self.__mu=mu

    def __repr__(self):
        return f"4 {self.__C[0]} {self.__C[1]} {self.__C[2]} {self.__r} {self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
        
    def t(self):
        return 4
    
    def isIn(self, point):
        __=0
        for i in range(3):
            __+=(point[i]-self.__C[i])**2
        if self.__r_2>=__:
            return True
        else:
            return False

class Cylinder(object):
    def __init__(self, C, r, h, layer=0, e=1, mu=1):

        if not isinstance(C, (tuple, list, array)):
            raise TypeError("C(center) must be a tuple, list or array")
        
        if len(C)!=3:
            raise ValueError('C(center) is defined in 3D')
        for i in C:
	        if i<0:
		        raise ValueError("Each component of C must be >=0")
        if not isinstance(r, (int, float)):
            raise TypeError("r (radius) must be an int or float")
        
        if r<0:
            raise ValueError("r (radius) must be >=0")
        
        if not isinstance(h, (int, float)):
            raise TypeError("h (height) must be an int or float")

        if h<0:
            raise ValueError("h (height) must be >=0")

        if not isinstance(layer, int):
            raise TypeError("# of layer must be an int")

        if layer>1000:
            raise ValueError("# of layer must be <=1000")

        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")

        self.__C=C
        self.__r=r
        self.__r_2=r**2
        self.__h=h
        self.__layer=layer
        self.__e=e
        self.__mu=mu

    def __repr__(self):
        return f"5 {self.__C[0]} {self.__C[1]} {self.__C[2]} {self.__r} {self.__h} {self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
        
    def t(self):
        return 5
    
    def isIn(self, point):
        __=0
        if self.__C[-1]<=point[-1]<=self.__C[-1]+self.__h:
            for i in range(2):
                __+=(point[i]-self.__C[i])**2
            if self.__r_2>=__:
                return True
            else:
                return False
        else:
            return False
        
