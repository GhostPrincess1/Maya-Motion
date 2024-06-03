import numpy as np
import json 
from scipy.spatial.transform import Rotation as R



class EulerJson:

    def __init__(self,keypoints_data_path):
        
        self.keypoints_data_path = keypoints_data_path

        #self.points_con_relation = [[36,35],[35,37],[37,0],[11,13],[13,15],[15,33],[12,14],[14,16],[16,34],[23,25],[25,27],[24,26],[26,28]]
        self.__points_con_relation = [[36,35],[35,37],[37,0],[11,13,15],[15,33],[12,14,16],[16,34],[23,25,27],[24,26,28]]

        self.euler_data_list = []

        self.creat_euler_json()
        pass

    def creat_euler_json(self):
        reference_coordinate = np.array([1,0,0])
        with open(self.keypoints_data_path, 'r') as json_file:
            pose_data_list = json.load(json_file)
        
        for i in range(len(pose_data_list)):
            current_frame = pose_data_list[i]

            euler_data_frame = []

            for j in range(len(self.__points_con_relation)):
                
                pos1_index = self.__points_con_relation[j][0]
                pos2_index = self.__points_con_relation[j][1]
                pos3_index = None
                if len(self.__points_con_relation[j]) == 3:
                    pos3_index = self.__points_con_relation[j][2]
                
                pos1 = current_frame[pos1_index]
                pos2 = current_frame[pos2_index]
                pos3 = None

                if pos3_index != None:
                    pos3 = current_frame[pos3_index]
                

                if pos3 != None:

                    euler_angle = self.get_euler_angle_by3pos(pos1,pos2,pos3)
                    euler_angle_dict = {'rx':euler_angle[0],'ry':euler_angle[1],'rz':euler_angle[2]}

                    euler_data_frame.append(euler_angle_dict)

                    ry = self.get_vector_angle(pos1,pos2,pos3)
                    euler_angle_dict = {'rx':0,'ry':-ry,'rz':0}

                    euler_data_frame.append(euler_angle_dict)

                    
                    
                    continue

                else:
                    vector = self.get_vector_by_dict(pos1,pos2)
                    euler_angle = self.get_euler_angle(reference_coordinate,vector)
                    euler_angle_dict = {'rx':euler_angle[0],'ry':euler_angle[1],'rz':euler_angle[2]}
                    euler_data_frame.append(euler_angle_dict)
                
            left_ankle_norm = self.get_norm(current_frame[27],current_frame[31],current_frame[29])
            euler_angle = self.get_euler_angle(reference_coordinate,left_ankle_norm)
            euler_angle_dict = {'rx':euler_angle[0],'ry':euler_angle[1],'rz':euler_angle[2]}
            euler_data_frame.append(euler_angle_dict)

            right_ankle_norm = self.get_norm(current_frame[28],current_frame[32],current_frame[30])
            euler_angle = self.get_euler_angle(reference_coordinate,right_ankle_norm)
            euler_angle_dict = {'rx':euler_angle[0],'ry':euler_angle[1],'rz':euler_angle[2]}
            euler_data_frame.append(euler_angle_dict)

            self.euler_data_list.append(euler_data_frame)   

        with open('euler_data.json', 'w') as json_file:
            json.dump(self.euler_data_list, json_file,indent=len(self.euler_data_list[0]))
           


    def get_vector_by_dict(self,dict1,dict2):

        dx = dict2['x']-dict1['x']
        dy = dict2['y']-dict1['y']
        dz = dict2['z']-dict1['z']
        vector = [dx,dy,dz]
        return np.array(vector)

    def get_euler_angle(self,vec1, vec2):

        rotation_matrix = self.rotation_matrix_from_vectors(vec1,vec2)

        return self.rotation_matrix_to_euler(rotation_matrix)
    
    def rotation_matrix_from_vectors(self,vec1, vec2):
        a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

        return rotation_matrix

    def rotation_matrix_to_euler(self,rotation_matrix):
        rotation_object = R.from_matrix(rotation_matrix)
        return rotation_object.as_euler('xyz', degrees=True)
    

    def get_euler_angle_by3pos(self,pos1,pos2,pos3):

        init_normal = np.array([0, 1, 0])
        init_vector = np.array([1, 0, 0])

        p1 = np.array([pos1['x'], pos1['y'], pos1['z']])
        p2 = np.array([pos2['x'], pos2['y'], pos2['z']])
        p3 = np.array([pos3['x'], pos3['y'], pos3['z']])

        target_normal = np.cross(p2 - p1, p3 - p1)
        target_normal = target_normal / np.linalg.norm(target_normal)

        rotation_matrix1 = self.rotation_matrix_from_vectors(init_normal, target_normal)

        rotated_init_vector = rotation_matrix1.dot(init_vector)

        target_vector = p2 - p1
        target_vector = target_vector / np.linalg.norm(target_vector)

        rotation_matrix2 = self.rotation_matrix_from_vectors(rotated_init_vector, target_vector)

        final_rotation_matrix = rotation_matrix2.dot(rotation_matrix1)

        final_euler_angles = self.rotation_matrix_to_euler(final_rotation_matrix)

        final_euler_angles[0] =  180  + final_euler_angles[0]
        return final_euler_angles
    
    def get_norm(self,pos1,pos2,pos3):

        vec1 = self.get_vector_by_dict(pos1,pos2)
        vec2 = self.get_vector_by_dict(pos1,pos3)

        return np.cross(vec1,vec2)

    def get_vector_angle(self,pos1,pos2,pos3):
        vec1 = self.get_vector_by_dict(pos1,pos2)
        vec2 = self.get_vector_by_dict(pos1,pos3)

        # 计算点积
        dot_product = np.dot(vec1, vec2)

        # 计算向量长度（模）
        norm_A = np.linalg.norm(vec1)
        norm_B = np.linalg.norm(vec2)

        # 计算夹角的余弦值
        cos_theta = dot_product / (norm_A * norm_B)

        # 计算夹角（弧度）
        theta = np.arccos(cos_theta)

        # 将弧度转换为度数
        theta_degrees = np.degrees(theta)

        return theta_degrees




if __name__ == "__main__":


    EulerJson('keypoints_data.json')