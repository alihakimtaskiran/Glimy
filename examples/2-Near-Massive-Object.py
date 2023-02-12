import glimy

obj=glimy.geo.SingularCelestial((.3,.2), 1e27)

field=glimy.Continuum((100,100), 1e-2)
field.add(obj)

field.add(glimy.DotSource((50,20), (0,1000), 1, 2.4e9))

field.build()
field.view_metric()

field.Render(250)

field.view_field()
