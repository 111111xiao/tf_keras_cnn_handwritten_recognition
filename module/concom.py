#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

import cv2 
import tensorflow as tf

from tensorflow import keras


# In[ ]:


model = keras.models.load_model('/home/admin/module/keras.h5')


# class Node:
class Node:
    
    def __init__(self, x = 0, y = 0):
        self.x_min = self.x_max = x
        self.y_min = self.y_max = y
        self.next = None
        self.con = False
        self.sort = False
        self.obj = 'n'
        self.img = None
        self.area = 0
        self.lev = 0
        
    def cp(self, node):
        self.x_min = node.x_min; self.x_max = node.x_max;
        self.y_min = node.y_min; self.y_max = node.y_max;
        
# x = x_max - x_min, y = y_max - y_min
def make_img(x, y, node, img):
    #node.area = x * y;
    border = max(x, y) + 30
    node.area = border * border;
    _x = int((border - x) / 2)
    _y = int((border - y) / 2)
    
    v_image = np.full((_x, y), 255)
    result_image = img[node.x_min:node.x_max, node.y_min: node.y_max]
    # concat img by direct v
    result_image = np.vstack([v_image, result_image])
    result_image = np.vstack([result_image, v_image])
    
    xx, yy = result_image.shape
    h_image = np.full((xx, _y), 255)
    # concat img by direct h
    result_image = np.hstack([h_image, result_image])
    result_image = np.hstack([result_image, h_image])
    return result_image

def preprocessing_and_predict_image(image, IMAGE_SIZE = 28, flag = 0):
    # flag = 0 calculate
    # flag = 1 mathjax
    rescaler = 255.0 - image
    rescaler = rescaler / 255.0
    resize = cv2.resize(rescaler, (IMAGE_SIZE, IMAGE_SIZE))
    reshape = np.array(resize).reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 1)
    pred = model.predict(reshape)
    index = int(np.argmax(pred, axis = 1))
    if flag == 0: 
        result = classes[index]
    else:
        result = classes2[index]
    return result

classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+', '=', '*', '/', 'x', '(', ')', '@', 'e', 'r', 'y']
classes2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+', '=', '*', '\\div', 'x', '\\left(', '\\right)', '\\pi', 'e', 'r', 'y']


# change mark

# merge node by vertial
def merge_by_vertial(node):
    # node is waiting for being connected
    tmp_node1 = node.next
    if tmp_node1.next.y_min != None and \
    tmp_node1.y_min - 1 <= ((tmp_node1.next.y_min + tmp_node1.next.y_max) / 2.0) and \
    ((tmp_node1.next.y_min + tmp_node1.next.y_max) / 2.0) <= tmp_node1.y_max + 1 or \
    tmp_node1.next.y_min - 1 <= ((tmp_node1.y_min + tmp_node1.y_max) / 2.0) and \
    ((tmp_node1.y_min + tmp_node1.y_max) / 2.0) <= tmp_node1.next.y_max + 1:
        # next node is the destination node
        merge(tmp_node1.next, tmp_node1)
        node.next = tmp_node1.next
        return False
    return True

def is_subset(node1, node2):
    if node1.x_min >= node2.x_min and \
    node1.x_max <= node2.x_max and \
    node1.y_min >= node2.y_min and \
    node1.y_max <= node2.y_max:
        return True
    return False
    
# if x is y subset or y is subset delete x or y 
def find_subset(node):
    tmp_node1 = node.next
    tmp_node2 = node.next
    if tmp_node2.next != None:
        tmp_node2 = tmp_node2.next
        if is_subset(tmp_node1, tmp_node2) or is_subset(tmp_node2, tmp_node1):
            node.next = tmp_node1.next
            # do not move
            return False
    return True

# find the image if pixel counts lower n
# useless image
def find_small_image(node, n = 4):
    tmp_node1 = node.next
    if tmp_node1.next != None:
        if ((tmp_node1.x_max - tmp_node1.x_min) + (tmp_node1.y_max - tmp_node1.y_min)) <= n :
            node.next = tmp_node1.next
            return False
    return True
    
# judge if index by axis
def is_index(prenode, node):
    if prenode.x_min > (node.x_max - node.x_min) / 2 + node.x_min and \
    (prenode.area > node.area or ((prenode.x_max - prenode.x_min) > (node.x_max - node.x_min))):
        return True
    return False
    
