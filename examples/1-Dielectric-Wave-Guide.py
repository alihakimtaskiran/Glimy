import glimy
field=glimy.Continuum((100,100), 10e-9)

a=glimy.geo.Rectangle((0,0), (99,99), 100,1)

field.add(a)

for i in range(10):
    for j in range(4):
        field.add(glimy.geo.Circle((4+10*i,4+10*j), r=3, layer=8, e=10))
    for j in range(5,10):
        field.add(glimy.geo.Circle((4+10*i,4+10*j), r=3, layer=8, e=10))


field.add(glimy.DotSource((45,45), (0,100), 1, glimy.c/(120e-9)))
field.build()
field.view_structure()

field.Render(100)

field.view_field()
