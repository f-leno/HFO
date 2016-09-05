from cmac import CMAC
import numpy as np
import numpy.random as npr

c = CMAC(1,0.5,0.1)

data = []
for i in range(10):
    t = npr.rand(10) * 4 - 2
    print("t[%d]: %s" % (i,str(t)))
    pts = c.quantize(t)
    print("pts[%d]: %s" % (i,str(pts)))
    pts = c.quantize_alt(t)
    print("pts[%d]: %s" % (i,str(pts)))
    pts = c.quantize_fast(t)
    print("pts[%d]: %s" % (i,str(pts)))
    data.append([t,pts])

labels = [d[1][0] for d in data]

print len(set(labels))
