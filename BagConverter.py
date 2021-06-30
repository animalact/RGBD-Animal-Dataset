import os.path
import argparse

import open3d as o3d

FILE_DIR = os.path.dirname(os.path.abspath(__file__))

class BagConverter:
    def __init__(self):
        self.bags = []

    def loadBags(self, bag_folder=None):

        # this is for test env
        if not bag_folder:
            bag_folder = os.path.join(FILE_DIR, "data_origin")
            print(bag_folder)

        # load bag files from folder
        for root, dir, filenames in os.walk(bag_folder):
            for filename in filenames:
                if filename[-3:] == "bag":
                    bag = os.path.join(root, filename)
                    if os.path.exists(bag):
                        self.bags.append(bag)
        print(self.bags)

    def convertBagToImage(self, bag_file):
        dir_name = os.path.dirname(bag_file)
        folder_name = os.path.splitext(os.path.basename(bag_file))[0]
        save_folder = os.path.join(dir_name, folder_name)

        bag_filename = bag_file
        bag_reader = o3d.t.io.RSBagReader()
        bag_reader.open(bag_filename)
        im_rgbd = bag_reader.next_frame()

        # check all frame till end
        while not bag_reader.is_eof():
            bag_reader.save_frames(save_folder)
            im_rgbd = bag_reader.next_frame()

        bag_reader.close()

    def convertAll(self, bag_folder):
        self.loadBags(bag_folder)
        if not self.bags:
            print("no bag in folder")
            raise NotImplementedError

        for bagfile in self.bags:
            self.convertBagToImage(bagfile)

def main():
    converter = BagConverter()
    
    if args.folder:
        converter.convertAll(args.folder)
        return
    if args.input:
        converter.convertBagToImage(args.input)
        return
    print("something wrong!")
    raise InterruptedError


parser = argparse.ArgumentParser(description="Read recorded bag file and save depth and color png file.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-f", "--folder", type=str, help="Path to the folder contained bag files")
parser.add_argument("-i", "--input", type=str, help="Convert a bag file to color and depth image")

# Parse the command line arguments to an object
args = parser.parse_args()

main()
