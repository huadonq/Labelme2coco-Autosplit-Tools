import os
import shutil
#  @author : zhaojihuai z50010333
# This file can push all file from anywhere subdir into target rootdir.

json_list = []
image_dict = dict()
scen = []

def search_leaf_file(func):
    def wrapper(path, *args):
        lsdir = os.listdir(path)
        dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
        files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
        if files:
            for f in files:
                func(os.path.join(path, f), *args)
        if dirs:
            for d in dirs:
                wrapper(os.path.join(path, d), *args) 
    return wrapper

@search_leaf_file    
def merge_file(path, save_path, img_format = '.jpg'):

    if 'json' in path:
        json_file_name = path.split('/')[-1]
        shutil.copy(path, os.path.join(save_path, json_file_name))
        img_name = json_file_name.split('.')[0] + img_format
        img_path = path.replace(json_file_name, img_name)
        shutil.copy(img_path, os.path.join(save_path, img_name))

@search_leaf_file    
def merge_json(path, ignore=[]):
    if ignore:
        if os.path.dirname(path) in ignore:
            return
    json_list.append(path) if 'json' in path else None
    image_dict[path.split('/')[-1].split('.')[0]+'.jpg'] = path.replace('/' + path.split('/')[-1], '/') if 'json' in path else None


@search_leaf_file    
def processing_file(path, image_list, root_dir):

    leaf_file = path.split('/')[-1]
    path_list = []
    flag = False
    for sub_dir in path.split('/')[:-1]:
        if sub_dir == root_dir and not flag:
            flag = True
            continue
        if flag:
            path_list.append(sub_dir)
     
    if 'json' not in leaf_file:
        tmp = dict()
        tmp[leaf_file] = mp(path_list)
        image_list.append(tmp)

@search_leaf_file    
def get_scen(path):
    root_dir = os.path.dirname(os.path.dirname(path))
    scen.append(root_dir) if root_dir not in scen else None
    # re_dir = os.path.dirname(root_dir)
    # root_dir.replace(re_dir+'/', '')
    
    # scen_path = os.path.join()

    # scen.append(root_dir) if root_dir not in scen else None

if __name__=='__main__':
    path = '/home/jovyan/qrcode-single-detection/0718_detection'
    save_path = '/home/jovyan/aaaaaaa'
    os.mkdir(save_path) if not os.path.exists(save_path) else None
    merge_json(path)
    print(image_dict)
    