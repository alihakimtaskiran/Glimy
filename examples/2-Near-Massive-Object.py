import glimy

obj=glimy.curved.SingularCelestial((2,4), 1e27)

field=glimy.Continuum(2,(100,100), 1e-2)
field.set_curve(True)
field.add(obj)

field.view_structure(False)
field.add_energizer(glimy.DotSource((10,10), (0,1000), 1, 2.4e9))
glimy.Render(field,500)

field.view_field()
