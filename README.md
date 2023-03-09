# Glimy
## FDTD Simulator
<img src="https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/logo.png" width="200"></img>

  The electromagnetic field.. Interacts with our reality and the reason that we continue to live. We can live beter, if we know time evolution of electromagnetic field. 
  Moreover, Glimy can simulate behaviour of light near massive objects(i.e neutron stars, blackholes). It utilizes VSL Theory of **Mach-Einstein-Dicke**.
  Glimy can simulate photonic devices with varying refractive index through time.
<pre>
pip install glimy
</pre>
## Capabilities
-  Electromagnetic waves in dielectric and magnetic materials.
-  Gravitational effect on electromagnetism
-  Anisotropic materials
-  Lossy medium and conductive materials
-  Objects can be inserted and omitted through the time
### ![Strong Gravitational Potential](examples/2-Near-Massive-Object.py)
![](https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/5.png)     ![](https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/6.png)

### ![Waveguide Example](examples/1-Dielectric-Wave-Guide.py):
![](https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/3.png)     ![](https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/4.png)

<hr/>

### ![Anisotropic Medium](https://github.com/alihakimtaskiran/Glimy/blob/main/examples/5-%20Anisotropic%20Medium.py)

<img src="https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/7.png" width="400">    <img src="https://github.com/alihakimtaskiran/Glimy-FDTD/raw/main/src/8.png" width="600">

<hr>

### Tree
<pre>
|----Continuum(object)----|
|                         |---__init__(grid_size,ds)
|                         |---add(arg)
|                         |---export_grid()
|                         |---export_field()
|                         |---build(verbose=1)
|                         |---impose_grid(e,mu,anisotropy=(False,False))
|                         |---view_(field="t",*args,colorbar=True)
|                         |---view_structure(field="e",*args,colorbar=True)
|                         |---view_field(field="E",*args,colorbar=True)
|                         |---Render(time_steps,backend="numpy",observers=None)
|
|
|----DotSource(object)----|
|                         |---__init__(location,presence,amplitude,frequency,phase=0)
|                         |---__repr__()
|                         |---inf()
|
|
| 
|----geo(module)--------|
                        |----SingularCelestial(object)----|
                        |                                 |---__init__(location,mass)
                        |                                 |---export()
                        |                                 |---dimensionality()
                        |                                 |---__repr__()
                        |
                        |
                        |----MassiveCluster(object)-------|
                        |                                 |---__init__(objects,volatile=False)
                        |                                 |---add(arg)
                        |                                 |---content()
                        |                                 |---dimensionality()
                        |                                 |---__repr__()
                        |
                        |
                        |----PointCloud(object)-----------|
                        |                                 |---__init__(points,layer=0,e=1,mu=1,time=None)
                        |
                        |
                        |----Rectangle(PointCloud)--------|
                        |                                 |---__init__(A,B,layer=0,e=1,mu=1,time=None)
                        |
                        |
                        |----RectPrism(PointCloud)--------|
                        |                                 |---__init__(A,B,layer=0,e=1,mu=1,time=None)
                        |
                        |
                        |----Circle(object)---------------|
                        |                                 |---__init__(A,r,layer=0,e=1,mu=1,time=None)
                        |
                        |
                        |----Sphere(object)---------------|
                        |                                 |---__init__(A,r,layer=0,e=1,mu=1,time=None)
                        |
                        |
                        |----Cylinder(object)-------------|
                                                          |---__init__(A,r,h,layer=0,e=1,mu=1,time=None)
          
  </pre>
  
  # Documentation
  <hr/>
  
  ## Continuum(dim,grid_size,ds)
   Creates electromagnetic field with given dimensions and grid size. Grid spacing is introduced with ds.
   - **grid_size** : Defines grid cell count per axis. It may take a tuple or list. It's 2D or 3D.
   - **ds** : Length of a edge of a grid cell. It may take a float or integer. **All units are SI**.

