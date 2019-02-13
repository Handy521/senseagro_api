#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 11:23:32 2019

@author: shinong
"""

import os
import requests
import base64
import shutil
import time
import sys
from pprint import pprint

class PlantRecognizer():

    def __init__(self):
        #init key
#        self.key_list = [{'api_key':'G5Vq7N0GGTBGK5C3vk4BV2N7', 'secret_key':'2NVxyDw46Ri6'},
#              {'api_key':'0BQDyq70rwrqvYG4Pxqlq6cI', 'secret_key':'thNFUnkeINVRoDtRun7j'},
#              {'api_key':'wgxFAFYzf1DNxtfpx0ltGOWV', 'secret_key':'00SjqCtYbKRYHgL1TV2'},
#              {'api_key':'wRGCrs8LMKLns6o3PncVmybg', 'secret_key':'HyGWBUOGBvlboDr7M'},
#              {'api_key':'nR4crblf18okFgqEFMHKEUaZ', 'secret_key':'rEibMAD1UM6loeIao'},
#              {'api_key':'bcGMFf1wvOq6OuvcxvMBuaoG', 'secret_key':'tTtuHvqddS4FZe'},
#              {'api_key':'1X5jrxzIC9wuXBx3iBFUwmv9', 'secret_key':'bBNzkiOjPfpifeEMmnut8'},
#              {'api_key':'WzR0OroAKIE7xwiKjPGRTpcL', 'secret_key':'HqgwwX3Igue6gYsVpzHf'},
#              {'api_key':'hNOvEkxktGbctqGbtbyAQE1g', 'secret_key':'xX4jGdLuT2CACnjn7d85LFxk'},
#              {'api_key':'l5H7LmEOQ6ngxQj6V91i9sFI', 'secret_key':'9TSFswGSl3jHD1bsT'},#
#              {'api_key':'byeXlLkdGWvCAoPPPK6gsyRe', 'secret_key':'A966erqa8q4he7D'},
#              {'api_key':'V6GGkpyfxYMAcWnzW9raGbmV', 'secret_key':'ZUzilF9v'},
#              {'api_key':'IxyvfymjcacoKk5TNqyKjLPO', 'secret_key':'z9'}]
        self.key_list ={'api_key':'NAqRuUQOyiO038NUNWVVCmOn', 'secret_key':'TEfgiQ'}
        self.access_token = self._get_access_token(self.key_list['api_key'],self.key_list['secret_key'])
        self.API_URL = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant' + '?access_token=' \
                        + self.access_token

    @staticmethod
    def _get_access_token(api_key, secret_key):
        api = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
              '&client_id={}&client_secret={}'.format(api_key, secret_key)
        #rp = requests.post(api)
        try:
            rp = requests.post(api, timeout=5)
        except:
            print('[ERROR]:request time out...')
            return
        if rp.ok:
            rp_json = rp.json()
            print(rp_json['access_token'])
            return rp_json['access_token']
        else:
            print('=> Error in get access token!')

    def get_result(self, params):
        # get access_token TODO
        try:
            rp = requests.post(self.API_URL, data=params, timeout=5)
        except:
            print('=> Error! token invalid or network error!')
            return
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
        label=test_path.split('/')
        log=open('log.txt', 'a+')  #log file
        log.write(test_path+'\n')
        flag=0
        f = open(test_path, 'rb')
        img_str = base64.b64encode(f.read())
        params = {'image': img_str, 'with_face': 1}
        tic = time.clock()
        rp_json = self.get_result(params)
        toc = time.clock()
        print('=> Cost time: ', toc - tic)
        #avoid request error
        try:
            result = rp_json['result']
        except:
            print('[ERROR]: 请求错误...')
            return

        for res in result[0:3]:
            if res['name'] == label[-2] and res['score'] > 0.15:
                if not os.path.exists(res['name']):  #true dir
                    os.mkdir(res['name'])
                shutil.move(test_path,label[-2])
                flag=1
            log.write('[name]: <{}>, [score]: <{}>.\n'.format(res['name'], res['score']))

        if flag==0:
            if not os.path.exists('xx'+label[-2]):  #error dir
                os.mkdir('xx'+label[-2])
            shutil.move(test_path,('xx'+label[-2]))
            log.write('xxxxxxxxx--claen_data--xxxxxxxxxxx\n')
        log.write('==================\n')

    def start(self, path):
        """
        path: 起始图像文件夹路径
        """
        # step1. 读 1 dir
        contents=os.listdir(path)
        for single_class in contents:
            single_class_path= os.path.join(path,single_class)
            #step2.
            for ii,image in enumerate(os.listdir(single_class_path)):
                img_path=os.path.join(single_class_path,image)
#                self.access_token = self._get_access_token(self.key_list['api_key'],self.key_list['secret_key'])
                self.detect(img_path)


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('[ERROR]:请指定需要处理图片文件的源路径...')
#    all_img_path='/media/shinong/study/try/Jun21_20class'
    all_img_path = sys.argv[1]
    recognizer = PlantRecognizer()
    recognizer.start(all_img_path)








