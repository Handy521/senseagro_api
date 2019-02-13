#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 17:55:56 2019

@author: shinong
"""

import os
import requests
import base64
from pprint import pprint
import time
import json
import shutil

class PlantRecognizer():
    """
    baidu easydl release model api,call and test 
    """
    def __init__(self):
        #init key        
        self.key_list = {'api_key':'ruULG1SpNTZeD1peYQxebfjS', 'secret_key':'KXoKM0Vszt'} #song_yang account
#        self.key_list = {'api_key':'H8YLLk18i7DApqG8DUoSG6xu', 'secret_key':'TKRWncbdr7Kup'} #myself
        self.access_token = self._get_access_token(self.key_list['api_key'],self.key_list['secret_key'])
        self.API_URL = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/shinong_30' + '?access_token=' \
                + self.access_token

    @staticmethod
    def _get_access_token(api_key, secret_key):
        api = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
              '&client_id={}&client_secret={}'.format(api_key, secret_key)
        rp = requests.post(api)
        if rp.ok:
            rp_json = rp.json()
            print(rp_json['access_token'])
            return rp_json['access_token']
        else:
            print('=> Error in get access token!')
            
    def get_result(self, params):
        # get access_token TODO
        print(self.API_URL)
        headers = {
                'Content-Type':'application/json'
                }
        rp = requests.post(self.API_URL, data=params, headers=headers)
        time.sleep(1)  #request delay

        if rp.ok:
            print('=> Success! got result: ')
            rp_json = rp.json()
            pprint(rp_json)
            return rp_json
        else:
            print('=> Error! token invalid or network error!')
            print(rp.content)
            return None
        
    def detect(self, test_path):
        """
        detect single image
        """
        f = open(test_path, 'rb')
        img_str = base64.b64encode(f.read()).decode()  #img format decode
        params = {'image':img_str, "top_num": 5}
        params = json.dumps(params)   
        tic = time.clock()
        rp_json = self.get_result(params)
        toc = time.clock()
        print('=> Cost time: ', toc - tic)
        #avoid request error     
        result = rp_json['results']
        shutil.move(test_path,'xxxxx')  #delete origin_img
        return result[0]            

    def start(self, path):
        """
        path: 起始图像文件夹路径
        """
        log=open('loglabel_10.txt', 'a+')  #log file        
        # step1. 读 1 dir
        contents=os.listdir(path)
        for single_class in contents:
            single_class_path= os.path.join(path,single_class)
            flag=0
            #step2.
            for ii,image in enumerate(os.listdir(single_class_path)):
                img_path=os.path.join(single_class_path,image)
                label=img_path.split('/')
                log.write(img_path+'\n')
                try:
                    res=self.detect(img_path)
                except:
                    print("request-error:=========")
                    return
                if res['name'] == label[-2]:
                    flag+=1

                log.write(' {}, [score]: <{}>.\n'.format(res['name'], res['score']))
            log.write(str(flag)+'\n')
            log.write('class:'+label[-2]+'\n')
                            
if __name__ == '__main__':
    
    all_img_path='/media/shinong/study/30_easy_test'
    recognizer = PlantRecognizer()
    recognizer.start(all_img_path)








