
import maya.cmds as cmds



# 设置渲染输出路径
output_path = "F:\skecapture\jpgs"
cmds.setAttr("defaultRenderGlobals.imageFilePrefix", output_path, type="string")

# 设置分辨率
width = 1920  # 替换为所需的宽度
height = 1080  # 替换为所需的高度
cmds.setAttr("defaultResolution.width", width)
cmds.setAttr("defaultResolution.height", height)

# 设置渲染帧范围
start_frame = 1
end_frame = 200  # 替换为您的序列帧的起始和结束帧数
cmds.setAttr("defaultRenderGlobals.startFrame", start_frame)
cmds.setAttr("defaultRenderGlobals.endFrame", end_frame)

# 使用硬件渲染器进行渲染
cmds.loadPlugin("Mayatomr.mll", quiet=True)  # 加载Mental Ray插件
cmds.setAttr("defaultRenderGlobals.currentRenderer", "mayaHardware2", type="string")  # 设置渲染器为硬件渲染器
cmds.setAttr("defaultRenderGlobals.imageFormat", 8)  # 设置图像格式为JPEG

# 开始渲染
cmds.batchRender()
