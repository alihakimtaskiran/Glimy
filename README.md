# Glimy
## FDTD Simulator
  The electromagnetic field.. Interacts with our reality and the reason that we continue to live. We can live beter, if we know time evolution of electromagnetic field. 


<pre>
  
|----Continuum(object)----|
|                         |---__init__(dim,grid_size,ds,ANC=False)
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
