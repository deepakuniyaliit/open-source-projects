import sys
import os
import Stemmer
import timeit
from math import log10
import re
from collections import defaultdict
from bisect import bisect


def loadDocToTitle(path_to_doc_to_title):
	global num_docs
	with open(path_to_doc_to_title, "r", encoding = "utf-8") as f:
		for line in f:
			num_docs += 1
			id_title = line.split("#")
			docToTitle[id_title[0]] = id_title[1]
	

def loadStopwords(path_to_stopwords_file):
	try :
		file = open(path_to_stopwords_file, "r", encoding = "utf-8")
		for line in file:
			words = line.strip()
			stopwords.add(words)
	except:
		print("file containing stopwords not found.\n Exiting system")
		sys.exit(1)


def loadSecondaryIndexFile(path_to_sec_index_file):
	with open(path_to_sec_index_file, "r", encoding = "utf-8") as f:
		for line in f:
			sec_index.append(line.split()[0])


def search(query, out_file):
	isFieldQuery = False
	for tag in tags:
		if tag in query:
			isFieldQuery = True
			break

	print ("isFieldQuery ", str(isFieldQuery) +"\n")
	parse(query, isFieldQuery, out_file)




def postingListOfWord(word):
	word_pos = bisect(sec_index, word)
	if word_pos>=1 and sec_index[word_pos-1]==word:
		if word_pos!=1:
			word_pos -= 1
		if word_pos+1==len(sec_index) and sec_index[word_pos]==word:
			word_pos += 1
	
	index_file = path_to_merged_index_folder + "index" + str(word_pos) + ".txt"
	posting_list = []
	# print(word, " present in ", word_pos, "\n")
	with open(index_file, 'r', encoding='utf-8') as f:
		all_lines = f.readlines()
		low=0
		high = len(all_lines)
		mid = 0
		while high >= low:
			mid = int((low+high)/2)
			curr_line_word = all_lines[mid].split(":")[0]
			if curr_line_word==word:
				posting_list = all_lines[mid].split(":")[1].split(",")
				break
			elif curr_line_word < word:
				low = mid+1
			else:
				high = mid-1
	return posting_list



def processQuery(text):

	reg = re.compile(r'[^\x00-\x7F]+', re.DOTALL)
	text = reg.sub(' ', text)
	reg = re.compile(r'[.,;_()"/\']', re.DOTALL)
	text = reg.sub(' ', text)	

	text = text.split()

	tokens = []
	for word in text:
		reg = re.compile(r'[\ \.\-\:\&\$\!\*\+\%\,\@]+', re.DOTALL)
		word = reg.sub('', word)
		word = stemmer.stemWord(word)
		word = word.lower()

		if len(word)>2 and word.isalpha and word not in stopwords:
			tokens.append(word)

	return tokens


# def writeOutputToFile(ranking_docs):
	
	
def calculate_score(posting_list, num_docs_in_posting_list):
	# ranking_docs = {}
	for info in posting_list:
		docID, fieldInfo = info.split("-")
		fieldFreq = fieldInfo.split("|")

		tf = 0
		for tag_freq in fieldFreq:
			tag = tag_freq[0]
			freq = int(tag_freq[1:])
			tf += (freq * tag_weights[tag])

		idf = log10(num_docs/ num_docs_in_posting_list)
				
		ranking_docs[docID] += (float(log10(1+tf))*float(idf))
	return ranking_docs


