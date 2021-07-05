import os

def getFolderList(root_folder):
    roots = []
    skip = True
    for root, dir, filenames in os.walk(root_folder):
        if skip:
            skip = False
            continue
        if 'depth' in root or 'color' in root:
            continue
        roots.append(root)
    
    return sorted(roots)
