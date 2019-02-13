#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:51:49 2019

@author: shinong
"""

def evaluate(logtxt_path): 
    """
    针对记录的log求P、R、accuracy、F1score
    """
    #init
    tp_dict,tp_fp_dict = {},{} #tp预测为正，tp_fp预测真实结果
    rec,tru,pre=0,0,0  
    key_label,val=[],[]#key:标签，val:记录单个类别预测正确样本
    for label in range(1,31):#31个类别，label从1开始
        tp_fp_dict[label]=0
        tp_dict[label]=0
    #read line 
    f=open(logtxt_path,'r') 
    for line in f :  
       if len(line)>45:
           continue # 图片路径略过
       elif len(line) > 30: # 图片预测值
           label=line[1:3]
           try:
               a=int(label)    #10以上的label占两位
           except:
               a=int(label[0:1]) # 1-9为1位
           tp_fp_dict[a]+=1
       else :
           if len(line)<5:
               value=line
               val.append(int(value))
           else:
               key=line[6:]
               key_label.append(int(key))
    for ii in range(0,30):
        tp_dict[key_label[ii]]=val[ii]   
        tru=tru+val[ii]   # all true example
        recall=val[ii]/20 # recall rate=predict correct numbel/all number
        rec=rec+recall
    
    for jj in range(1,31):
        precision=tp_dict[jj]/tp_fp_dict[jj] # precision=predict correct numbel/all predict this class number
        pre=pre+precision    
    acc=tru/600        #total sample:600 
    rec_mean=rec/30    #30class 
    pre_mean=pre/30
    F1=((pre*rec*2)/30)/(pre+rec)       
    return acc,rec_mean,pre_mean,F1

if __name__=='__main__':
    path="./loglabel.txt" 
    acc,rec_mean,pre_mean,F1=evaluate(path)
    print('accuracy:%.3f'%acc)
    print('recall:%.3f'%rec_mean)
    print('precison:%.3f'%pre_mean)
    print('F1score:%.3f'%F1)
