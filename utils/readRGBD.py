import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


# http://www.open3d.org/docs/release/python_api/open3d.geometry.RGBDImage.html

sample_color_path = "./sit_000001_20210702_161412/color/00074.jpg"
sample_depth_path = "./sit_000001_20210702_161412/depth/00074.png"

def readRGBD(color_path, depth_path):
    # 파일 읽어오기
    color_raw = o3d.io.read_image(color_path)
    depth_raw = o3d.io.read_image(depth_path)

    # RGBDImage 객체로 만들기
    # convert_rgb_to_intensity = True로 하게되면 (640, 480) 1채널 값이 나오는데 무엇인지 연구중...
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw, convert_rgb_to_intensity=False)

    ### 로우 파일 넘파이로 변경 (잘못된 변경예시) ###
    # color_raw_np = np.array(color_raw)  # (640,480,3)
    # depth_raw_np = np.array(depth_raw)  # (640, 480) (주의, 1000 곱해진 값 나옴 == 미터*1000)

    # RGBD Image에서 Depth 추출
    # rgbd.depth or rgbd.color 프로퍼티 사용
    rgbd_color_np = np.array(rgbd.color)
    rgbd_depth_np = np.array(rgbd.depth) 
    print(rgbd_depth_np.shape)          # (640, 480) (카메라부터의 거리 나옴)

    # RGBD를 하나의 채널로 변경
    print("Create RGBD numpy")
    rgbd_np = np.dstack((rgbd_color_np, rgbd_depth_np))
    print("Shape : ", rgbd_np.shape)    #(640, 480,4)

    plt.subplot(1,2,1)
    plt.imshow(rgbd_depth_np)
    plt.show()

readRGBD(sample_color_path, sample_depth_path)