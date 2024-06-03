import maya.cmds as cmds 
import json
from maya import standalone
from maya_controller import MayaController
import sys
import os
from arold import arold
class FkController:

    def __init__(self,namespace,control_relation_filepath):

        self.namespace = namespace #namespace's type is string
        self.control_relation_filepath = control_relation_filepath

    def init_fkikblend(self):

        fkik = ['FKIKArm_L','FKIKArm_R','FKIKSpine_M','FKIKLeg_L','FKIKLeg_R']
        attribute_name = "FKIKBlend"

        for item in fkik:

            cmds.setAttr(f"{item}.{attribute_name}", 0)

    def destination_controll(self):

        control_relation_list = self.load_control_relation(self.control_relation_filepath)

        for item in control_relation_list:
            keys_list = list(item.keys())
            key = keys_list[0]
            source_object = key
            target_object = item[key] 

            cmds.orientConstraint(source_object, target_object, maintainOffset=True)[0]

            

    def load_control_relation(self,file_path):

        with open(file_path, 'r') as json_file:
            control_relation_list = json.load(json_file)
        return control_relation_list

    
    def import_fbx_and_hide(self,fbx_file_path):
        cmds.file(fbx_file_path, i=True, type="FBX", ra=True, mergeNamespacesOnClash=False, namespace="")
        
                # 获取导入的FBX节点的名称
        imported_fbx_nodes = cmds.ls(type="FBX")

        # 隐藏导入的FBX节点
        for node in imported_fbx_nodes:
            cmds.setAttr(node + ".visibility", 0)

if __name__ == "__main__":

    standalone.initialize()
    cmds.loadPlugin("fbxmaya")

    fkController = FkController("Faye_rig",r'control_relation.json')

    cmds.file(sys.argv[1],open = True,force = True)
    print("open scene success")

    #init T pose

    cmds.setAttr('FKShoulder_L' + '.rotateY', -40)
    cmds.setAttr('FKShoulder_R' + '.rotateY', -40)
    cmds.setAttr('FKWrist_L' + '.rotateY', -20)
    cmds.setAttr('FKWrist_R' + '.rotateY', -20)

    print("init T pose success")

    fkController.init_fkikblend()

    print("init_fkikblend")

    fkController.import_fbx_and_hide(r"reference.fbx")

    print("import_fbx-and_hide")

    fkController.destination_controll()

    print("destination_controll")

    
    endframe = MayaController(r'euler_data.json',r'centre_pos.json').endframe
    print("关键帧设置")

    # 创建一个Arnold Skydome Light
    skydome_light = cmds.shadingNode('aiSkyDomeLight', asLight=True)
    cmds.rename(skydome_light, "mySkyDomeLight")




    out_file = sys.argv[1]


    cmds.file(rename = out_file)

    cmds.file( f=True, type='mayaAscii', save=True )

    standalone.uninitialize()
        
        
