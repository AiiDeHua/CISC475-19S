# coding = utf-8
import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import os, shutil
import jieba
import jieba.posseg as pseg
from gensim import corpora, models, similarities

#-------------------------global variable-----------------------------------
KEY_WORD = ''
#list of instances of BibData
bibinfo = []
#list of instances that to output
extractList = []

#-------------------------function define-----------------------------------

#return a whole string
def entry_to_string(entry):
	result = '@Article{\n'
	for key in entry:
		if(key == 'title' or key == 'abstract'):
			result = '	' + result + str(key)+'=['+str(entry[key])+']\n'
		else:
			result = '	' + result + str(key)+'='+str(entry[key])+'\n'
		resulr = result + '\n' 
	return result

#return a string list
def entry_to_stringList(entry):
	result = []
	result.append('@Article{\n')
	for key in entry:
		if(key == 'title' or key == 'abstract'):
			result.append( '	' + str(key)+'=['+str(entry[key])+']'+'\n')
		else:
			result.append( '	' + str(key)+'='+str(entry[key])+'\n')
		result.append('\n')
	return result

def setKeyWord():
	keyword_dir = 'search/search.txt'
	with open(keyword_dir, 'r', encoding='utf-8') as f:
		KEY_WORD = f.read()
		print('now keyword is: '+ KEY_WORD +'\n')
	

def exportBib(BibList):
	output_dir = 'output/output.bib'
	#with open(keyword_dir, 'w+') as f:
		#for b in BibList:
			#f.write(b.text)
			#print('WRITE: '+ b.title +'\n')
	fs = open(output_dir, 'w', encoding='utf-8')
	for b in BibList:
		fs.write(entry_to_string(b.text))
		print('WRITE: '+ b.title +'\n')
	fs.close()


def selectExport():
	extractList.clear()
	single_export_flag = 0
	total_export_flag = input('manually select to export bib file(enter 1) or export all inut bib file with sorted(enter 0)\n')
	if total_export_flag > 0:
		for b in bibinfo:
			print('Title:	'+b.title+'\n')
			print('Abstract:	'+b.abstract+'\n\n')
			single_export_flag = input('choose this bib(enter 1) or not(enter 0)\n')
			if single_export_flag > 0:
				extractList.append(b)
		exportBib(extractList)
	else:
		exportBib(bibinfo)

#-------------------------definition----------------------------------------
# a class saves bib
class BibData:
    text = ''
    title = ''
    score = 0
    abstract = []
    
    '''
    def __init__(self, tex, tle, s, abst):
        self.text = tex
        self.title = tle
        self.score = s
        self.abstract = abst

    def __init__(self, tex, tle, abst):
        self.text = tex
        self.title = tle
        self.score = 0
        self.abstract = abst'''   

    def __init__(self, entry):
        self.text = entry
        self.title = entry['title']
        self.score = 0
        try:
            entry['abstract']
        except Exception:
            self.abstract.append(entry['title'])
        else:
            self.abstract = entry['abstract'].split("\\\\")
        
    def set_score(self, s):
        self.score = s
        
    def set_title(self, t):
        self.title = t
    
    def set_abstract(self, abst):
        self.abstract = abst
    
    def sort_key(self):
        return self.abstract

#--------------------------get similarity score-----------------------
def StopWordsList(filepath):
    wlst = [w.strip() for w in open(filepath, 'r', encoding='utf8').readlines()]
    return wlst
        
        
def StopWordsList(filepath):
    wlst = [w.strip() for w in open(filepath, 'r', encoding='utf8').readlines()]
    return wlst


def seg_sentence(sentence, stop_words):
    # stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']#过滤数字m
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'f', 'r']
    sentence_seged = pseg.cut(sentence)
    # sentence_seged = set(sentence_seged)
    outstr = []
    for word,flag in sentence_seged:
        # if word not in stop_words:
        if word not in stop_words and flag not in stop_flag:
            outstr.append(word)
    return outstr

#input a Bibdata type
#set score to this Bibdata
def calScore(bdata):
    spPath = 'stopwords.txt'
    score = 0
  
    stop_words = StopWordsList(spPath)

    # 1、将【文本集】生产【分词列表】
    texts = bdata.abstract

#一、建立词袋模型
    # 2、基于文件集建立【词典】，并提取词典特征数
    dictionary = corpora.Dictionary([texts])
    feature_cnt = len(dictionary.token2id.keys())
    #feature_cnt = len(dictionary.token2id)
    # 3、基于词典，将【分词列表集】转换为【稀疏向量集】，也就是【语料库】
    corpus = [dictionary.doc2bow([text]) for text in texts]
    # 4、使用“TF-TDF模型”处理【语料库】
#二、建立TF-IDF模型
    tfidf = models.TfidfModel(corpus)
#三构建一个query文本，利用词袋模型的字典将其映射到向量空间
    # 5、同理，用词典把搜索词也转换为稀疏向量
    #kw_vector = dictionary.doc2bow(lcut(KEY_WORD))
    kw_vector = dictionary.doc2bow(seg_sentence(KEY_WORD, stop_words))
    # 6、对稀疏向量建立索引
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
    # 7、相似的计算
    sim = index[tfidf[kw_vector]]

    result_list = []
    for i in range(len(sim)):
        #print('keyword 与 text%d 相似度为：%.2f' % (i + 1, sim[i]))
        #if sim[i] > score:
        #    result_list.append(orig_txt[i])
        score = score + sim[i]
        #result_list.append(orig_txt[i])
    #print(score)
    bdata.set_score(score)
    #print('原始的句子：',result_list)


#-----------------------------main---------------------------------------

work_dir = 'bib_collect/'
print('loading data...')
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        if '.bib'in filename:
            with open(work_dir+filename, 'r', encoding='utf-8') as bibfile:
                parser = BibTexParser()  # 声明解析器类
                parser.customization = convert_to_unicode  # 将BibTeX编码强制转换为UTF编码
                bibdata = bp.load(bibfile, parser = parser)  # 通过bp.load()加载
				# 输出作者和DOI
				#print(bibdata.entries[0]['abstract'].split("\\\\"))
				# put entries into bibdata list
                for e in bibdata.entries:
                    tmpBib = BibData(e)
                    bibinfo.append(tmpBib)


print('\nsuccessfully loading data\n')

#print(len(bibinfo[0].abstract))
#for b in bibinfo:
    #print(b.title + ': ',b.score, '\n')

setKeyWord()
for bdata in bibinfo:
    calScore(bdata)

bibinfo.sort(key=lambda x:x.score)


#for b in bibinfo:
    #print(b.title + ': ',b.score, '\n')

#selectExport()
exportBib(bibinfo)



    
