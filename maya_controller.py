import maya.cmds as cmds
from maya import standalone
import json
class MayaController:

    def __init__(self,euler_data_path,centre_pos_path):

        self.euler_data_path = euler_data_path
        self.centre_pos_path = centre_pos_path

        self.points_name = [

            'mixamorig:LeftArm',
            'mixamorig:LeftForeArm',
            'mixamorig:LeftHand',

            'mixamorig:RightArm',
            'mixamorig:RightForeArm',
            'mixamorig:RightHand',

            'mixamorig:LeftUpLeg',
            'mixamorig:LeftLeg',
            'mixamorig:RightUpLeg',
            'mixamorig:RightLeg',

            'mixamorig:Spine',
            'mixamorig:Head'

        ]

        self.__ry_0 = ['mp_bone:left_elbow','mp_bone:right_elbow']

        self.euler_data = self.get_euler_data()
        self.centre_pos = self.get_centre_pos()
        self.delete_all_keyframes()
        self.skeletal_control()

        self.endframe = len(self.euler_data)
    

    def get_euler_data(self):

        with open(self.euler_data_path, 'r') as json_file:
            euler_data = json.load(json_file)
        return euler_data

    def get_centre_pos(self):

        with open(self.centre_pos_path, 'r') as json_file:
            centre_pos = json.load(json_file)
        return centre_pos
        

    def delete_all_keyframes(self):
        all_objects = cmds.ls(type="transform")

        for obj in all_objects:
            keyframes = cmds.keyframe(obj, query=True)
            if keyframes:
                cmds.cutKey(obj, time=(keyframes[0], keyframes[-1]), clear=True)
                print("Deleted all keyframes on:", obj)

        
    def insertframe(self,joint_name,keyframe):
        cmds.setKeyframe(joint_name, attribute='rotateX',time=keyframe)
        cmds.setKeyframe(joint_name, attribute='rotateY',time=keyframe)
        cmds.setKeyframe(joint_name, attribute='rotateZ',time=keyframe)

    
    def skeletal_control(self):

        for frame,euler_data_oneframe in enumerate(self.euler_data):
            keyframe = 2*frame
            x = self.centre_pos[frame]['x']
            z = self.centre_pos[frame]['z']
            
            cmds.setAttr('mixamorig:Hips' + '.translateX', 100*x)
            cmds.setAttr('mixamorig:Hips' + '.translateZ', 100*z)

            cmds.setKeyframe('mixamorig:Hips', attribute='translateX', time=keyframe)
            cmds.setKeyframe('mixamorig:Hips', attribute='translateZ', time=keyframe)
            
            for joint_name, joint_euler_dict in zip(self.points_name, euler_data_oneframe):

                rx = joint_euler_dict['rx']
                ry = joint_euler_dict['ry']
                rz = joint_euler_dict['rz']

                cmds.setAttr(joint_name + '.rotateX', rx)
                cmds.setAttr(joint_name + '.rotateY', ry)
                cmds.setAttr(joint_name + '.rotateZ', rz)

                self.insertframe(joint_name,keyframe)
            

if __name__ == "__main__":


    MayaController('F:\skeCapture\euler_data.json','F:\skecapture\centre_pos.json')