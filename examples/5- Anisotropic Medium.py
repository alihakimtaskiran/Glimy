import glimy
field=glimy.Continuum((150,150,150),1e-2)
#Anisotropic Object
e=[[5, 0, 0],
   [0, 1.7, 0],
   [0, 0, 1.5]]
an_obj=glimy.geo.RectPrism((10,10,10),(40,40,40),0,e)
field.add(an_obj)
field.add(glimy.DotSource((30,30,30),[0,1000],1, 2.4e9))
field.build()
field.view_structure('e','z',20)
field.Render(100)
field.view_field('E','z',20)
field.view_field('E','x',20)
