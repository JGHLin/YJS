
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:07:38 2017
@author: cetc_ic
"""

from __future__ import division
import os
import xml.dom.minidom
import cv2

#root='/home/ygx/cascade-rcnn/data/VOCdevkit_car/VOC2007/'
#ImgPath = root+'JPEGImages'
#AnnoPath = root+'Annotations'
#ProcessedPath = root+'gt_show'

#处理后的图片位置
ImgPath = 'crop/crop_imgs'
#处理后的xml位置
AnnoPath = 'crop/crop_xmls'
#描框后结果存放位置
ProcessedPath = 'crop/crop_result'


if not os.path.exists(ProcessedPath):
    os.makedirs(ProcessedPath)

label_list = os.listdir(AnnoPath)

num = 0

for labelfile in label_list:
    xmlfile = os.path.join(AnnoPath,labelfile)
    imgfile = os.path.join(ImgPath,'%s.jpg' % labelfile[:-4])

    DomTree = xml.dom.minidom.parse(xmlfile)
    annotation = DomTree.documentElement

    #    filenamelist = annotation.getElementsByTagName('filename') #[<DOM Element: filename at 0x381f788>]
    #    filename = filenamelist[0].childNodes[0].data
    objectlist = annotation.getElementsByTagName('object')
    bboxes = []
    for objects in objectlist:
        namelist = objects.getElementsByTagName('name')
        class_label = namelist[0].childNodes[0].data

        bndbox = objects.getElementsByTagName('bndbox')[0]

        x1_list = bndbox.getElementsByTagName('xmin')
        x1 = int(float(x1_list[0].childNodes[0].data))
        y1_list = bndbox.getElementsByTagName('ymin')
        y1 = int(float(y1_list[0].childNodes[0].data))
        x2_list = bndbox.getElementsByTagName('xmax')
        x2 = int(float(x2_list[0].childNodes[0].data))
        y2_list = bndbox.getElementsByTagName('ymax')
        y2 = int(float(y2_list[0].childNodes[0].data))

        bbox = [x1,y1,x2,y2,class_label]
        bboxes.append(bbox)

    img = cv2.imread(imgfile)
    for bbox in bboxes:
        x1 = bbox[0]
        y1 = bbox[1]
        x2 = bbox[2]
        y2 = bbox[3]

        if x1 < 0 : x1 = 0
        if y1 < 0 : y1 = 0
        if x2 > img.shape[1] - 1 : x2 = img.shape[1] - 1
        if y2 > img.shape[0] - 1 : y2 = img.shape[0] - 1

        cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
        #cv2.putText(img,bbox[4],(bbox[0],bbox[1]),0.6,cv2.FONT_HERSHEY_SIMPLEX,2)
    cv2.imwrite(os.path.join(ProcessedPath,'%s.jpg' % labelfile[:-4]),img)
    print (labelfile)

    num += 1
    print (num)

