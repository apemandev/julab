#!/usr/bin/env python3

import argparse
import os
import json
import socket


def get_ip_address():
	# 创建一个UDP套接字
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	try:
		# 连接到一个公共的域名
		sock.connect(("8.8.8.8", 80))
		# 获取本地IP地址
		ip_address = sock.getsockname()[0]
	finally:
		# 关闭套接字连接
		sock.close()
		
	return ip_address

def read_json_file(path):
	try:
		with open(path+"config.json", 'r') as file:
			data = json.load(file)
		return data
	except (IOError, json.JSONDecodeError) as e:
		print(f"无法读取JSON文件: {e}")
		return None

def create_custom_json(path,file_name,frames,dir_name,ip):
	
	readData = read_json_file(path)	
	baseUrl = readData["baseUrl"]
	
	if len(ip) > 0 :
		baseUrl = ip
	
#	baseUrl2 = get_ip_address()+":8888/"
	
	text = dir_name
	color = readData["color"]
	imageUrl = ""
	frameUrls = [] 
	for frame in frames:		
		if ".DS_Store" in frame:
			continue
		frameUrl = baseUrl + frame
		frameUrls.append(frameUrl)
	
	data = [{
		"text": text,
		"image": imageUrl,
		"color":color,
		"frames": frameUrls
	}
	]
		
	
	try:
		with open(path+file_name, 'w') as file:
			json.dump(data, file, indent=4)
		print("自定义JSON文件已创建成功。",baseUrl+file_name)
	except IOError:
		print("无法创建自定义JSON文件。")
		
	


def list_files_in_directory(path):
	list = []
	try:
		file_list = os.listdir(path)
		for file_name in file_list:
#			print(file_name)
			if ".png" in file_name:
				list.append(file_name)
		return list
	except FileNotFoundError:
		print("指定路径不存在")
		

current_dir = os.getcwd()
dir_name = os.path.basename(current_dir)


ip="http://"+get_ip_address()+":8888/"
print("当前IP地址是:", ip)

# 创建参数解析器
#parser = argparse.ArgumentParser(description='列出指定路径下的文件列表')
#parser.add_argument('work_path', metavar='工作路径', type=str, help='要列出文件的路径')
#
## 解析命令行参数
#args = parser.parse_args()
work_path = "./"
# 调用函数列出路径下的文件列表
#album = list_files_in_directory(args.work_path+"album")[0]
frames=list_files_in_directory(work_path)

#print(frames)



folder = os.path.basename(work_path)

create_custom_json(work_path,"{0}.json".format(dir_name),frames,dir_name,"")
create_custom_json(work_path,"{0}_locol.json".format(dir_name),frames,dir_name,ip)


