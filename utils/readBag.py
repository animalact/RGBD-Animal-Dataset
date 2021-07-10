import open3d as o3d

bag_filename = "./20210706_172335.bag"

def readBag(bag_filename):
    bag_color_info = []
    bag_depth_info = []
    bag_reader = o3d.t.io.RSBagReader()
    bag_reader.open(bag_filename)
    im_rgbd = bag_reader.next_frame()

    bag_color_info.append(im_rgbd.color)
    bag_depth_info.append(im_rgbd.depth)

    # check all frame till end
    while not bag_reader.is_eof():
        im_rgbd = bag_reader.next_frame()
        bag_color_info.append(im_rgbd.color)
        bag_depth_info.append(im_rgbd.depth)

    bag_reader.close()

    return bag_color_info, bag_depth_info