def  parse(query, isFieldQuery, out_file):
	
	
	start = timeit.default_timer()
	ranking_docs = defaultdict(int)
	# normal query
	if isFieldQuery==False:
		tokens = processQuery(query)
		print ("normal : ",  tokens , "\n")
		for word in tokens:
			posting_list = postingListOfWord(word)
			#print ("positn list : ", posting_list, "\n")
			num_docs_in_posting_list = len(posting_list)
			
			for info in posting_list:
				docID, fieldInfo = info.split("-")
				fieldFreq = fieldInfo.split("|")

				tf = 0
				for tag_freq in fieldFreq:
					tag = tag_freq[0]
					freq = int(tag_freq[1:])
					tf += (freq * tag_weights[tag])

				idf = log10(num_docs/ num_docs_in_posting_list)
				
				ranking_docs[docID] += (float(log10(1+tf))*float(idf))
				#print("tf : ", tf)
				#print("\nidf : ", idf)
				#print("\nrankinfg odcs : ", docID, " ", ranking_docs[docID], "\n" )
		
		
	# field query
	else:
		field_indexes = []

		for tag in tags:
			ind = query.find(tag)
			if ind!=-1:
				field_indexes.append(ind)
		field_indexes.append(len(query)+1)

		num_tags = len(field_indexes)-1
		tag_tokens = []

		for i in range(num_tags):
			q = query[field_indexes[i]:field_indexes[i+1]-1]
			q = q.strip().split(":")
			tag = q[0]
			#print ("tag found : ", tag)
			if tag not in fields:
				print ("wrong tag\n")
				sys.exit()
			tokens = q[1].strip().split()

			for token in tokens:
				token = re.sub(r'[^\x00-\x7F]+','', token)
				token = token.lower()
				token = stemmer.stemWord(token)
				if len(token)>2 and token.isalnum() and token not in stopwords:
					tag_tokens.append((tag, token))

		#ranking_docs = defaultdict(int)
		print ("field : ", tag_tokens, "\n")
		for (tag, token) in tag_tokens:
			posting_lists_all = postingListOfWord(token)
			posting_lists_of_given_tag = []
			for field_info in posting_lists_all:
				if tag in field_info:
					posting_lists_of_given_tag.append(field_info)

			if len(posting_lists_of_given_tag) <= 1:
				posting_lists_of_given_tag = posting_lists_all
			#print ("positn list : ", posting_lists_of_given_tag, "\n")	
			num_docs_in_posting_list = len(posting_lists_of_given_tag)
			
			for info in posting_lists_of_given_tag:
				docID, fieldInfo = info.split("-")
				fieldFreq = fieldInfo.split("|")

				tf = 0
				for tag_freq in fieldFreq:
					tag = tag_freq[0]
					freq = int(tag_freq[1:])
					tf += (freq * tag_weights[tag])

				idf = log10(num_docs/ num_docs_in_posting_list)
				
				ranking_docs[docID] += (float(log10(1+tf))*float(idf))
				#print("tf : ", tf)
				#print("\nidf : ", idf)
				#print("\nrankinfg odcs : ", docID, " ", ranking_docs[docID], "\n" )
		
	
	docid_score = sorted(ranking_docs.items(), key=lambda item: item[1], reverse=True)[0:10]
	#print ("docid_score docs : ", docid_score)
	for item in docid_score:
		docID, score = item
		#print ("docs : ", docToTitle[docID])
		
		out_file.write(str(docID)+","+str(docToTitle[docID]))
	end = timeit.default_timer()
	out_file.write(str(end - start)+" sec\n\n")

if __name__ == "__main__":

	path_to_query_file = "./queries.txt"
	path_to_doc_to_title = "./docToTitle.txt"
	path_to_stopwords_file = "./all_stopwords.txt"
	path_to_sec_index_file = "./secIndex.txt"
	path_to_merged_index_folder = "./mergedIndexedFiles/"

	stopwords = set()
	loadStopwords(path_to_stopwords_file)

	sec_index = []
	loadSecondaryIndexFile(path_to_sec_index_file)

	docToTitle = {}
	num_docs = 0
	loadDocToTitle(path_to_doc_to_title)
	stemmer = Stemmer.Stemmer('english')
	fields = ['t', 'b', 'c', 'i', 'r', 'e']
	tags = ['t:', 'b:', 'c:', 'i:', 'r:', 'e:']
	tag_weights = {'t': 1000,'b': 1,'i': 50,'c': 50,'r': 50,'e': 50}


	out_file = open("queries_op2.txt", "w+", encoding="utf-8")

	with open(path_to_query_file, "r") as f:
		#print ("file opened")
		for query in f:
			print ("query : ", query + "\n")
			search(query, out_file)

	out_file.close()

# main()

# python search_ritvik.py
