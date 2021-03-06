# !/usr/bin/env python
# -*- coding: UTF-8  -*-
# GetSina Weibo Repost_timeline
# Author: chengjun wang
# 20120328-20120407@Canberra

from weibo_api import api
import csv
import time
import sys
'''
Step 0: automatically get authorization by oauth2.0
'''
api=api()
'''
Step 1: get the repost_timeline 
'''	
"""The target weibo: http://www.weibo.com/2099181812/ybI0dopBD """
from base62 import base62_decode # import base62 module
mid='ybI0dopBD'	  # input the mid here
id1=base62_decode(mid[:1])	
id2=base62_decode(mid[1:-4])	
id3=base62_decode(mid[5:])
numList=[id1, id2, id3]
id=int(''.join(map(str,numList)))
print id


"""get the repost_count"""
for object in api.counts(ids=id):
    repost_count=object.__getattribute__('rt')
    print repost_count
pages= repost_count/200	+2  # why should it be 2? cuz python starts from 0
	
# import csv
# addressForSavingData= "C:/Python27/weibo/Weibo_repost/repostSave.csv"    
# file = open(addressForSavingData,'wb') # save to csv file
# for page in range(1, pages):
    # for object in api.repost_timeline(id=id, count=200, page=page):  # get the repost_timeline of a weibo
        # """1.1 reposts"""
        # pid = object.__getattribute__("id")
        # text = object.__getattribute__("text").encode('gb18030') # add encode here
        # created_at = object.__getattribute__("created_at")
        # in_reply_to_status_id = object.__getattribute__("in_reply_to_status_id")  
        # in_reply_to_user_id = object.__getattribute__("in_reply_to_user_id")  
        # in_reply_to_screen_name = object.__getattribute__("in_reply_to_screen_name").encode('gbk')  	
        # """1.2 reposts.user"""
        # user = object.__getattribute__("user")   # for object in user
        # user_id = user.id
        # user_name =user.name.encode('gbk') # add encode here
        # user_gender = user.gender
        # user_province = user.province
        # """2.1 retweeted_status"""
        # retweeted_status = object.__getattribute__("retweeted_status")
        # retweeted_status_id=retweeted_status.id  # the id of weibo,i.e. id
        # retweeted_status_text = retweeted_status.text.encode('gb18030') # add encode here 
        # """2.2 retweeted_status.user"""
        # retweeted_status_user_name = retweeted_status.user[u'name'].encode('gbk')
        # retweeted_status_user_province = retweeted_status.user[u'province']
        # w = csv.writer(file,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # w.writerow((pid, created_at, text, in_reply_to_status_id, in_reply_to_user_id, in_reply_to_screen_name, 
		       # retweeted_status_user_name, retweeted_status_user_province, user_id, user_name, user_gender, user_province)) # write it out		
# file.close()
# pass

'''
Step 2: get the social graph
# '''

"""get the user ids"""
dataReader = csv.reader(open('C:/Python27/weibo/Weibo_repost/repostSave.csv', 'r'), delimiter=',', quotechar='|')
data = []
for row in dataReader:
    data.append(int(row[8]))  # modify the number to get the diffusers' ids

"""get the friends"""	
# import functools
# get_friends_ids=functools.partial(api.friends_ids) #
addressForSavingData= "C:/Python27/weibo/Weibo_repost/friendSave.csv"    # change here to save in different file names
file = open(addressForSavingData,'wb') # save to csv file
user_list= data  # e.g. [123456, 1243844290] # input the list of user id
for user_id in user_list:
    max_ids=10000 # if the id is more than max_id, this script will stop to collect.
    cursor = -1
    ids=[]
    while cursor != 0:
        if api.rate_limit_status().remaining_hits >= 205:    
            response=api.friends_ids(id=user_id, count=5000, cursor=cursor)
            ids	+= response.ids
            cursor = response.next_cursor
            print api.rate_limit_status().remaining_hits, api.rate_limit_status().reset_time  #user_id
            w = csv.writer(file,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            w.writerow((user_id, ids)) 
            if len(ids) >= max_ids:
                break
        elif api.rate_limit_status().remaining_hits < 205:	
            sleep_time=api.rate_limit_status().reset_time_in_seconds # time.time()
            print sleep_time, api.rate_limit_status().reset_time
            time.sleep(sleep_time+2)
file.close()
pass	
