import os
import argparse

import open3d as o3d

from utils.createLabel import createEmptyLabel

"""
Caution : depth frame and RGB frame should be same!!
"""

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
        for filename in os.listdir(bag_folder):
            if filename[-3:] == "bag":
                bag_folder = os.path.abspath(bag_folder)
                bag = os.path.join(bag_folder, filename)
                if os.path.exists(bag):
                    self.bags.append(bag)

        # sort self.bags
        self.bags = sorted(self.bags)
        print(self.bags)


    def _getSaveFolder(self, bag_file):
        dir_name = os.path.dirname(bag_file)
        bag_name = os.path.splitext(os.path.basename(bag_file))[0]
        save_folder = os.path.join(dir_name, bag_name)

        return save_folder

    def convert(self, bag_file):
        """
        convert Bag To Image
        create new folder contains color and depth images
        """
        save_folder = self._getSaveFolder(bag_file)
        if os.path.exists(save_folder):
            return

        bag_filename = bag_file
        bag_reader = o3d.t.io.RSBagReader()
        bag_reader.open(bag_filename)
        im_rgbd = bag_reader.next_frame()

        # check all frame till end
        while not bag_reader.is_eof():
            bag_reader.save_frames(save_folder)
            im_rgbd = bag_reader.next_frame()

        bag_reader.close()

        createEmptyLabel(save_folder)

    def convertAll(self, bag_folder):
        self.loadBags(bag_folder)
        if not self.bags:
            print("no bag in folder")
            raise NotImplementedError

        for bagfile in self.bags:
            self.convertBagToImage(bagfile)

