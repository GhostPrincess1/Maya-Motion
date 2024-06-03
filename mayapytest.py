from maya import cmds
from maya import standalone
standalone.initialize()
print("-----------------")

cube = cmds.polyCube()


cmds.setAttr(cube[0] + ".translateX", 5)
cmds.setAttr(cube[0] + ".translateY", 3)
cmds.setAttr(cube[0] + ".translateZ", 2)


out_file = r"/Users/liuwei/skecapture/test.ma"


cmds.file(rename = out_file)

cmds.file( f=True, type='mayaAscii', save=True )

standalone.uninitialize()
