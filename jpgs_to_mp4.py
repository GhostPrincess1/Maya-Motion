import cv2
import os


def gmp4():
    # 指定输入文件夹和输出文件名
    input_folder = 'jpgs'
    output_video = 'output_video.mp4'

    # 获取输入文件夹中所有的PNG图像文件
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_files.sort()  # 确保按顺序合并帧

    # 获取第一帧图像的尺寸（假设所有图像具有相同的尺寸）
    frame = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, layers = frame.shape

    # 设置视频编码器和输出视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用MP4编码
    video = cv2.VideoWriter(output_video, fourcc, 30, (width, height))  

    # 合并PNG序列帧到视频
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        video.write(frame)

    # 完成后释放资源
    video.release()

    print(f'视频已保存为: {output_video}')

    return output_video
