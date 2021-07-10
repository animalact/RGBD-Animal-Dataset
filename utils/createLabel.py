import os
from utils.getFolderList import getFolderList

def createEmptyLabel(folder):
    if os.path.exists(folder):
        print("folder exists")
        emptyTxt = os.path.join(folder, "label.txt")
        if os.path.exists(emptyTxt):
            print("file is already exists")
            return
        with open(emptyTxt, "w") as f:
            print("file created")
    else:
        print("cannot find folder")
    return

def generateLabels(root_folder):
    for dir in getFolderList(root_folder):
        createEmptyLabel(dir)
    return

def checkLabels(root_folder):
    act_dict = {}
    for dir in getFolderList(root_folder):

        if dir[-4:] == "done":
            continue

        label = os.path.join(dir, "label.txt")
        with open(label, "r") as f:
            for l in f:
                label_info = l.split(" ")
                act_count = act_dict.get(label_info[0], 0)
                act_count += 1
                act_dict[label_info[0]] = act_count
    print(act_dict)
    return

if __name__ == "__main__":
    checkLabels("/Users/song-yunsang/Desktop/Business/Butler/Dataset/bags")







