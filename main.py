# author : zhaojihuai z50010333
import os
import argparse
from tqdm import tqdm
from tools.subdir2rootdir import merge_json, json_list, image_dict, scen, get_scen
from tools import subdir2rootdir
from tools.label2coco import labelme2coco
from tools.split_coco_tran_val import split_train_val, split_dir_train_val
# import glob
import shutil

parser = argparse.ArgumentParser(
        description="labelme annotation to coco data json file."
    )
parser.add_argument(
    "--root_dir", 
    type=str, 
    # default='/home/jovyan/qrcode-single-detection/0718_detection/',
    help="Directory to labelme images and annotation json files."
)
parser.add_argument(
    "--save_path",
    type=str,
    help="Directory to save images and annotation json files."
)

parser.add_argument('--train_ratio', type=float, dest='ratio_train', default='0.9', help='set train dataset ratio')
parser.add_argument('--valid_ratio', type=float,  dest='ratio_valid',default='0.1', help='set valid dataset ratio')
parser.add_argument('--trainJson_name', type=str, default='train/annotations/train.json', help='Where to store COCO training annotations')
parser.add_argument('--validJson_name', type=str, default='val/annotations/val.json', help='Where to store COCO valid annotations')

args = parser.parse_args()


def processing_single_scen(scen, args, train_scen_list, val_scen_list):
    for single_scen in tqdm(scen, desc='Processing single scen'):
        merge_json(single_scen, train_scen_list)

        val_json_list = subdir2rootdir.json_list
        val_dict = subdir2rootdir.image_dict

        subdir2rootdir.json_list = []
        subdir2rootdir.image_dict = dict()
        
        merge_json(single_scen, val_scen_list)
        train_json_list = subdir2rootdir.json_list
        train_dict = subdir2rootdir.image_dict
        
        save_scen_path = single_scen.replace(args.root_dir, args.save_path)
        for mode in ['train', 'val']:
            os.makedirs(os.path.join(save_scen_path, mode, 'images'), exist_ok=True)

        if val_json_list:
            labelme2coco(val_json_list, os.path.join(save_scen_path, 'val' , 'annotations', 'val.json'))
        if train_json_list:
            labelme2coco(train_json_list, os.path.join(save_scen_path, 'train' , 'annotations', 'train.json'))
        
        for dict_mode, mode in tqdm(zip([train_dict, val_dict], ['train', 'val'])):
            
            for key in dict_mode.keys():
                if 'Thumbs' in key:
                    continue
                filename = key
                dir_path = dict_mode[key]
                
                save_dir = dir_path.replace(args.root_dir, args.save_path)
                shutil.copy(os.path.join(dir_path, filename), os.path.join(save_scen_path, mode, 'images', filename))
      

def remove_file(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path,file)) if not os.path.isdir(os.path.join(path,file)) else None

def main(args):
    args.trainJson_name = os.path.join(args.save_path, args.trainJson_name)
    args.validJson_name = os.path.join(args.save_path, args.validJson_name)

    os.mkdir(args.save_path) if not os.path.exists(args.save_path) else None
    print("🚀🚀🚀  get scen...  🚀🚀🚀")
    get_scen(args.root_dir)
    
    print("🚀🚀🚀  split train val...  🚀🚀🚀")
    train_scen_list, val_scen_list = split_dir_train_val(args, scen)
    print("🚀🚀🚀  processing single scen...  🚀🚀🚀")
    processing_single_scen(scen, args, train_scen_list, val_scen_list)


    print("😊😊😊  finish processing!!!  😊😊😊")



if __name__=='__main__':

    main(args)