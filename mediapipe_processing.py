import sys
import cv2
import mediapipe as mp
import json
from euler_json import EulerJson
import time 
class MediapipeProcessing:
    
    def __init__(self,video_path):

        self.video_path = video_path
        self.frames = 0
        self.creat_point_position_json()
        pass

    def creat_point_position_json(self):

        # 初始化 MediaPipe Pose 模型
        mp_pose = mp.solutions.pose
        #pose = mp_pose.Pose()
        pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, smooth_landmarks=True)

                # 打开视频
        cap = cv2.VideoCapture(self.video_path) 

        # 用于存储关键点数据的列表
        keypoints_data = []

        centre_pos = []

        '''
        # 获取原始视频的帧速率、分辨率和编解码器
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用MP4V编解码器

        out = cv2.VideoWriter(self.target_video_path, fourcc, frame_rate, (width, height))
        '''

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 将图像从 BGR 转换为 RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 运行姿势估计模型
            results = pose.process(frame_rgb)

            if results.pose_world_landmarks:
                # 处理姿势估计结果
                landmarks = []
                for landmark in results.pose_world_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': -landmark.y,
                        'z': -landmark.z,
                        'visibility': landmark.visibility,
                    })

                #添加手掌平均点
                #33
                avg_x = (landmarks[17]['x']+landmarks[19]['x'])/2
                avg_y = (landmarks[17]['y']+landmarks[19]['y'])/2
                avg_z = (landmarks[17]['z']+landmarks[19]['z'])/2
                avg_vis = 1
                landmarks.append({
                        'x': avg_x,
                        'y': avg_y,
                        'z': avg_z,
                        'visibility': avg_vis,
                    })
                #34
                avg_x = (landmarks[18]['x']+landmarks[20]['x'])/2
                avg_y = (landmarks[18]['y']+landmarks[20]['y'])/2
                avg_z = (landmarks[18]['z']+landmarks[20]['z'])/2
                avg_vis = 1
                landmarks.append({
                        'x': avg_x,
                        'y': avg_y,
                        'z': avg_z,
                        'visibility': avg_vis,
                    })
                

                #额外添加两个关节点，胸部和盆骨
                #35
                avg_x = (landmarks[12]['x']+landmarks[11]['x'])/2
                avg_y = (landmarks[12]['y']+landmarks[11]['y'])/2
                avg_z = (landmarks[12]['z']+landmarks[11]['z'])/2
                avg_vis = 1
                landmarks.append({
                        'x': avg_x,
                        'y': avg_y,
                        'z': avg_z,
                        'visibility': avg_vis,
                    })
                #36
                avg_x = (landmarks[24]['x']+landmarks[23]['x'])/2
                avg_y = (landmarks[24]['y']+landmarks[23]['y'])/2
                avg_z = (landmarks[23]['z']+landmarks[23]['z'])/2
                avg_vis = 1
                landmarks.append({
                        'x': avg_x,
                        'y': avg_y,
                        'z': avg_z,
                        'visibility': avg_vis,
                    })
                
                #添加头部平均中心点
                #37
                avg_x = (landmarks[8]['x']+landmarks[0]['x']+landmarks[7]['x'])/3
                avg_y = (landmarks[8]['y']+landmarks[0]['y']+landmarks[7]['y'])/3
                avg_z = (landmarks[8]['z']+landmarks[0]['z']+landmarks[7]['z'])/3
                avg_vis = 1
                landmarks.append({
                        'x': avg_x,
                        'y': avg_y,
                        'z': avg_z,
                        'visibility': avg_vis,
                    })
                

                

                
                
                keypoints_data.append(landmarks)

                # 绘制关节点和连接线
                
                landmarks_relative = []
                for landmark in results.pose_landmarks.landmark:
                    landmarks_relative.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility,
                    })
                
                x_pos  = (landmarks_relative[23]['x']+landmarks_relative[24]['x'])/2
                z_pos = -(landmarks_relative[23]['y']+landmarks_relative[24]['y'])/2

                centre_pos.append({'x':x_pos,'z':z_pos})
                '''
                image_h, image_w, _ = frame.shape
                for connection in mp_pose.POSE_CONNECTIONS:
                    start_idx = connection[0]
                    end_idx = connection[1]
                    if landmarks_relative[start_idx]['visibility'] > 0 and landmarks_relative[end_idx]['visibility'] > 0:
                        start_point = (int(landmarks_relative[start_idx]['x'] * image_w), int(landmarks_relative[start_idx]['y'] * image_h))
                        end_point = (int(landmarks_relative[end_idx]['x'] * image_w), int(landmarks_relative[end_idx]['y'] * image_h))
                        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
                '''
                
            #out.write(frame)
            # 显示图像
            #cv2.imshow('MediaPipe Pose', frame)

            
            '''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            '''
            
        
        # 关闭视频流
        cap.release()
        #out.release()
        cv2.destroyAllWindows()
        print(len(keypoints_data[0]))
        self.frames = len(keypoints_data)


        # 将关键点数据存储到 JSON 文件中
        with open('keypoints_data.json', 'w') as json_file:
            json.dump(keypoints_data, json_file)
        with open('centre_pos.json', 'w') as json_file:
            json.dump(centre_pos, json_file)

        


if __name__ == "__main__":

    MediapipeProcessing("xiaoyang3.mp4")
    