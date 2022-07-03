import CEM
field=CEM.Continuum(2, (100,100), 10e-9)

a=CEM.geo2D.Rectangle((0,0), (99,99), 100,4)
field.add(a)

for i in range(10):
    for j in range(10):
        field.add(CEM.geo2D.Circle((4+10*i,4+10*j), r=3, layer=8, e=1))


field.add_energizer(CEM.DotSource((50,50), (0,100), 1, CEM.c/(500e-9)))
field.view_structure(False)

CEM.Render(field, 100)

field.view_field()
