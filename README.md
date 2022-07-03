# Glimy
## FDTD Simulator
  The electromagnetic field.. Interacts with our reality and the reason that we continue to live. We can live beter, if we know time evolution of electromagnetic field. 


<pre>
|----Continuum(object)----|
|                         |---__init__(dim,grid_size,ds)
|                         |---add(arg)
|                         |---add_energizer(arg)
|                         |---view_structure(bypass=True,*kwargs)
|                         |---view_field(*kwargs)
|                         |---export_for_renderer()
|                         |---load_from_renderer(E,H)
|                         |---export_E_field()
|
|
|
|---Render(field,n_time_steps)
|
|
|
|----DotSource(object)----|
|                         |---__init__(location,presence,amplitude,frequency,phase=0)
|                         |---__repr__()
|                         |---inf()
|                         
| 
| 
|----geo1D(module)--------|----Line(object)---------|
|                                                   |---__init__(A, B, layer, e=1, mu=1)
|                                                   |---__repr__()
|                                                   |---inf()
|                                                   |---t()
|                                                   |---isIn(point)
| 
| 
|                                                   
|----geo2D(module)--------|----Rectangle(object)----|
|                         |                         |---__init__(A,B,layer,e=1,mu=1)
|                         |                         |---__repr__()
|                         |                         |---inf()
|                         |                         |---t()
|                         |                         |---isIn(point)
|                         |
|                         |
|                         |----Circle(object)-------|
|                                                   |---__init__(A,r,layer,e=1,mu=1)
|                                                   |---__repr__()
|                                                   |---inf()
|                                                   |---t()
|                                                   |---isIn(point)
|
|
|
|----geo3D(module)--------|----RectPrism(object)----|
                          |                         |---__init__(A,B,layer=0,e=1,mu=1)
                          |                         |---__repr__()
                          |                         |---inf()
                          |                         |---t()
                          |                         |---isIn(point)
                          |
                          |
                          |----Sphere(object)-------|
                          |                         |---__init__(C,r,layer=0,e=1,mu=1)
                          |                         |---__repr__()
                          |                         |---inf()
                          |                         |---t()
                          |                         |---isIn(point)
                          |
                          |
                          |----Cylinder(object)-----|
                                                    |---__init__(C,r,h,layer=0,e=1,mu=1)
                                                    |---__repr__()
                                                    |---inf()
                                                    |---t()
                                                    |---isIn(point)
  </pre>
  
  # Documentation
  
  ## Continuum(dim,grid_size,ds)
   Creates electromagnetic field with given dimensions and grid size. Grid spacing is introduced with ds.
   - **dim** : Number of dimensions of the Continuum. It may take 1, 2 or 3.
   - **grid_size** : Deines grid cell count per axis. It may take a tuple orlist. It's lenghts must be the same as # of dimensions.
   - **ds** : Length of a edge of a grid cell. It may take a float or integer. All units are SI.
     
     
  ## Render(field,n_time_steps)
   Executes FDTD calculations on a Continuum object.
   - **field** : It must take Continuum object. It s the field that evolved through time.
   - **n_time_steps** : It is number of time steps that field will evolve. It may take an integer. Lenght of time steps is given by ds/c/(<span>&#8730;</span>dim) ; where ds is grid spacing, c is speed of light and dim is number of dimensions of the grid. All units are SI.
  
  
  ## DotSource(location,presence,amplitude,frequency,phase=0)
   Creates a point source on a given place on grid, through given time interval with given amplitude, frequency and phase.
   - **location** : It is location of dot source. It may take a list or tuple. 
   - **presence** : It is a tuple or list in the form of:( start, stop ). It defines in which time step dot source emits electromagnetic wave.
   - **amplitude** : Amplitude of the wave. It may take int or float.
   - **frequency** : Frequency of the wave. It may take int or float.
   - **phase** : Phase of the wave. It may take int or float. It is default 0.
  
  ## geo1D.Line(A, B, layer, e=1, mu=1)
  Creates a line in 1D.
  - **A**: One of endpoints of the Line. It may take an integer. All units are # of grid cells.
  - **B**: One of endpoints of the Line. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
  ## geo2D.Rectangle(A, B, layer, e=1, mu=1)
  Creates a rectangle in 2D.
  - **A**: One of non-connected vertex of the Rectangle. It may take an integer. All units are # of grid cells.
  - **B**: One of non-connected vertex of the Rectangle. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
  ## geo2D.Circle(A,r,layer,e=1,mu=1)
  Creates a circle in 2D.
  - **A** : Coordinates of center of the Circle. It may take a tuple or list. All units are # of grid cells.
  - **r** : Radius of the circle. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
  ## geo3D.RectPrism(A, B, layer, e=1, mu=1)
 Creates a rectangular prism in 3D.
  - **A**: One of non-connected vertex of the RectPrism. It may take an integer. All units are # of grid cells.
  - **B**: One of non-connected vertex of the RectPrism. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
  ## geo3D.Sphere(C,r,layer=0,e=1,mu=1)
  Creates a sphere in 3D.
  - **C** : Coordinates of center of the Sphere. It may take a tuple or list. All units are # of grid cells.
  - **r** : Radius of the sphere. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
  ## geo3D.Cylinder(C,r,h,layer=0,e=1,mu=1)
 Creates a cylinder in 3D. Its planes are **parallel to xy-plane**
  - **C** : Coordinates of center of the Cylinder. It may take a tuple or list. All units are # of grid cells. Height signifies elongation though z axis.
  - **r** : Radius of the Cylinder. It may take an integer. All units are # of grid cells.
  - **h** : Height of the Cylinder. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int. It is not restricted to be less than 1 intentionally.
  
