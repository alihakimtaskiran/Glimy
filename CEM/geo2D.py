class Rectangle(object):
    def __init__(self, A,B,layer,e=1, mu=1):
        
        if not isinstance(A, (tuple, list)):
            raise TypeError("A must be a tuple or list")
        if not isinstance(B, (tuple, list)):
            raise TypeError("B must be a tuple or list")
        
        if len(A)!=2:
            raise ValueError("A must be 2D")
            
        if len(B)!=2:
            raise ValueError("B must be 2D")
         
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        for i in B:
            if not i>=0:
                raise ValueError("Coordinates of B must be greater than 0")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float, complex)):
            raise TypeError("e(permittivity) must be a complex, float or int")
        
        if not isinstance(mu, (int, float, complex)):
            raise TypeError("mu(permiablity) must be a complex, float or int")
        
        self.__A=tuple(A)
        self.__B=tuple(B)
        self.__layer=layer
        self.__e=e
        self.__mu=mu
        
    def __repr__(self):
        __="1 "
        for i in self.__A+self.__B:
            __+=str(i)+" "
        __+=f"{self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
        return __

    def t(self):
        return 1


class Circle(object):
    def __init__(self, A, r,layer, e=1, mu=1):
        if not isinstance(A, (tuple, list)):
            raise TypeError("A(center) must be a tuple or list")
            
        if len(A)!=2:
            raise ValueError("A(center) must be 2D")
            
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        if not isinstance(r, (int, float)):
            raise TypeError("r(radius) must be an int")
        
        if not r>=0:
            raise ValueError("r(radius) must be more than 0")
    
        if not layer<=1000:
            raise ValueError("Layer priority must be <=1000")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float, complex)):
            raise TypeError("e(permittivity) must be a complex, float or int")
        
        if not isinstance(mu, (int, float, complex)):
            raise TypeError("mu(permiablity) must be a complex, float or int")
        
        self.__A=tuple(A)
        self.__r=r
        self.__layer=layer
        self.__e=e
        self.__mu=mu
        
    def __repr__(self):
        return f"2 {self.__A[0]} {self.__A[1]} {self.__r} {self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    def t(self):
        return 2