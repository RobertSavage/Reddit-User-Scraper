import praw
import requests
import bs4
from prawcore.exceptions import Forbidden
from time import sleep
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
with open('config.json') as config_file:
	data = json.load(config_file)

client_id = data['client_id']
client_secret = data['client_secret']
username = data['username']
password = data['password']
user_agent = data['user_agent']
reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,username=username,password=password,user_agent=user_agent)

listtest = []
print('START TIME: ', datetime.now())

def titleusers(subredd):
	with open('config.json') as config_file:
		data = json.load(config_file)

	limit = data['post_to_scrape']
	x = reddit.subreddit(subredd)
	y = x.new(limit=limit)
	worked = 0
	failed = 0
	try:
		for post in y:
			try:
				auth = post.author
				Text_file = open('temp.txt','a', encoding='utf-8')
				Text_file.write(str(post.author)+"\n")
				worked += 1
				sleep(0.5)
			except:
				print(f'{subredd}bad g')
				failed += 1
				sleep(5)
				continue
		print('----------------------------------------')
		print(str(subredd)+'_titleuser'+' TIME: ',  datetime.now())
		print(str(subredd)+'_titleuser'+' Worked: ',worked,' Failed: ', failed)
		print('----------','DONE: ',subredd,'----------')
		sucess = 0
		worked = 0
		sleep(20)
	except:	
		print(f'MESSED UP ALL ON {subredd}')
		sleep(20)
		pass
def commentusers(subredd):
	with open('config.json') as config_file:
		data = json.load(config_file)
	limit = data['post_to_scrape']
	x = reddit.subreddit(subredd)
	y = x.new(limit=limit)
	worked = 0
	failed = 0
	try:
		for post in y:
			for comment in post.comments:
				try:
					Text_file = open('temp.txt','a', encoding='utf-8')
					Text_file.write(str(comment.author)+"\n")
					worked += 1
					sleep(0.3)
				except:
					print(f'{subredd}bad subred')
					failed += 1
					sleep(5)
					continue
		print('----------------------------------------')
		print(str(subredd)+'_commentuser'+' TIME: ',  datetime.now())
		print(str(subredd)+'_commentuser'+' Worked: ',worked,' Failed: ', failed)
		print('----------','DONE: ',subredd,'----------')
		sucess = 0
		worked = 0
		sleep(20)
	except:	
		print(f'MESSED UP ALL ON {subredd}')
		sleep(20)
		pass

workers = data['workers']
subred = data['subreddits']
pull_title_users = data['pull_title_users']
pull_comment_users = data['pull_comment_users']

processes = []
with ThreadPoolExecutor(max_workers=workers) as executor:
	for sub in subred:
		if pull_title_users == True:
			processes.append(executor.submit(titleusers, sub))
		if pull_comment_users == True:
			processes.append(executor.submit(commentusers, sub))
for task in as_completed(processes):
	print(task.result())
print('END OF SCRAPE: ',datetime.now())
print('MAKING TEXT FILE UNIQUE')
lines_seen = set() # holds lines already seen
with open("userspulled.txt", "w") as output_file:
	for each_line in open("temp.txt", "r"):
		if each_line not in lines_seen: # check if line is not duplicate
			output_file.write(each_line)
			lines_seen.add(each_line)
os.remove("temp.txt")
print('TASK IS NOW COMPLETE')

'''
add onto
- unique list
'''