### add(arg)
  Adds either new geometries, celestial objects and sources into the Continuum.
  - **arg** : It adds new objects into the grid. It can take either defined object or list/tuple of them(recursively). It can take tuple, list, set, everything in **geo**(**geo.\***) and **DotSource**. As long as dimensionality of object and Continuum is the same, it is added.
### build(verbose=1)
   Builds the dielectric, magnetic and geometrodynamic structure. 
   - **verbose**: Determines whether info is displayed. If 0, nothing displayed. If 1, render time is displayed.
### export_field()
  Get Electric and Magnetic Field arrays. It returns a tuple (E, H).
### export_grid()
  Get permittivity and permeability arrays. It returns a tuple (e, mu).
### impose_grid(e,mu,anisotropy=(False,False))
  Embed the electromagnetic grid - generated by other sources -. It is useful for fetching electromagnetic material structure from any optimization algorithm and examining it's electromagnetic properties with **glimy**.
  - **e**: Epsilon of each point of the grid. Shape of the array is (Nx, Ny,...) in isotropic media; (3,Nx,Ny,Nz) in anisotopic media.
  - **mu**: Mu of each point of the grid. Shape of the array is (Nx, Ny,...) in isotropic media; (3,Nx,Ny,Nz) in anisotopic media.
### view_structure(field="e",\*args,colorbar=True)
  You can view the grid structure
  - **field** : It takes "e" for permittivity array, "mu" for permeability array and "Z" for impedance of the grid.
  - **\*args** : Only used in 3D. It used specify axis of view. Plane and and index number can be inserted. For example "z", 10 corresponds z=10 plane in the 3D array. "x","y","z" can be inserted. Also "yz", "xz", "xy" are synonym respectively.
  - **colorbar**: If is is set to **True**, colorbar is displayed.
### view_field(field="E",*args,colorbar=True)
  You can get graph of Electric or Magnetic Field.
  - **field** : It takes "E" for electric field, "H" or magnetic field.
  - **\*args** : Only used in 3D. It used specify axis of view. Plane and and index number can be inserted. For example "z", 10 corresponds z=10 plane in the 3D array. "x","y","z" can be inserted. Also "yz", "xz", "xy" are synonym respectively.
  - **colorbar**: If is is set to **True**, colorbar is displayed.
### view_metric(field="t",*args,colorbar=True)
  You can view geometrodynamic curvature due to the massive objects in the grid.
  - **field** : It takes "t" for curvatures in time. No other grids are not compatible yet.
  - **\*args** : Only used in 3D. It used specify axis of view. Plane and and index number can be inserted. For example "z", 10 corresponds z=10 plane in the 3D array. "x","y","z" can be inserted. Also "yz", "xz", "xy" are synonym respectively.
  - **colorbar**: If is is set to **True**, colorbar is displayed.
