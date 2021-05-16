import xml.etree.ElementTree as ET
from os import getcwd
import glob

classes = ["human"]
voc_txt_dir = "./human_annotation_simulator_ver.txt"
annotation_dir = f'./human/'
xml_annotation_dir = annotation_dir + '*.xml'


def convert_annotation(annotation_voc, train_all_file):
    tree = ET.parse(annotation_voc)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        train_all_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


train_all_file = open(voc_txt_dir, 'w')

# Get annotations_voc list
annotations_voc = glob.glob(xml_annotation_dir)
for annotation_voc in annotations_voc:
    image_id = annotation_voc.split('/')[-1].split('.')[0].split('\\')[1]+'.png'
    print(image_id)
    train_all_file.write(annotation_dir + image_id)
    convert_annotation(annotation_voc, train_all_file)
    train_all_file.write('\n')
train_all_file.close()
