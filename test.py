import sys
import json
from scene_detect import SceneDetection

bd = SceneDetection()
a = open(sys.argv[1])
b = a.read()
c = bd.annotate(b)
for i in c.views:
    a = i.__dict__
    print (a)
    c = a.get("contains")
    bd = a.get("annotations")
    for d in bd:
        print (d.__dict__)
