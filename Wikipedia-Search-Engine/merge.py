import sys
import os
from heapq import heapify, heappush, heappop
from glob import glob

secIndex = {}

def writeToFile(inverted_index):
	global filenum, num_inverted_index
	filepath = path_to_merged_index_folder +"/index" + str(filenum)+".txt"
	firstWordFlag = True

	with open(filepath, 'w', encoding="utf-8") as f:
		for word in sorted(inverted_index):
			if firstWordFlag:
				secIndex[word]=filenum
				firstWordFlag = False
			f.write(word+":"+inverted_index[word]+"\n")
	print ("file ", filenum, "  created..!!!\n")
	filenum += 1
	num_inverted_index += len(inverted_index)
	


def writeSecIndex():
	with open(path_to_secondary_file, "w") as f:
		for word in sorted(secIndex):
			f.write(word+"\n")


def mergeKFiles():
	inverted_index = {}
	k_heap = []
	total_words_till_now = 0
	total_temp_index_files = len(temp_index_files)
	print("num of temp files : ", total_temp_index_files)
	file_pointers = {}

	fileProcessed = {}
	row_of_file = {}
	posting_list = {}

	for num in range(total_temp_index_files):
		fileProcessed[num] = False
		try:
			file_pointers[num] = open(temp_index_files[num], "r", encoding="utf-8")
		except:
			pass

		row_of_file[num] = file_pointers[num].readline()
		posting_list[num] = row_of_file[num].strip().split(":")

		if(posting_list[num][0] not in k_heap):
			heappush(k_heap, posting_list[num][0])

	num_parsed_files = 0

	while (num_parsed_files < total_temp_index_files):
		total_words_till_now += 1
		top_word = heappop(k_heap)

		for num in range(total_temp_index_files):
			if not fileProcessed[num] and top_word == posting_list[num][0]:
				if top_word not in inverted_index:
					inverted_index[top_word] = posting_list[num][1]
				else:
					inverted_index[top_word] += "," + posting_list[num][1]

				row_of_file[num] = file_pointers[num].readline()
				if row_of_file[num]:
					posting_list[num] = row_of_file[num].strip().split(":")
					if(posting_list[num][0] not in k_heap):
						heappush(k_heap, posting_list[num][0])
				else:
					fileProcessed[num] = True
					num_parsed_files += 1
					file_pointers[num].close()

				if total_words_till_now >= threshold:
					writeToFile(inverted_index)
					total_words_till_now = 0
					inverted_index.clear()

	writeToFile(inverted_index)
	writeSecIndex()

def deleteTempIndexFiles():
	for filename in temp_index_files:
		os.remove(filename)
	os.remove(path_to_temp_index_files)


path_to_temp_index_files = "./tempIndexedFiles"
path_to_merged_index_folder = "mergedIndexedFiles"
path_to_secondary_file =  "./secIndex.txt"

threshold = 50000

temp_index_files = glob("./tempIndexedFiles/*")
num_inverted_index = 0
filenum = 1


try:
	os.mkdir(path_to_merged_index_folder)
	print("folder created!!")
except:
	print ("path_to_merged_index_folder already exists..!! chillaxx")



mergeKFiles()

# deleteTempIndexFiles()
with open("stats.txt", "w", encoding="utf-8") as stats_file :
	stats_file.write(str(filenum-1) + "\n" + str(num_inverted_index))

""" 
os.remove all temp files
word_pos_dict in sagnik code for faster search
"""
# main()
# python merge.py
