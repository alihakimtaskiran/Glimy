import Glimy as glimy

encoder=glimy.Continuum(2, (20,300), 5e-9)

DBR=[]

for i in range(5):
    DBR.append(glimy.geo2D.Rectangle((0,18*i), (20,18*i+8),0,5))#n=5 d=40 nm
    DBR.append(glimy.geo2D.Rectangle((0,18*i+8), (20,18*i+18),5,40))#n=4 d=50 nm

msg=[
     glimy.geo2D.VRectangle((0,100),(19,150), 50,0, 30),
     glimy.geo2D.VRectangle((0,100),(19,150), 100,0, 2),
     glimy.geo2D.VRectangle((0,100),(19,150), 150,0, 30),
     glimy.geo2D.VRectangle((0,100),(19,150), 200,0, 2)
     ]

encoder.add((DBR,msg))

encoder.add_energizer(glimy.DotSource((10,72), (0,100000), 1, 3.747405725e+14))

encoder.view_structure(False)


glimy.Render(encoder, 1000)
encoder.view_field()
