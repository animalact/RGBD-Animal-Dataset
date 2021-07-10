import argparse

from lib import BagConverter

def main():
    converter = BagConverter()
    if args.check:
        print("start check bags")
        converter.loadBags(args.check)
        return

    if args.folder:
        print("start convert All bags")
        converter.convertAll(args.folder)
        return

    if args.input:
        print(f"start convert {args.input}")
        converter.convertBagToImage(args.input)
        return

    print("something wrong!")
    raise InterruptedError




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read recorded bag file and save depth and color png file.")
    # Add argument which takes path to a bag file as an input
    parser.add_argument("-c", "--check", type=str, help="Path to the folder contained bag files to check bags exists")
    parser.add_argument("-f", "--folder", type=str, help="Path to the folder contained bag files")
    parser.add_argument("-i", "--input", type=str, help="Convert a bag file to color and depth image")

    # Parse the command line arguments to an object
    args = parser.parse_args()

    main()