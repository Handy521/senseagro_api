#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:40:09 2019

@author: shinong
"""

import os
import tensorflow as tf

from collections import Counter
import time
    
def test_img(pb_path,image_name):
    """
    """
    # step1. import pb
    with tf.gfile.FastGFile(pb_path, 'rb') as f:                                                                                      
        graph_def = tf.GraphDef()                                                                                                                  
        graph_def.ParseFromString(f.read())                                                                                                        
        _ = tf.import_graph_def(graph_def, name='')  
    # step2. 
    with tf.Session() as sess:
        log=open('category40_log.txt', 'a+')                                                                             
        for single_img in image_name:             
            log.write(single_img+'\n')                                                                                   
            # Read in the image_data                                                                                                               
            image_data = tf.gfile.FastGFile(single_img, 'rb').read()                                                                               
            # Feed the image_data as input to the graph and get first prediction                                                                   
            softmax_tensor = sess.graph.get_tensor_by_name('final_training_ops/final_ret:0')                                                                                                                                                 
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})                                                                          
 
            # Sort to show labels of first prediction in order of confidence                                                                       
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            print(top_k[0])
            log.write(str(top_k[0])+'\n')
#            acc.append(top_k[0]) #for test single document 
#            ret=Counter(acc)
#            print(ret)
#            value=[]
#            for k,v in ret.items():
#                value.append(v)              
#            print((max(value))/b)
    log.close()
    
def all_test_img(test_path):
    """
    save image path to list
    """
    image_name=[]
    sub_dirs = [x[0] for x in os.walk(test_path)]
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir = False
            continue
        print(sub_dir)
        second_dir=os.path.join(test_path,sub_dir)
        for image in os.listdir(second_dir):    
            image_path=os.path.join(second_dir,image)
            image_name.append(image_path)
    return image_name        
           
if __name__ == '__main__':

    pb_path = 'out40.pb' #inception v3 model
    image_dir = '/media/shinong/study/try/test_1-28' #test set
    image_name=all_test_img(image_dir)
    test_img(pb_path,image_name)