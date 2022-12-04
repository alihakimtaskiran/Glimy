import glimy
import matplotlib.pyplot as plt
a=glimy.Continuum(3, (20,20,20), 1e-2)

a.add(glimy.geo3D.PointCloud(((0,2,0),(17,0,3),(0,20,8),(10,2,5)),0,2,1))
a.view_structure(False,0,0)

a.add_energizer(glimy.DotSource((3,0,5), (0,1000), 5, 2.4e9))

k=glimy.Render(a,150,{(3,4,9),(2,6,4)})#add time dependent measurement
a.view_field(0,1)
plt.imshow(k[-20:])
