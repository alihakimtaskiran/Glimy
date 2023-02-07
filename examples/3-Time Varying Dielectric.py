import glimy

encoder=glimy.Continuum((20,300), 5e-9)

DBR=[]

for i in range(5):
    DBR.append(glimy.geo.Rectangle((0,18*i), (20,18*i+8),0,5))#n=5 d=40 nm
    DBR.append(glimy.geo.Rectangle((0,18*i+8), (20,18*i+18),5,40))#n=4 d=50 nm

msg=[
     glimy.geo.Rectangle((0,100),(19,150),0, 30,time=(50,10000000)),
     glimy.geo.Rectangle((0,100),(19,150),0, 2,time=(100,100000002)),
     glimy.geo.Rectangle((0,100),(19,150),0, 30,time=(150,100000003)),
     glimy.geo.Rectangle((0,100),(19,150),0, 2,time=(200,100000004))
     ]

encoder.add((DBR,msg))

encoder.add(glimy.DotSource((10,72), (0,100000), 1, 3.747405725e+14))

encoder.build()

encoder.view_structure()


encoder.Render(1000)
encoder.view_field()
