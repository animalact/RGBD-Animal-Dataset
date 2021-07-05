import os
import shutil

class CustomDataset():
    def __init__(self):
        self.checklist = []
        self.errors = []


    def loadBagLabel(self, bag_folder):
        """
            bag 폴더 안에 있는 label.txt 파일을 읽어서 행동별 시작 인덱스 리스트를 반환합니다
            return 값 : {행동1 : [21, 56, 23], 행동2 : [45, ...]}
        """
        acts = {}
        try:
            with open(os.path.join(bag_folder, "label.txt"), "r") as f:
                for line in f:
                    info = line.split(" ")
                    if info[0] in ['no', 'check']:
                        return acts
                    act_idx = acts.get(info[0], [])
                    act_idx.append(info[1])
                    acts[info[0]] = act_idx
        except:
            self.errors.append(bag_folder)
            print(bag_folder, " - label.txt is not correct")

        return acts


    def checkList(self, save_folder):
        """
            save_folder에 있는 checklist.txt를 읽고 
            self.checklist에 bag_id를 append합니다
            # bag_id : 210702_145232 의 형식 (날짜_고유번호)
        """
        self.checklist = []
        checklist = []
        checklist_file = os.path.join(save_folder, "checklist.txt")
        if os.path.exists(checklist_file):
            with open(checklist_file, "r") as f:
                for i in f.readlines():
                    checklist.append(i.split("\n")[0])
            self.checklist = checklist
            return checklist
        else:
            with open(checklist_file, "w") as f:
                pass
        return checklist

    def checkDuplicate(self, bag_id):
        """
            bag_id가 self.checklist에 있는지 검사
        """
        dup = False
        if bag_id in self.checklist:
            dup = True

        return dup


    def addBagIdOnCheckList(self,save_folder, bag_id):
        """
        copy를 완료하면 기존의 checklist.txt 파일을 업데이트합니다
        """
        self.checklist.append(bag_id)
        checklist_file = os.path.join(save_folder, "checklist.txt")
        if os.path.exists(checklist_file):
            with open(checklist_file, "a") as f:
                f.write(f"{bag_id}\n")


    def extractBag(self, folder):
        '''
        삭제 예정
        acts -> {sit:[21, 37], walk: [221,232]}
        idxs -> [21, 37]
        Return acts_ext -> {sit:[00021, 00037], walk: [00221, 00232]}
        '''

        acts = self.loadBagLabel(folder)
        acts_ext = {}
        if not acts:
            return acts_ext
            
        for act in acts:
            act_ext = []
            idxs = acts[act]
            for start_idx in idxs:
                filename = str(int(start_idx)).zfill(5)       # 21 -> 00021
                # color_set, depth_set = self.packageFolder(folder, filenames)
                act_ext.append(filename)
            acts_ext[act] = act_ext
        print("-----extract Start Filename-----")
        print(acts_ext)

        return acts_ext

    def createCustomBag(self, from_folder, save_folder, frames=30):
        ''' 
        save_folder should be DatasetFolder
        ex. /User/CustomDataset/
        '''
        self.checkList(save_folder)
        bag_id = from_folder.split("/")[-1]    # ex. 20210702_154436

        if self.checkDuplicate(bag_id):
            print(bag_id, " is already created")
            return

        acts_ext = self.extractBag(from_folder)
        if not acts_ext:
            print("labeling error")
            return

        print("from :", from_folder)
        print("to   :", save_folder)
        for act in acts_ext:
            cur_id = CustomDataset.checkId(save_folder, act)
            
            for start_filename in acts_ext[act]:
                cur_id += 1
                bag_name = f"{act}_{str(cur_id).zfill(6)}_{bag_id}"
                to_folder = os.path.join(save_folder, bag_name)
                print(act, " - ", start_filename)
                # acts_ext[act] -> [00031, 00124,...]
                CustomDataset.createDirectory(to_folder)
                for i in range(frames):
                    filename = str(int(start_filename) + i).zfill(5)
                    CustomDataset.copyFile(from_folder, to_folder, filename)
                print(start_filename, " is copied")
        print("-----Copy Finished-----")
        self.addBagOnCheckList(save_folder, bag_id)


    def createCustomBags(self, from_folder, save_folder):
        id = 0
        for bag in os.listdir(from_folder):
            if "." in bag:
                continue
            id += 1
            bag_file = from_folder+"/"+bag
            self.createCustomBag(bag_file, save_folder)
        print(sorted(self.errors))


    @staticmethod
    def checkId(save_folder, act):
        max_id = 0
        for bag in os.listdir(save_folder):
            if act in bag:
                id = int(bag.split("_")[1])
                if id > max_id:
                    max_id = id
        return max_id            
        

    @staticmethod
    def copyFile(from_folder, save_folder, filename):
        color_path = os.path.join("color", filename + ".jpg")
        depth_path = os.path.join("depth", filename + ".png")

        src_color = os.path.join(from_folder, color_path)
        src_depth = os.path.join(from_folder, depth_path)
        src_info = os.path.join(from_folder, "intrinsic.json")

        dst_color = os.path.join(save_folder, color_path)
        dst_depth = os.path.join(save_folder, depth_path)
        dst_info = os.path.join(save_folder, "intrinsic.json")

        shutil.copyfile(src_color, dst_color)
        shutil.copyfile(src_depth, dst_depth)
        shutil.copyfile(src_info, dst_info)


    @staticmethod
    def createDirectory(save_folder):
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
            os.mkdir(os.path.join(save_folder, "color"))
            os.mkdir(os.path.join(save_folder, "depth"))
            return
        else:
            print("Folder Already Exists")
            raise FileExistsError
        # if not os.path.exists(os.path.join(save_folder, "color")):
        #     os.mkdir(os.path.join(save_folder, "color"))
        # if not os.path.exists(os.path.join(save_folder, "depth")):
        #     os.mkdir(os.path.join(save_folder, "depth"))
        # return


    @staticmethod
    def extractFilename(start_idx):
        """
        삭제 예정
        """
        return str(int(start_idx)).zfill(5)


    @staticmethod
    def extractFilenames(start_idx, frames=30):
        """
        삭제 예정
        """
        print("extract File names")
        filenames = []
        for i in range(frames):
            filename = CustomDataset.extractFilename(start_idx)
            filenames.append(filename)
        return filenames


    @staticmethod
    def joinFolder(folder, name="color"):
        ''' 
        삭제예정
        type = [ 'color', 'depth' ] 
        '''
        if not name in ['color', 'depth']: 
            raise TypeError

        def joinFunc(filename):
            filepath =  os.path.join(folder, name, filename)    # ex. User/Dataset/123/color/00021.jpg
            filename = os.path.join(name, filename)             # ex. color/00021.jpg
            return (filepath, filename)

        return joinFunc


    @staticmethod
    def packageFolder(folder, filenames):
        '''
        삭제 예정 
        copy_fileset -> [(from_file1, file1), (from_file2, file2), ..] 
        '''
        color_copy_set = list(map(CustomDataset.joinFolder(folder, "color"), filenames))
        depth_copy_set = list(map(CustomDataset.joinFolder(folder, "depth"), filenames))
        return color_copy_set, depth_copy_set


from_folder = "/Users/song-yunsang/Desktop/Business/Butler/Dataset/bags"
save_folder = "/Users/song-yunsang/Desktop/Business/Butler/Dataset/CustomDataset"
cd = CustomDataset()
# cd.extractFilename(10)
# cd.copyBag("/Users/song-yunsang/Desktop/Business/Butler/Dataset/bags/20210702_154436", "/Users/song-yunsang/Desktop/Business/Butler/Dataset/CustomDataset/")
cd.createCustomBags(from_folder, save_folder)

