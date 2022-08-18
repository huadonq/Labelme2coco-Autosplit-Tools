from subdir2rootdir import merge_json, json_list
import subdir2rootdir
path = '/home/jovyan/qrcode-single-detection/0718_detection'
merge_json(path)
print(len(json_list))


subdir2rootdir.json_list = []
# from subdir2rootdir import json_list
merge_json(path)
print(len(json_list))