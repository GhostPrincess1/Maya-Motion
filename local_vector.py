import numpy as np

import copy
from scipy.spatial.transform import Rotation as R
# 计算向量的模
def magnitude(vector):
    return np.sqrt(np.sum(np.square(vector)))

# 归一化向量
def normalize(vector):
    return vector / magnitude(vector)
#计算向量旋转矩阵
def from_to_rotation(vec1, vec2):
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    return rotation_matrix


def caculate_local_vector(original_vector,local_coordinate_matrix):

    right = local_coordinate_matrix[0]
    up = local_coordinate_matrix[1]
    forward = local_coordinate_matrix[2]

    new_vector =  np.array([np.dot(original_vector, right)/magnitude(right), np.dot(original_vector, up)/magnitude(up), np.dot(original_vector, forward)/magnitude(forward)])
    return new_vector

def get_local_coordinate_matrix(rotation_matrix,original_coordinate_matrix):
    right = original_coordinate_matrix[0]
    up = original_coordinate_matrix[1]
    forward = original_coordinate_matrix[2]

    new_right = rotation_matrix @ right
    new_up = rotation_matrix @ up
    new_forward = rotation_matrix @ forward

    local_coordinate_matrix = np.array([new_right,new_up,new_forward])

    return local_coordinate_matrix

def get_universal_vector():

    return np.array([0,1,0])


def rotation_matrix_to_euler(rotation_matrix):
    rotation_object = R.from_matrix(rotation_matrix)
    return rotation_object.as_euler('xyz', degrees=True)


def get_root_coordinate_matrix(coordinate_matrix):

    return coordinate_matrix
    


def pos_initialize(pos_list,root_coordinate_matrix):

    for j in range(len(pos_list)):
            #Relative coordinate transformation
            pos = pos_list[j]
            new_pos  =  caculate_local_vector(pos,root_coordinate_matrix)
            pos_list[j] = new_pos
    return pos_list

def rotation_matrix_list(pos_list,root_coordinate_matrix):

    #pos_list eg [np.array([])]

    #Deeply copy the original coordinate points, and use them for coordinate transformation later on
    temp_pos_list = copy.deepcopy(pos_list)

    
    rotation_matrix_list = []
    original_coordinate_matrix = get_root_coordinate_matrix(root_coordinate_matrix)

    temp_pos_list = pos_initialize(temp_pos_list,original_coordinate_matrix)

    joint_vector = get_universal_vector()#[1,0,0]

    for i in range(len(temp_pos_list)-1):

        pos1 = temp_pos_list[i]
        pos2 = temp_pos_list[i+1]

        target_vector = pos2 - pos1
        rotation_matrix = from_to_rotation(joint_vector,target_vector)

        rotation_matrix_list.append(rotation_matrix)

        local_coordinate_matrix = get_local_coordinate_matrix(rotation_matrix,np.array([[1,0,0],[0,1,0],[0,0,1]]))

        for j in range(len(temp_pos_list)):
            #Relative coordinate transformation
            pos = temp_pos_list[j]
            new_pos  =  caculate_local_vector(pos,local_coordinate_matrix)
            temp_pos_list[j] = new_pos

    return rotation_matrix_list

def get_euler_list(rotation_matrix_list):
    euler_angles = [] 
    for item in rotation_matrix_list:
        euler_dict = {}
        euler_angle = rotation_matrix_to_euler(item)
        euler_dict['rx'] = euler_angle[0]
        euler_dict['ry'] = euler_angle[1]
        euler_dict['rz'] = euler_angle[2]
        euler_angles.append(euler_dict)
    
    return euler_angles

if __name__ == "__main__":

    a = np.array([-4.436, 1.385, 5.628])
    b = np.array([-2.768, 2.68, 4.074])
    c = np.array([-1.28,1.554,5.39])
    d = np.array([0.77,2.102,4.043])
    

    rotation_matrix_list = rotation_matrix_list([a,b,c,d],np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
    print(get_euler_list(rotation_matrix_list))




    


