import sys
from mediapipe_processing import MediapipeProcessing
from euler_json import EulerJson
import os 
from jpgs_to_mp4 import gmp4


def swap_last_two_extensions(filename):
    # 使用os.path.splitext分割文件名和最后一个后缀
    root, last_extension = os.path.splitext(filename)
    
    # 使用os.path.splitext再次分割剩余的部分以获取倒数第二个后缀
    root, second_last_extension = os.path.splitext(root)
    
    # 重新组合文件名
    new_filename = f"{root}{last_extension}{second_last_extension}"
    
    return new_filename

def swap_extensions_in_directory(directory):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # 获取完整的文件路径
            file_path = os.path.join(directory, filename)
            
            # 获取交换后的文件名
            new_filename = swap_last_two_extensions(filename)
            
            # 构建新的文件路径
            new_file_path = os.path.join(directory, new_filename)
            
            # 重命名文件
            os.rename(file_path, new_file_path)
            
def delete_png_files(directory):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and filename.endswith('.png'):
            # 获取完整的文件路径
            file_path = os.path.join(directory, filename)
            
            # 删除PNG文件
            os.remove(file_path)
            

if __name__ == "__main__":

    end_frame = MediapipeProcessing(sys.argv[1]).frames # sys.argv[1] is the original video path
    EulerJson('keypoints_data.json')
    
    os.system("mayapy fkcontroller.py "+sys.argv[2])

    # 渲染输出目录和前缀
    output_directory = "F:\skecapture\jpgs"
    output_prefix = "my_render"

    # 渲染命令
    render_cmd = 'Render -r arnold -x 680 -y 480 -s 1 -e {} -rd "F:\\skecapture\\jpgs" -im "my_render" -of "png" {}'.format(end_frame, sys.argv[2])

    # 执行渲染命令
    os.system(render_cmd)

    swap_extensions_in_directory(output_directory)

    gmp4()

    delete_png_files(output_directory)

    print("all things done")

    
    

    

    

    
    