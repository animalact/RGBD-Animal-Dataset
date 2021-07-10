import argparse

from lib import CustomDataset

def main():
    from_folder = args.input
    save_folder = args.output
    cd = CustomDataset()
    # cd.extractFilename(10)
    cd.createCustomBags(from_folder, save_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create Dataset with rgbd folder and label.txt")
    # Add argument which takes path to a bag file as an input
    # parser.add_argument("-c", "--check", type=str, help="Path to the folder contained bag files to check bags exists")
    parser.add_argument("-i", "--input", type=str, help="Path to the rgbd folder with label.txt")
    parser.add_argument("-o", "--output", type=str, help="Path to the folder ")

    # Parse the command line arguments to an object
    args = parser.parse_args()

    main()