def find_index(node, level):
    # lev is level
    # node is prenode
    if node.next != None:
        if is_index(node, node.next):
            level = level + 1
        elif is_index(node.next, node):
            level = 0
        else:
            level = level
        node.next.lev = level
    return level

# class linkList
class linkList:
    
    def __init__(self):
        self.head = Node()
        
    def insert(self, node):
        tmp_node = self.head
        while tmp_node.next != None:
            tmp_node = tmp_node.next 
        tmp_node.next = node
        node.next = None
        
    def is_empty(self):
        if self.head.next == None:
            return True
        else:
            return False
        
# display function

    def display_xy(self):
        tmp_node = self.head
        print("x_min y_min x_max y_max area")
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            print(tmp_node.x_min, tmp_node.y_min, tmp_node.x_max, tmp_node.y_max, 
                 tmp_node.area)
        
    # get the object in the list
    def display_level(self):
        tmp_node = self.head
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            print(tmp_node.obj, tmp_node.lev)
    
    # get the object in the list        
    def display_obj(self, arr):
        tmp_node = self.head
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            arr.append(tmp_node.obj)
            if tmp_node.next != None and tmp_node.lev < tmp_node.next.lev:
                arr.append('^')
            
# preprocessing function
# predict function

    # make the images in the list convert to rect image
    def make_image_list(self, image):
        merge_flag = 1
        while merge_flag == 1:
            merge_flag = self.merge_list_vertial()
        self.del_subset()
        tmp_node = self.head
        # make img from data to image
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            # area is calculated here
            tmp_node.img = make_img(tmp_node.x_max - tmp_node.x_min,
                                    tmp_node.y_max - tmp_node.y_min,
                                    tmp_node, image)
            #tmp_node.img = test(tmp_node, image)
            #plt.imshow(tmp_node.img)
            #plt.show()
    
    def layered_level(self):
        level = 0
        tmp_node = self.head
        tmp_node.next.lev = level 
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            level = find_index(tmp_node, level)
    
    def merge_list_vertial(self):
        length = self.get_length()
        index = 0
        flag = 0
        tmp_node = self.head
        while index < length:
            go_next = merge_by_vertial(tmp_node)
            if go_next == True:    
                index += 1
                tmp_node = tmp_node.next
            else:
                length = length - 1
                flag = 1
        return flag
                
    def preprocess(self, image):
        tmp_node = self.head
        self.del_small_image()
        self.del_last_node()
        # get part of image
        self.make_image_list(image)
    
    def predict_list(self):
        tmp_node = self.head
        while tmp_node.next != None:
            tmp_node = tmp_node.next
            tf.compat.v1.reset_default_graph()
            tmp_node.obj = preprocessing_and_predict_image(tmp_node.img)
        print("Done!")

# delete useless images
# subset, too small, last
# last image can't be process
# so add last image in con_com and delete it befor predict
    def get_length(self):
        length = 0
        tmp_node = self.head.next
        if tmp_node == None:
            return length
        while tmp_node.next != None:
            length += 1
            tmp_node = tmp_node.next
        return length
    
    def del_subset(self):
        length = self.get_length()
        index = 0
        tmp_node = self.head
        while index < length:
            go_next = find_subset(tmp_node)
            if go_next == True:    
                index += 1
                tmp_node = tmp_node.next
            else:
                length = length - 1

    
    def del_small_image(self):
        length = self.get_length()
        index = 0
        tmp_node = self.head
        while index < length:
            # set small images size and delete
            go_next = find_small_image(tmp_node, 10)
            if go_next == True:    
                index += 1
                tmp_node = tmp_node.next
            else:
                length = length - 1

    def del_last_node(self):
        tmp_node = self.head
        while tmp_node.next.next:
            tmp_node = tmp_node.next
        tmp_node.next = None
        
# merge node to desNode
def merge(desNode, node):
    desNode.x_min = min(desNode.x_min, node.x_min)
    desNode.x_max = max(desNode.x_max, node.x_max)
    desNode.y_min = min(desNode.y_min, node.y_min)
    desNode.y_max = max(desNode.y_max, node.y_max)
    node.con = True


