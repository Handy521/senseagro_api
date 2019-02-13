#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:12:00 2019

@author: shinong
"""
#针对记录的log求P、R、accuracy、F1score

import numpy as np
from collections import Counter
 
def evaluate(all_predict_value,label_count,new_label): 
    """
    recorded dictionary
    """
    #init
    total_dict,tp_dict,tp_fp_dict = {}, {},{} #tp预测为正，tp_fp预测真实结果
    for label in range(0,40):#40个类别
        tp_fp_dict[label]=0
        tp_dict[label]=0
        total_dict[label]=0
    for ii,value in enumerate (new_label) :
        total_dict[value]=label_count[ii+1]-label_count[ii]
    for ii ,value in enumerate (new_label):
        for jj,value2 in enumerate(all_predict_value[label_count[ii]:label_count[ii+1]]):
            if value2==value:
                tp_dict[value]+=1
    for i in all_predict_value:
        tp_fp_dict[i]+=1            
    return total_dict,tp_dict,tp_fp_dict

def label_convert_numbel(path):
    """
    将原来的中文名label转换为数字标签
    """
    f=open(path,encoding='utf-8') #在Windows下为gbk格式，不能读取中文
    origin_name=[]
    label_number=[]
    label_dividion=[]
    label='a'      #init,arbitrary value
    new_label=[]
    for line in f:        #log第一行为文件路径名，第二行为预测值
        if len(line)> 10 :
            label=line.split('/')
            origin_name.append(label[-2])
        else:
            name=int(line)    
            label_number.append(name)

    for ii,index in enumerate(origin_name) : #将相同label的序号分割出来        
        if label != index :
            label=index                                            
            label_dividion.append(ii) 
    label_dividion.append(ii) #添加最后一个预测值
    f=open('category.txt','w') #保存类别对应名
    for jj in range(40): #假设相同label中预测出现最多的值为真实标签
        temp_list=label_number[label_dividion[jj]:label_dividion[jj+1]]    
        temp_dict=Counter(temp_list)
        temp_v=0               #求出字典中最大的value
        for k,v in temp_dict.items():
            if v>temp_v: 
                temp_v=v
                remember=k
        new_label.append(remember)
        
        f.write(origin_name[label_dividion[jj]]+':'+str(remember)+'\n')
    f.close()        
        
    return origin_name,label_number,label_dividion, new_label

def compute(total_dict,tp_dict,tp_fp_dict):
    """
    计算准确率，召回率，精确率，F1score
    """
    tp,total_count,rec,pre=0,0,0,0
    F1=np.zeros(40)
    for k,v in tp_dict.items():
        tp+=v
        total_count+=total_dict[k]
        recall=tp_dict[k]/total_dict[k]
        rec=rec+recall
        precision=tp_dict[k]/tp_fp_dict[k]
        pre=pre+precision
        F1[k]= 2*(precision*recall) / (precision+recall)
    acc= tp / total_count
    rec_average= rec / (k+1)
    pre_average= pre / (k+1)
    F1_average= sum(F1) / (k+1)
    return acc,rec_average,pre_average,F1,F1_average

if __name__=='__main__':

    path="./category40_log.txt"  #log第一行为文件路径名，第二行为预测值
    a,b,c,d=label_convert_numbel(path)
    total_dict,tp_dict,tp_fp_dict=evaluate(b,c,d)
    acc,rec_average,pre_average,F1,F1_average=compute(total_dict,tp_dict,tp_fp_dict)
    
    
