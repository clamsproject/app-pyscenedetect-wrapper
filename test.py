import sys
from scene_detect import SceneDetection

tool = SceneDetection()
a = open(sys.argv[1])
b = a.read()
c = tool.annotate(b)
with open (sys.argv[2], "w") as out:
    out.write(c)
# for i in c.views:
#     a = i.__dict__
#     print (a)
#     c = a.get("contains")
#     bd = a.get("annotations")
#     for d in bd:
#         print (d.__dict__)
