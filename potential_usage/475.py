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

def setKeyWord():
    key_value = input('enter the key word:\n')
    KEY_WORD = key_value
    print('now keyword is: '+ KEY_WORD +'\n')
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

    texts = bdata.abstract

    dictionary = corpora.Dictionary([texts])
    feature_cnt = len(dictionary.token2id.keys())
    corpus = [dictionary.doc2bow([text]) for text in texts]
    tfidf = models.TfidfModel(corpus)
    kw_vector = dictionary.doc2bow(seg_sentence(KEY_WORD, stop_words))
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
    sim = index[tfidf[kw_vector]]

    result_list = []
    for i in range(len(sim)):
        score = score + sim[i]
    bdata.set_score(score)


#-----------------------------main---------------------------------------

work_dir = 'bib_collect/'
#list of instances of BibData
bibinfo = []
print('loading data...')
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        with open(work_dir+filename) as bibfile:
            if 'bib' not in filename:
                continue
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bibdata = bp.load(bibfile, parser = parser)
            for e in bibdata.entries:
                tmpBib = BibData(e)
                bibinfo.append(tmpBib)

print('\nsuccessfully loading data\n')

setKeyWord()
for bdata in bibinfo:
    calScore(bdata)
bibinfo.sort(key=lambda x:x.abstract)
for bdata in bibinfo:
    print(bdata.abstract)
