#coding:utf-8
#Author:LSA
#Description:cms identification tool
#Date:20171030

import requests
import json
import hashlib

import gevent
from gevent.queue import Queue
from gevent import monkey; monkey.patch_all()

import time
import glob
import urllib
import urllib2
import re
import rule
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')



class cmsIdentificate(object):
    def __init__(self,tgtUrl,scanMode):
        
        self.tgtUrl = tgtUrl.rstrip("/")
	self.scanMode = scanMode
	self.header = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'}
	self.found = 0	
		
    def getMd5(self,rspfile):
        md5 = hashlib.md5()
        md5.update(rspfile)
        return md5.hexdigest()

    def clearQueue(self):
	
        while not self.cms0Queue.empty():
            self.cms0Queue.get()
    

    def cmsScan0(self):
	while not self.cms0Queue.empty():

        	cmsjson = self.cms0Queue.get()
		#print 'checking ' + self.tgtUrl + cmsjson["url"]
        	finalUrl = self.tgtUrl + cmsjson["url"]
        	rsphtml = ''
        	try:
		
            		rsp = requests.get(finalUrl,headers=self.header,timeout=10)
            		if (rsp.status_code != 200):
                		continue
				#return
            		rsphtml = rsp.text
            		if rsphtml is None:
                		continue
				#return
        	except:
            		rsphtml = ''

        	if cmsjson["re"]:
			#print cmsjson["re"]
            		if (rsphtml.find(cmsjson["re"]) != -1):
                		result = cmsjson["name"]
                		print("target's cms is : %s source: %s keyword : %s" % (result, finalUrl, cmsjson["re"]))
                		self.clearQueue()
				return True
				#sys.exit(0)
        	else:
            		md5 = self.getMd5(rsphtml)
            		if (md5 == cmsjson["md5"]):
                		result = cmsjson["name"]
                		print("target's cms is : %s |source : %s |md5 : %s" % (result, finalUrl, cmsjson["md5"]))
                		self.clearQueue()
				return True
				#sys.exit(0)

    def cmsScan1(self):
   	
    	while not self.cms1Queue.empty():
		
		line = self.cms1Queue.get()
		#print 'checking ' + self.tgtUrl + line[0]
            	try:
                	rsp1 = requests.get(self.tgtUrl + line[0],headers=self.header,timeout=10)
                	if rsp1.status_code != 200:
                    		continue
            	except:
                	continue
            	rsp1html = rsp1.text
            	if re.compile(r'(?i)'+line[1]).search(rsp1html):
			#self.found = self.found + 1
			#if self.found >= 3:
                    	print "target's cms is : " + line[2] + ' |source : ' + self.tgtUrl + line[0] + ' |keyword is ' + line[1]
                    	sys.exit(0)        	
    	#print 'not found!' 

    def cmsScan2(self):
	while not self.cms2Queue.empty():
		q2line = self.cms2Queue.get()
		#print 'checking ' + self.tgtUrl + q2line[0]
		try:
			rsp3 = requests.get(self.tgtUrl + q2line[0],headers=self.header,timeout=10)
			if rsp3.status_code != 200:
				continue
		except:
			continue
		rsp3html = rsp3.text
		
		r3md5 = self.getMd5(rsp3html)
		if(r3md5 == q2line[2]):
			print "target's cms is " + q2line[1] + '|source : ' + self.tgtUrl + q2line[0] + '|md5 : ' + q2line[2]
			sys.exit(0)


    def cmsScan3(self):
	while not self.cms3Queue.empty():
		q3line = self.cms3Queue.get()
		#print 'checking ' + self.tgtUrl + q3line[0]
		try:
			rsp4 = requests.get(self.tgtUrl + q3line[0],headers=self.header,timeout=10)
			if rsp4.status_code == 200:
				print "target's cms is " + q3line[1] + '|source ' + self.tgtUrl + q3line[0]		
				sys.exit(0)
			else:
				continue
		except:
			continue
		


    def scan_title(self,title):
    		titlerule = rule.title
    		web_information = 0
    		for key in titlerule.keys():
        		req = re.search(key,title,re.I)
        		if req:
            			web_information = titlerule[key]
            			break
        		else:
            			continue
    		return web_information

    def scan_head(self,header):
   	 	headrule = rule.head
    		web_information = 0
    		for key in headrule.keys():
        		if '&' in key:
            			keys = re.split('&',key)
            			if re.search(keys[0],header,re.I) and re.search(keys[1],response,re.I) :
                			web_information = headrule[key]
                			break
            			else:
                			continue
        		else:
            			req = re.search(key,header,re.I)
            			if req:
                			web_information = headrule[key]
                			break
            			else:
                			continue
    		return web_information




    def scan_body(self,response):
    		body = rule.body
    		web_information = 0
    		for key in body.keys():
       			 
        		if '&' in key:
            			keys = re.split('&',key)
            			if re.search(keys[0],response,re.I) and re.search(keys[1],response,re.I):
                			web_information = body[key]
                			break
            			else:
                			continue
        		else:
            			req = re.search(key,response,re.I)
            			if req:
                			web_information = body[key]
                			break
            			else:
                			continue
    		return web_information



    

    
       
    def cmsScan(self,coroutine=100):
        
	if(self.scanMode=='json'):
		#cms0init()
		self.cms0Queue = Queue()
        	fp0 = open('data.json')
        	cmsData = json.load(fp0, encoding="utf-8")
        	for i in cmsData:
            		self.cms0Queue.put(i)
        	fp0.close()
       		print("cms0Data total:%d"%len(cmsData))
		print 'Scanning......'
	
        	corlist0 = [gevent.spawn(self.cmsScan0) for i in range(coroutine)]
        	gevent.joinall(corlist0)

		print 'Over!'
        
       	if(self.scanMode=='holdsword'):
		#cms1init()
		self.cms1Queue = Queue()
		yjcmsList = glob.glob('./yjcms/*')
		
    		for cmstype in yjcmsList:
        		for line in open(cmstype, 'r'):
            			line = line.strip().split('------')
            			if len(line) != 3:
                			continue 
				self.cms1Queue.put(line) 
		print 'Scanning......'
		corlist1 = [gevent.spawn(self.cmsScan1) for i in range(coroutine)]
        	gevent.joinall(corlist1)

		print 'Over!'
	if(self.scanMode=='thb'):
		print 'collecting index......'
		rsp2 = requests.get(url=self.tgtUrl,headers=self.header,timeout=10)
        	
		bresponse = BeautifulSoup(rsp2.text,"lxml")
		title = bresponse.findAll('title')   
                       
		for i in title:
    			title = i.get_text()

		head = rsp2.headers
   			
		response = rsp2.text

		header = ''
		for key in head.keys():                             
    			header = header+key+':'+head[key]
   
		print('collecting index finished!')
		web_information = self.scan_title(title)
    		if web_information == 0:
       			web_information = self.scan_head(header)
        		if web_information == 0:
            			web_information = self.scan_body(response)
            			if web_information == 0:
               				print('Not found!')
                			sys.exit()
            			else:
                			print(web_information)
        		else:
            			print(web_information)
    		else:
        		print(web_information)

	if(self.scanMode=='fast'):
		self.cms2Queue = Queue()
		fp1 = open('cms00.txt')
		for line2 in fp1:
			line2 = line2.strip().split(' ')
			self.cms2Queue.put(line2)
		print 'Scanning......'

		corlist2 = [gevent.spawn(self.cmsScan2) for i in range(coroutine)]
        	gevent.joinall(corlist2)
	
		print 'Over!'

	if(self.scanMode=='rapid'):
		self.cms3Queue = Queue()
		fp2 = open('cms1.txt')
		for line3 in fp2:
			line3 = line3.strip().split(' ')
			self.cms3Queue.put(line3)
		print 'Scanning......'
		
     		corlist3 = [gevent.spawn(self.cmsScan3) for i in range(coroutine)]
        	gevent.joinall(corlist3)
	
		print 'Over!'
			
		


if __name__ == '__main__':
	tgtUrl = sys.argv[1]
	
	scanMode = raw_input("请选择扫描模式：json(结合式)/holdsword(御剑式)/thb(主页式)/fast(快速式)/rapid(急速式): ")
	
	c = cmsIdentificate(tgtUrl,scanMode)
	c.cmsScan(500)

