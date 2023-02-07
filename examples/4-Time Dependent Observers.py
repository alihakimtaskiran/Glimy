import glimy
import matplotlib.pyplot as plt
a=glimy.Continuum((20,20,20), 1e-2)

a.add(glimy.geo.PointCloud(((0,2,0),(17,0,3),(0,20,8),(10,2,5)),0,2,1))

a.add(glimy.DotSource((3,0,5), (0,1000), 5, 2.4e9))

a.build()


a.view_structure("e","z",0)


k=a.Render(1500,"numpy",((3,4,9),(2,6,4)))#add time dependent measurement
a.view_field("E","z",1)
plt.imshow(k[-20:])

