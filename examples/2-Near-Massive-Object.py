import glimy

obj=glimy.geo.SingularCelestial((2,4), 1e27)

field=glimy.Continuum((100,100), 1e-2)
field.add(obj)

field.view_structure()
field.add(glimy.DotSource((10,10), (0,1000), 1, 2.4e9))
field.Render(500)

field.view_field()
