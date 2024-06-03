def arold(endframe):
    # 创建一个Arnold Skydome Light
    skydome_light = cmds.shadingNode('aiSkyDomeLight', asLight=True)
    cmds.rename(skydome_light, "mySkyDomeLight")

    
    # 设置渲染器为arnold
    #cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
    

    # 设置输出格式为png
    cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")

    #script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 设置渲染范围为1到100帧
    cmds.setAttr("defaultRenderGlobals.startFrame", 1)
    cmds.setAttr("defaultRenderGlobals.endFrame", endframe)

    # 设置渲染分辨率为1920x1080
    width = 960
    height = 540

    # 循环渲染每一帧
    for frame in range(1, 300):
        # 设置当前时间为帧号
        cmds.currentTime(frame)
        # 调用arnold渲染函数，第三个参数为是否显示进度条，第四个参数为是否保存图片，第五个参数为相机名称，第六个参数为额外的选项
        # 设置输出文件名为frame_#.png，其中#是帧号
        cmds.setAttr("defaultArnoldDriver.pre", "F:\\skecapture\\jpgs\\frame_"+str(frame), type="string")
        arnold.arnoldRender(width, height, True, True, "persp", "-layer masterLayer -rl -ai:lcache 4096 -autotx")
        
