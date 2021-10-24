import Stemmer
import sys
import re
import xml.sax
import timeit
import os


class WikiSearchEngine(xml.sax.ContentHandler):
	def __init__(self):
		self.currData = ""
		self.docID = 0
		self.title = ""
		self.text = ""

	def startElement(self, tag, attributes):
		self.currData = tag
		# self.title = ""
		# self.text = ""

	def endElement(self, tag):
		if tag == "page":
			self.docID += 1
			processTags(self)
			# print("end elemenet title : ", self.title)
			# documentTitleMapping.write(str(self.docID)+":"+self.title.strip()+"\n")
			try :
			    documentTitleMapping.write(str(self.docID)+"#"+self.title.strip() + "\n")
			except:
				documentTitleMapping.write(str(self.docID)+"#"+ str(self.title.strip().encode('utf-8'))+"\n")
			self.title = ""
			self.text = ""

	def characters(self, text):
		if self.currData == "title":
			self.title += text
		if self.currData == "text":
			self.text += text


def removeNonAlphabets(data):
	data = re.sub(r"[~`!@#$%-^*+{\[}\]\|\\<>/?]",'', data)
	return data

def create_tokens(content):
	content = ' '.join(content)
	content = removeNonAlphabets(content)
	content = content.split()
	return content

def processTags(obj):
	title = obj.title
	docID = obj.docID
	content = obj.text
	#print("content : ", content)
	#sys.exit(1)

	processTitle(title, docID)
	processContent(content, docID)

def processTitle(title, docID):
	# datapreprocessing
	title = title.lower()
	##
	title_words = title.split()

	create_inverted_index(title_words, docID, "t", True)


def create_inverted_index(words, docID, tag, isTitle = False):
	global num_tokens
	num_tokens += len(words)

	for word in words:
		word = word.strip()
		if(len(word)<=2 or len(word)>20 or word in stopwords or word.isnumeric() or word.isalpha()==False):
			continue

		if isTitle==False:
			word = stemmer.stemWord(word)

		#if word in stopwords:
			#continue

		if word not in inverted_index:
			inverted_index[word] = {}

		if docID not in inverted_index[word]:
			inverted_index[word][docID] = {}

		if tag not in inverted_index[word][docID]:
			inverted_index[word][docID][tag] = 1
		else:
			inverted_index[word][docID][tag] += 1


def clean_content(content):
	content = content.lower()
	content = re.sub(r'<(.*?)>', '', content)
	content = re.sub(r'[^\x00-\x7F]+','', content)
	content = re.sub(r'[.,;_()/\"\'\=]', '', content)
	content = re.sub(r'<(.*?)>', '', content)
	content = re.sub(r'[^\x00-\x7F]+', '', content)
	#content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
	# regex sub
	# print ("conetnt \n\n\n\n\n")
	return content


def write_inverted_index_to_file(path_to_inverted_index_file):
	#print ("writeing to file \n")

	# word:docid-t1|i2|r4,docid-c2....
	f = open(path_to_inverted_index_file, 'w', encoding='utf-8')

	#inverted_index_sorted = sorted(inverted_index.iteritems())
	for word, val in sorted(inverted_index.items()):
		text = str(word) + ":"
		for docID, val in sorted(val.items()):
			text += str(docID) + "-"
			for tag, freq in val.items():
				text += (str(tag)+str(freq)+"|")
			text = text[:-1]+","
		f.write(text[:-1]+"\n")
	f.close()


def write_stat_file(path_to_inverted_index_stat):
	f = open(path_to_inverted_index_stat, "w", encoding="utf-8")
	text = str(num_tokens) +"\n" + str(num_inverted_index_tokens)
	f.write(text)
	f.close()


def add_infobox_index(content, docID):
	text = content.split("{{infobox")
	info_tokens = []
	if len(text) <= 1:
		return info_tokens
	#for i in range(1,len(text)):
	lines = text[1].split("\n")	
	for line in lines:
		if line=="}}":
			break	
		info_tokens += (tokenize(line))

	#print ("info tokens info : ", info_tokens)
	create_inverted_index(info_tokens, docID, "i")
		
			

def add_references_index(content, docID):
	ref = []
	ref = re.findall(r'== ?references ?==(.*?)==', content, re.DOTALL)
	ref_tokens = create_tokens(ref)
	content = re.sub(r'== ?references ?==(.*?)==', '', content)
	#print("refs tokesn : ", ref_tokens)
	create_inverted_index(ref_tokens, docID, "r")
	return content


