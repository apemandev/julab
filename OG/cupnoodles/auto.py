#!/usr/bin/env python3

import argparse
import os
import json

def read_json_file(path):
	try:
		with open(path+"config.json", 'r') as file:
			data = json.load(file)
		return data
	except (IOError, json.JSONDecodeError) as e:
		print(f"无法读取JSON文件: {e}")
		return None

def create_custom_json(path,file_name,image,frames):
	
	readData = read_json_file(path)	
	baseUrl = readData["baseUrl"]
	text = readData["text"]
	color = readData["color"]
	imageUrl = baseUrl + image
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
		print("自定义JSON文件已创建成功。")
	except IOError:
		print("无法创建自定义JSON文件。")
		



def list_files_in_directory(path):
	list = []
	try:
		file_list = os.listdir(path)
		for file_name in file_list:
#			print(file_name)
			list.append(file_name)
		return list
	except FileNotFoundError:
		print("指定路径不存在")
		

		
# 创建参数解析器
parser = argparse.ArgumentParser(description='列出指定路径下的文件列表')
parser.add_argument('work_path', metavar='工作路径', type=str, help='要列出文件的路径')

# 解析命令行参数
args = parser.parse_args()

# 调用函数列出路径下的文件列表
album = list_files_in_directory(args.work_path)[0]
frames=list_files_in_directory(args.work_path)
create_custom_json(args.work_path,"demo.json",album,frames)
