class Line(object):
    def __init__(self, A, B, layer, e=1, mu=1):
        
        if not isinstance(A, (int, float)):
            raise TypeError("A must be a float or int")
        if not isinstance(B, (int, float)):
            raise TypeError("B must be a float or int")

        if not A<=B:
            raise ValueError("A must be less than B") 
        
        if not A>=0:
            raise ValueError("A must be greater than 0") 
            
        if not B>=0:
            raise ValueError("B must be greater than 0")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
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
        return f"0 {self.__A} {self.__B} {self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
    
    
    def t(self):
        return 0
    
    def isIn(self, point):
        if self.__A<=point<=self.__B or self.__B<=point<=self.__A:
            return True
        else:
            return False
    