def add_categories_index(content, docID):
	cat = re.findall(r'\[\[category:(.*?)\]\]', content, re.MULTILINE)
	cat_tokens = create_tokens(cat)
	#print(" cat_tokens : ", cat_tokens)
	content = re.sub(r'\[\[category:(.*?)\]\]', '', content)
	create_inverted_index(cat_tokens, docID, "c")
	return content
	

def add_body_index(content, docID):
	body_tokens = tokenize(content)
	create_inverted_index(body_tokens, docID, "b")

def tokenize(text):
    tokens = re.split(r'[^A-Za-z0-9]+', text)
    return tokens

def add_external_links_index(content, docID):
	text = content.split("==external links==")
	ext_links_tokens = []
	
	#sys.exit(1)
	if len(text) <= 1:
		return ext_links_tokens	

	lines = text[1].split("\n")
	for line in lines:
		if line and line[0] == '*':
			#ref_tokens = create_tokens(ref)
			ext_links_tokens += tokenize(line)
		else:
			break
	####
	#print("external links tokesn : ", ans)
	create_inverted_index(ext_links_tokens, docID, "e")



def processContent(content, docID):
	global curr_file_num, max_page_limit, num_inverted_index_tokens
	# Title, Infobox, Body, Category, Links and Reference
	cleanContent = clean_content(content)
	
	# infobox
	add_infobox_index(cleanContent, docID)

	# references
	cleanContent = add_references_index(cleanContent, docID)

	#categories
	cleanContent = add_categories_index(cleanContent, docID)

	# external links
	add_external_links_index(cleanContent, docID) 

	# body
	add_body_index(cleanContent, docID)

	if(docID%1000==0):
		print(docID, " pages read\n")

	if(docID%max_page_limit==0):
		print ("limtt erached \n\n\n")
		filepath = getFilename(path_to_inverted_index_dir, curr_file_num)
		curr_file_num += 1
		write_inverted_index_to_file(filepath)
		num_inverted_index_tokens += len(inverted_index)
		inverted_index.clear()

		


def getFilename(path_to_inverted_index_dir, filenum):
	return path_to_inverted_index_dir + "/index_" + str(filenum) + ".txt"

if __name__ == "__main__":

	startTime = timeit.default_timer()
	if len(sys.argv) != 4:
		print ("Wrong number of argumnets..!!")
		sys.exit(1)

	stemmer = Stemmer.Stemmer('english')
	#stopwords = stopwords.words('english')
	#"""
	stopwords = set()
	stopwords_filename = "all_stopwords.txt"
	try :
		file = open(stopwords_filename, "r", encoding = "utf-8")
		for line in file:
			words = line.strip()
			stopwords.add(words)
	except:
		print("file containing stopwords not found.\n Exiting system")
		sys.exit(1)
	#"""

	path_to_wiki_dump = sys.argv[1]
	path_to_inverted_index_dir = sys.argv[2]
	path_to_inverted_index_stat =  sys.argv[3]

	try:
		os.mkdir(path_to_inverted_index_dir)
	except FileExistsError:
		print("Directory for inverted index already created")

	path_to_inverted_index_file = path_to_inverted_index_dir + "/inverted_index2.txt"

	max_page_limit = 10000
	inverted_index = {}
	num_tokens = 0
	num_inverted_index_tokens = 0
	curr_file_num = 1

	documentTitleMapping = open("docToTitle.txt", "w")

	wikiSearchEngine = WikiSearchEngine()
	parser = xml.sax.make_parser()
	parser.setContentHandler(wikiSearchEngine)
	parser.parse(path_to_wiki_dump)

	if (len(inverted_index)!=0):
		print ("abhi bacha hai\n")
		filepath = getFilename(path_to_inverted_index_dir, curr_file_num)
		curr_file_num += 1
		write_inverted_index_to_file(filepath)
		num_inverted_index_tokens += len(inverted_index)
		inverted_index.clear()

	num_index_files = curr_file_num-1
	#print("inverted index : ", inverted_index)

	# write_inverted_index_to_file(path_to_inverted_index_file)
	# write_stat_file(path_to_inverted_index_stat)

# python indexer.py wiki-dump-1-test.xml tempIndexedFiles stats2.txt
	documentTitleMapping.close()

# trial1 : 25521434
# 378599
# remove tags ==name== etc
# try spimi, bm-25/+

# bash inverIndex.sh wiki-dump-1-test.xml tempIndexedFiles stats3.txt

# bash inverIndex.sh enwiki-20210720-pages-articles-multistream.xml tempIndexedFiles stats3.txt
# bash inverIndex.sh enwiki-latest-pages-articles17.xml-p23570393p23716197 tempIndexedFiles stats3.txt	