### Render(time_steps,backend="numpy",observers=None)
   Executes FDTD calculations on a Continuum object.
   - **time_steps** : It is number of time steps that field will evolve. It may take an integer. Lenght of time steps is given by ds/c/(<span>&#8730;</span>dim) ; where ds is grid spacing, c is speed of light and dim is number of dimensions of the grid. All units are SI.
   - **backend** : It sets the backend. Only **numpy** is supported recently. Therefore it is always **numpy**
   - **observers** : Determines whether time dependent logging will be the case. If it is set to <code>None</code>, time dependent observation is not the case. However, it is a tuple or list of points e.g <code>[ (0,0), (2,2) ]</code> then it returns E-field amplitude of each given point. Returned array's order is the same as implicit order of the fed list/tuple.
<hr/> 


  ## DotSource(location,presence,amplitude,frequency,phase=0)
   Creates a point source on a given place on grid, through given time interval with given amplitude, frequency and phase.
   - **location** : It is location of dot source. It may take a list or tuple. 
   - **presence** : It is a tuple or list in the form of:( start, stop ). It defines in which time step dot source emits electromagnetic wave.
   - **amplitude** : Amplitude of the wave. It may take int or float.
   - **frequency** : Frequency of the wave. It may take int or float.
   - **phase** : Phase of the wave. It may take int or float. It is default 0.
  
  ## geo.SingularCelestial(location, mass):
   Creates a point mass.
   - **location** : Sets the location of point mass. Unit is **meters**. It may take tuple, list or np.array. It must bu in form of N-tuple. It may be outside of the grid.
   - **mass** : Stest the mass of the object. Unit is **kg**. It may take float ot int.
  ## geo.MassiveCluster(objects,volatile=False)
  Creates cluster of massive objects. It is used to integrate so many heavy objects.
   - **objects** : **geo.Singular** object or tuple/list/set of them
   - **volatile** : If it is set <code>False</code>, any new object can't be added. If it is <code>True</code>, new objects can be added.
  ### add(arg)
  Adds a new **geo.Singular** object or tuple/list/set of them. If MassiveCluster is volatile, anything can't be added.
  - **arg** : **geo.Singular** object or tuple/list/set of them.
 
  ## geo.PointCloud(points,layer=0,e=1,mu=1,time=None)
  Creates a point cloud object in 2D or 3D. It infills inside the points. It is compatible with convex hull. Draw miscallenious objects(i.e. hexagon,star, hearth) with it. 
  - **points** : Points that defines convex full. It is a list, tuple or array of 2D or 3D points. Coordinates indicates # of cell in the grid. Like [(1,2), (2,3), (3,4)]. I needs at least 3 points in 2D, 4 points in 3D. 
  - **layer** : Priority of the object. It is an integer. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations
  
  
  ## geo.Rectangle(A, B, layer, e=1, mu=1, time=None)
  Creates a rectangle in 2D.
  - **A**: One of non-connected vertex of the Rectangle. It may take an integer. All units are # of grid cells.
  - **B**: One of non-connected vertex of the Rectangle. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations
  
  ## geo.Circle(A,r,layer,e=1,mu=1, time=None)
  Creates a circle in 2D.
  - **A** : Coordinates of center of the Circle. It may take a tuple or list. All units are # of grid cells.
  - **r** : Radius of the circle. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
   - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations

  ## geo.RectPrism(A, B, layer, e=1, mu=1, time=None)
 Creates a rectangular prism in 3D.
  - **A**: One of non-connected vertex of the RectPrism. It may take an integer. All units are # of grid cells.
  - **B**: One of non-connected vertex of the RectPrism. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations
  
  ## geo.Sphere(C,r,layer=0,e=1,mu=1, time=None)
  Creates a sphere in 3D.
  - **C** : Coordinates of center of the Sphere. It may take a tuple or list. All units are # of grid cells.
  - **r** : Radius of the sphere. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations
  
  ## geo.Cylinder(C,r,h,layer=0,e=1,mu=1, time=None)
 Creates a cylinder in 3D. Its planes are **parallel to xy-plane**
  - **C** : Coordinates of center of the Cylinder. It may take a tuple or list. All units are # of grid cells. Height signifies elongation though z axis.
  - **r** : Radius of the Cylinder. It may take an integer. All units are # of grid cells.
  - **h** : Height of the Cylinder. It may take an integer. All units are # of grid cells.
  - **layer** : Priority of the object. It is an integer and maximum can take 1000. The less **layer** value, the more prior the object. It is useful where you want to design object are overlapping like open access cavity dielectric waveguides.
  - **e** : Relative permittivity of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally, for researching Cherenkov Radiation, metamaterials etc.
  - **mu** : Relative permeability of the object. It may take float ot int for isotropic materials, 3×3 array/list/tuple for anisotropic materials. It is not restricted to be less than 1 intentionally.
  - **time** : It determines in which time the object is seen and dissappear. If the object is eternal, <code>time=None</code>; otherwise <code>time=(start, stop)</code>, it is a list/tuple of start and stop durations.
