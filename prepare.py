




#pdf plumber
#csv.preview
import pandas as pd
#import unicode character database
import unicodedata
#import regular expression operations
import re

#import natural language toolkit
import nltk


#import our aquire
from acquire import *


#import our stopwords list
from nltk.corpus import stopwords
from copy import deepcopy






def split_apply_join(funct,listobj):
    'helperfuction letters'

    mapped=map(funct, listobj)
    mapped=list(mapped)
    mapped=''.join(mapped)
  
    return mapped






def stopfilter(text,stop_words_extend_reduce=["'"]):
    'we use symmetric difference so if a is already in stop words then it will be added to our third set else our third set will be missing it'
    #create oujr english stopwords list

    stops = set(stopwords.words('english'))
    stop_words_extend_reduce=set(stop_words_extend_reduce)
    stops=stops.symmetric_difference(stop_words_extend_reduce)

    # stops=(stops|stop_words_extend)-exclude_words
    #another way
    
    filtered=list(filter((lambda x: x not in stops), text.split()))
    filtered=' '.join(filtered)

    return filtered









def basic_clean(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''   
    Filters out all special characters if you need to edit then supply a new regex filter 
    
    
    
    
    '''
    #make a copy and begin to transform it
    newtext = text.lower()

    #encode into ascii then decode
    newtext = unicodedata.normalize('NFKD', newtext)\
    .encode('ascii', 'ignore')\
    .decode('utf-8')

    #use re.sub to remove special characters
    newtext = re.sub(fr'{regexfilter}', '', newtext)

    return newtext

 


def tokenizer(text,regexfilter=r'[^a-z0-9\'\s]'):
    ''' 
    For a large file just save it locally
    
    
    
    
    
    '''
    newtext=basic_clean(text,regexfilter=regexfilter)
    #make ready tokenizer object
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use the tokenizer
    newtext = tokenize.tokenize(newtext, return_str=True)
    return newtext





    
    
    
    


def stemmed(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''    
    Takes text, tokenizes it, stems it
    
    
    
    
    
    '''
    #make ready porter stemmer object
    newtext=tokenizer(text,regexfilter=regexfilter)
    ps = nltk.porter.PorterStemmer()
    stemmedlist=split_apply_join(ps.stem,newtext)
    return stemmedlist




def lemmatizor(text,regexfilter=r'[^a-z0-9\'\s]'):
    '''    
    
      Takes text, tokenizes it, lemmatizes it
    
    
    
    
    
    '''

    #make ready the lemmatizer object
    newtext=tokenizer(text,regexfilter=regexfilter)
    wnl = nltk.stem.WordNetLemmatizer()
    lemmatized=split_apply_join(wnl.lemmatize,newtext)
    return lemmatized



def dictlist_lemmatizor_else_stemmer(dictlistog,regexfilter=r'[^a-z0-9\'\s]',stop_words_extend_reduce=["'"],lemmatize=True):
    ''' 
        
        
        
        
        #   Stem or Lemmatize 
        # if file is large and resources are scarce stem otherwise you can expect better performace from lemmatize
    '''
    dictlist=deepcopy(dictlistog)
    if lemmatize==True:
        for i in range(0,len(dictlist)):
            keys=dictlist[i].keys()
            for k in keys:
                text=dictlist[i].get(k)
                lemmatized=lemmatizor(text,regexfilter)
                stopfilteredlemitezed=stopfilter(lemmatized,stop_words_extend_reduce=stop_words_extend_reduce)
                dictlist[i].update({k:stopfilteredlemitezed})
    else:
        for i in range(0,len(dictlist)):
            keys=dictlist[i].keys()
            for k in keys:
                text=dictlist[i].get(k)
                stem=stemmed(text,regexfilter)
                stopfilteredstem=stopfilter(stem,stop_words_extend_reduce=stop_words_extend_reduce)
                dictlist[i].update({k:stopfilteredstem})
    return dictlist




# def dictlist_super_NLP_comp(dictlist,regexfilter=r'[^a-z0-9\'\s]',stop_words_extend_reduce=["'"],interestingkeys=[]):
#     ''
#     ndictlist=deepcopy(dictlist)
#     for i in range(0,len(ndictlist)):            
            
#             for a in range(0,len(interestingkeys)):
#                 k=interestingkeys[a]
#                 text=dictlist[i].get(k)
#                 ndictlist[i].pop(k)
#                 ndictlist[i].update({f'{k}_org':text})
#                 clean=basic_clean(text,regexfilter=regexfilter)
#                 ndictlist[i].update({f'{k}_cleaned':clean})
#                 lemmatized=lemmatizor(text,regexfilter)
#                 stopfilteredlemitezed=stopfilter(lemmatized,stop_words_extend_reduce=stop_words_extend_reduce)
#                 ndictlist[i].update({f'{k}_lemmatized':stopfilteredlemitezed})
#                 stem=stemmed(text,regexfilter)
#                 stopfilteredstem=stopfilter(stem,stop_words_extend_reduce=stop_words_extend_reduce)
#                 ndictlist[i].update({f'{k}_stemmed':stopfilteredstem})                 
               

#     a=pd.DataFrame(ndictlist[0],columns=list(ndictlist[0].keys()),index=[0])
#     for i,s in enumerate(ndictlist):
#         b=pd.DataFrame(s,columns=list(s.keys()),index=[i])
#         a=pd.merge(a,b,how='outer',right_index=False,left_index=False)
#     df=a  
       
#     return df

    
 




def dictlist_super_NLP_comp(dictlist,regexfilter=r'[^a-z0-9\'\s]',stop_words_extend_reduce=["'"]):
    ''
    ndictlist=deepcopy(dictlist)
    mapper=[]
    interestingkeys=list(ndictlist.keys())
    for i in range(0,len(ndictlist)):           
            k=interestingkeys[i]
            text=ndictlist.get(k)         
            org={f'org':text}
            clean=basic_clean(text,regexfilter=regexfilter)
            cleaned=({f'cleaned':clean})
            lemmatized=lemmatizor(text,regexfilter)
            stopfilteredlemitezed=stopfilter(lemmatized,stop_words_extend_reduce=stop_words_extend_reduce)
            lemma={f'lemmatized':stopfilteredlemitezed}
            stem=stemmed(text,regexfilter)
            stopfilteredstem=stopfilter(stem,stop_words_extend_reduce=stop_words_extend_reduce)
            stemma={f'stemmed':stopfilteredstem}
            mapper.append({k:dict(**org,**cleaned,**lemma,**stemma)})

    
 
                
               


  
       
    return mapper