# get all img from imgData by connected componment
def connected_components(img):
    x, y = img.shape
    _x = 0
    _y = 0
    img_list = linkList();
    # pre_layer use 2 times loops to save one line image
    # pre_layer2 use for saving all pre image
    pre_layer = linkList();
    pre_layer2 = linkList();
    while _y < y:
        # this_layer is only use for one loop to save one new line image
        # this_layer2 use for saving image after merge new line and assgin to pre_layer2
        this_layer = linkList()
        this_layer2 = linkList()
        while _x < x:
            if img[_x][_y] <= 100:
                # next pixel is not white
                node = Node(_x, _y)
                _x += 1
                while _x < x and img[_x][_y] <= 100:
                    # get next pixel into img
                    node.x_max += 1
                    _x += 1
                if pre_layer.is_empty() == True:
                    # node is a new img
                    this_layer.insert(node)
                    this_layer2.insert(node)
                else:
                    this_layer.insert(node)
                    # node2 have same values with node but not same space
                    node2 = Node(0, 0)
                    node2.cp(node)
                    # preLayer have some img merge to preimg
                    tmp_node = pre_layer.head.next# first img
                    tmp_node2 = pre_layer2.head.next
                    while tmp_node != None:
                        # 1 use for judge and 2 use for merge
                        # merge new line image to tl2
                        if tmp_node.x_min - 20 <= node2.x_max and node2.x_min <= tmp_node.x_max + 20:
                            merge(node2, tmp_node2)
                        
                        this_layer2.insert(node2)
                        tmp_node = tmp_node.next   
                        tmp_node2 = tmp_node2.next 
            else:
                # next piexl is not black
                _x += 1
        tmp_node = pre_layer2.head.next;#after screen
        while tmp_node != None:
            if tmp_node.con == False:
                img_list.insert(tmp_node)
            
            tmp_node = tmp_node.next
        
        # after the row loop thisLayer become the preLayer
        pre_layer = this_layer
        pre_layer2 = this_layer2
        _y += 1 
        _x = 0
    # del node in make_image_list
    node = Node(0, 0)
    img_list.insert(node)
    return img_list

# get horizontal projection image
def get_h_projection(image, images):
    (h,w)=image.shape # height width
    a = [0 for z in range(0, h)] # black count

    for j in range(0,h): 
        for i in range(0,w):
            if  image[j,i]==0:  
                a[j]+=1         
    y = []
    flag = 0
    for i in range(0,len(a) - 1):
        if a[i] == 0:
            if flag == 0:
                if 0 != a[i + 1]:
                    y.append(i + 1)
                    flag = 1
            else:
                if 0 == a[i + 1]:
                    y.append(i)
                    flag = 0
    i = 0
    while i < len(y):    
        images.append(image[y[i]:y[i + 1]])
        i+=2

def predict_division(res, res2, lis3):
    # res use for calculate
    # res2 use for mathjax
    # judge if division by middle area
    test_node = lis3.head
    areas = []
    while test_node.next:
        test_node = test_node.next
        areas.append(test_node.area)
    areas.sort()
    area = areas[int(lis3.get_length() / 2)]
    # for index
    level = 0
    # use h_projection and con_com to predict single image
    test_node = lis3.head
    lis3.layered_level()
    while test_node.next:
        images = []
        test_node = test_node.next
        get_h_projection(test_node.img, images)
        if test_node.lev == 0:
            level = 0
        if test_node.lev > level:
            level = test_node.lev
            res.append('^')
            res2.append('^')
        # this is multi images
        # separate division operator images
        if len(images) >= 3 and (area < test_node.area or preprocessing_and_predict_image(test_node.img) != '/'):
            i = 0
            res.append('(')
            res2.append("\\frac")
            for img in images:
                if i % 2 != 0:
                    res.append('/')
                    i += 1
                    continue
                res.append('(')
                res2.append('{')
                t_lis = connected_components(img)
                t_lis.preprocess(img)
                t_lis.layered_level()
                predict_division(res, res2, t_lis)
                res.append(')')
                res2.append('}')
                i += 1
            res.append(')')
        else:
            #lis3.predict_list()
            #lis3.display_obj(res) after con_com make repeat elements
            res.append(preprocessing_and_predict_image(test_node.img))
            res2.append(preprocessing_and_predict_image(test_node.img, flag = 1))
            
def make_predict(image, result):
    # result use for calculate
    # results use for show
    results = []
    lis3 = connected_components(image)
    if lis3.is_empty():
        return "error"
    lis3.preprocess(image)
    predict_division(result, results, lis3)
    return results
