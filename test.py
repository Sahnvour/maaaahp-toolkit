from Aaaah.base.primitives import *

#m = Map.from_file('map.txt')
#to_clipboard(m)

g = Group()
g.add(line(5,0,0,100,100), rectangle(5, Shape.Full, 200,200,100,100))
g.rotate(360, 0, 5, Transform.LoopBack)

m = Map()
m.add(g)

to_clipboard(m)
