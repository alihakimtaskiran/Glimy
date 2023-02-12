import glimy
field=glimy.Continuum((200,200), 10e-9)



for i in range(10):
    for j in range(4):
        field.add(glimy.geo.Circle((8+20*i,8+20*j), r=4, layer=8, e=10))
    for j in range(5,10):
        field.add(glimy.geo.Circle((8+20*i,8+20*j), r=4, layer=8, e=10))
        
for i in range(9):
    for j in range(3):
        field.add(glimy.geo.Circle((18+20*i,18+20*j), r=4, layer=9, e=10))
    for j in range(5,9):
        field.add(glimy.geo.Circle((18+20*i,18+20*j), r=4, layer=9, e=10))


field.add(glimy.DotSource((100,90), (0,100000), 1, glimy.c/(300e-9)))
field.build()
field.view_structure()

field.Render(500)

field.view_field()
