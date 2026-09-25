import json,os
import pdb, time
from pycocotools.coco import COCO
import shutil

####################################################################################################
source_root = "/root/autodl-tmp/coco"
dest_root = "mini_coco"

# train
# anno_json_file = "annotations/instances_train2017.json"
# imgdatadir = "train2017"

# mini_anno_json_file = "annotations/instances_train2017.json"
# mini_imgs_name = "train2017" 

# #regenerate = True 
# regenerate = False 
# num = 64
# images_list = [391895, 522418, 184613, 318219, 554625, 574769, 60623, 309022, 5802, 222564, 118113, 193271, 224736, 483108, 403013, 374628]
####################################################################################################

# val
anno_json_file = "annotations/instances_val2017.json"
imgdatadir = "val2017"

mini_anno_json_file = "annotations/instances_val2017.json"
mini_imgs_name = "val2017" 

#regenerate = True 
regenerate = False 
num = 64
images_list = [139, 285, 632, 724, 776, 785]
####################################################################################################


def generate_annotations(images_list=images_list):
    with open(os.path.join(source_root, anno_json_file), 'r') as f:  
        coco = json.load(f)

    new_images = []
    new_annotations = []

    # look for images
    for img in coco['images']:
        if img['id'] in images_list:
            new_images.append(img)

    # look for annotations
    for ann in coco['annotations']:
        if ann['image_id'] in images_list:
            new_annotations.append(ann)

    # update and save
    coco['images'] = new_images
    coco['annotations'] = new_annotations

    new_dir_path = os.path.join(dest_root, 'annotations')
    if not os.path.exists(new_dir_path):
        # shutil.rmtree(new_dir_path)
        os.mkdir(new_dir_path)

    print("begin to save")
    with open( os.path.join(dest_root, mini_anno_json_file), 'w') as ff:
        json.dump(coco, ff)


def generate_images(images_list=images_list):
    new_dir_path = os.path.join(dest_root, mini_imgs_name)  

    if not os.path.exists(new_dir_path):
        # shutil.rmtree(new_dir_path)
        os.mkdir(new_dir_path) 

    for img in images_list:
        img_name = format(img, "012") + ".jpg"
        src_file  = os.path.join(source_root, imgdatadir, img_name)
        dest_file = os.path.join(new_dir_path, img_name)
        shutil.copyfile(src_file, dest_file) 
    


if regenerate:
    images_list = [item['id'] for item in coco['images'][:num]]
    print(images_list)

if not os.path.exists(dest_root):
    # shutil.rmtree(dest_root)
    os.mkdir(dest_root)

generate_annotations(images_list)
generate_images(images_list)