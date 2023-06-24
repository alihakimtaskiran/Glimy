import glimy

conduct=glimy.geo.RectPrism((10,10,10),(100,50,100),e=1,sigma=7000)
grid=glimy.Continuum((100,100,100),5e-8)
grid.add(conduct)
grid.add(glimy.DotSource((50,50,50),[0,1000],1, 5e14))

grid.build(gpu_flag=1)#IMPORTANT: Set gpu_flag=1
grid.view_structure("sigma","z",62)
grid.Render(100,"cupy")#IMPORTant: Set backend "cupy"
grid.view_field('E','z',62)
grid.view_field('J','z',62)
