from nltk import *
from nltk.stem.porter import *
import contractions
import sys
import json

def mainprog():

    if os.path.exists(r"C:\Users\Tariq Shahzad\PycharmProjects\pythonProject2\invertedindex.json"):
        with open('invertedindex.json', 'r') as openfile:
            # Reading from json file
            finalinverted = json.load(openfile)
        with open('positionalindex.json', 'r') as openfile:
            # Reading from json file
            finalpositional = json.load(openfile)
    else:
        finalinverted = invertedindexing(1)
        json_object = json.dumps(finalinverted)
        with open("invertedindex.json", "w") as fileobj:
            fileobj.write(json_object)

        finalpositional = positionalindexing(2)
        json_object = json.dumps(finalpositional)
        with open("positionalindex.json", "w") as fileobj:
            fileobj.write(json_object)

    while(1):
        print("Enter 1 for inverted index and 2 for positional index or any key to exit.")
        userinput = input()
        if userinput=="1":
            queryinvertedsearch(finalinverted)
        elif userinput=="2":
            querysearch(finalpositional)
        else:
            sys.exit()

def invertedindexing(userinput):
    invertedindex=preprocessing(userinput)              #preparing dictionary
    return(invertedindex)

def positionalindexing(userinput):
    positionalindex = preprocessing(userinput)
    positionalindex = populatingindex(positionalindex)     #inserting documents word positions
    return(positionalindex)

def populatingindex(positionalindex):

    punc = '''!‘()[]{};:'"\,<>./?@#$%^&*_~“”’'''

    stoplist=['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are',
             'has','have','had','up','his','her','in','on','no','we','do']

    for i in range(1,51):              #traversing through each file
        filenum=i
        filename=str(i)+".txt"

        f=open(filename,"rt",encoding='utf-8')
        document=f.read()
        f.close()

        expanded_words = []

        for word in document.split():          #using contractions to rephrase shortened words
            expanded_words.append(contractions.fix(word))

        text = ' '.join(expanded_words)

        result=text.replace("—", " ")

        no_punct = ""            #removing punctuation marks
        for char in result:
            if char not in punc:
                no_punct = no_punct + char

        words = word_tokenize(no_punct)         #tokenizing document
        document = [word.lower() for word in words]

        stemmer = PorterStemmer()               #applying stemming on tokenized document
        document = [stemmer.stem(plural) for plural in words]

        for j in range(len(document)):       #traversing through whole tokenized document
            word=document[j]
            tempdict = {}
            if word in stoplist:
                continue
            elif word in positionalindex.keys():        #if word found in the dictionary key
               if not bool(positionalindex[word].get(filenum)):   #to check if a particular doc id is not already present in the postinglist as a key
                   tempdict[filenum] = [j]
                   positionalindex[word].update(tempdict)
               else:
                   if filenum in positionalindex[word].keys():    #to check if a particular doc id is already present in the postinglist as a key
                       positionalindex[word][filenum].append(j)
            else:
                pass
    return positionalindex         #return the populated positional dictionary

def preprocessing(userinput):       #a function that preprocesses all the document to get terms for dictionary
    finaldict={}
    posidict={}

    punc='''!‘()[]{};:'"\,<>./?@#$%^&*_~“”’'''

    stoplist = ['a', 'is', 'the', 'of', 'all', 'and', 'to', 'can', 'be', 'as', 'once', 'for', 'at', 'am', 'are',
                'has', 'have', 'had', 'up', 'his', 'her', 'in', 'on', 'no', 'we', 'do']

    for i in range(1,51):      #traversing through each file
        filenum=i
        filename=str(i)+".txt"
        f=open(filename,"rt",encoding='utf-8')
        corpus=f.read()
        f.close()

        expanded_words = []

        for word in corpus.split():              #using contractions to rephrase shortened words
            expanded_words.append(contractions.fix(word))

        text = ' '.join(expanded_words)

        result = text.replace("—"," ")

        no_punct =""                #removing punctuation marks from document
        for char in result:
            if char not in punc:
                no_punct=no_punct + char

        words=word_tokenize(no_punct)           #tokenizing the document
        words=[word.lower() for word in words]

        stemmer = PorterStemmer()             #applying stemming on each tokenized document word
        words= [stemmer.stem(plural) for plural in words]

        cont = list(dict.fromkeys(words))    #getting unique words to be added as dictionary keys

        finallist=[]      #finalized words for indexing

        for i in range(len(cont)-1):
            if cont[i] in stoplist:
                continue
            else:
                finallist.append(cont[i])

        finallist=sorted(finallist)
        if userinput==1:
            finaldict=devdict(finallist,filenum,finaldict)       #developing dictionary for inverted index
        else:
            posidict=develope_dict(finallist,posidict)          #developing dictionary for positional index

    if bool(finaldict):
        return finaldict         #return inverted index dictionary
    else:
        return posidict          #return positional index dictionary

def devdict(indexes,num,finaldict):         #function to develope inverted indexes dictionary

    mydict={}

    for i in range(len(indexes)-1):
        mydict[indexes[i]] = [num]         #number file ka

    if not(bool(finaldict)):             #creating dictionary for inverted index document by document
        finaldict=mydict

    else:
        for i in mydict.keys():
            if i in finaldict.keys():          #if dictionary word exists it will append the doc ids against the dictionary term
                finaldict[i].append(num)
            else:
                finaldict[i]=[num]
    return finaldict

def develope_dict(indexes,posidict):          #function to develope positional index dictionary

    mydict={}

    for i in range(len(indexes)-1):        #creating dictionary for positional index document by document
        mydict[indexes[i]] = {}

    if not(bool(posidict)):
        posidict=mydict
    else:
        for i in mydict.keys():           #if dictionary word exists it will append the doc ids against the dictionary term
            if i in posidict.keys():
                continue
            else:
                posidict[i]= {}
    return posidict

def not_items(list1):        #a function to get not of given doc ids

    filelist=[*range(1, 51, 1)]
    reslist=[]
    for f in range(len(filelist)):
        if filelist[f] in list1:
            continue
        else:
            reslist.append(filelist[f])
    return reslist

def queryinvertedsearch(invertedindex):      #a function which is called when a user needs to query inverted index

    print("Enter your query for inverted index search")
    userquery=input()
    l1 = userquery.lower()
    l2 = l1.split(' ')

    wordlist=[]
    notlist=[]
    operatorlist=[]
    result=[]
    not_flag=0
    stemmer = PorterStemmer()

    for i in range(len(l2)):          #here we are segmenting the list of query terms
        if l2[i]=="and" or l2[i]=="or" or l2[i]=="not":
            if l2[i]=="not":
                not_flag=1
            else:
                operatorlist.append(l2[i])
        else:
            if not_flag==1:            #using flag to identify not words accurately
                l2[i]=stemmer.stem(l2[i])        #applying stemmer on queried words
                wordlist.append(l2[i])
                notlist.append(1)
                not_flag=0
            else:
                l2[i] = stemmer.stem(l2[i])      #applying stemmer on queried words
                wordlist.append(l2[i])
                notlist.append(0)

    i=0
    partiallist=[]
    templist=[]
    while i< len(wordlist):      #here we are storing dictionary terms doc ids as a list to perform AND OR NOT operations
        if notlist[i]==1:
            if wordlist[i] in invertedindex.keys():
                partiallist.append(not_items(invertedindex[wordlist[i]]))
            else:
                filelist = [*range(1, 51, 1)]
                partiallist.append(filelist)
        else:
            if wordlist[i] in invertedindex.keys():
                partiallist.append(invertedindex[wordlist[i]])
            else:
                partiallist.append([])
        i=i+1

    if len(wordlist)==1 and notlist[0]==0:
        result=partiallist[0].copy()
    elif not bool(operatorlist) and notlist[0]==1:
        result = partiallist[0].copy()

    else:
        for i in range(len(operatorlist)):
            if not bool(templist):         #if templist is empty we can store intermediate result
                if operatorlist[i] == 'and':
                    templist.append(list(set(partiallist[i]) & set(partiallist[i+1])))
                elif operatorlist[i] == 'or':
                    templist.append(list(set(partiallist[i]) | set(partiallist[i + 1])))
                else:
                    pass
            else:
                if bool(templist):          #if templist is not empty we retrieve the intermediate result to formulate final result
                    if operatorlist[i] == 'and':
                        templist[0] = list(set(templist[0]) & set(partiallist[i+1]))
                    elif operatorlist[i] == 'or':
                        templist[0] = list(set(templist[0]) | set(partiallist[i+1]))
                    else:
                        pass
        result=templist[0].copy()
    print(sorted(result))         #print results for user query

def querysearch(positionalindex):

    print("Enter your query for positional index search")
    userquery=input()
    l2=userquery.lower()

    words_search=l2.split(' ')
    differ=int(words_search[3])       #getting hold of distance
    differ=differ+1

    stemmer = PorterStemmer()              #applying stemming on user query
    words_search = [stemmer.stem(plural) for plural in words_search]

    word1=words_search[0]
    word2=words_search[1]
    result=[]
    if word1 and word2 in positionalindex.keys():
        list1=positionalindex[word1].keys()
        list2=positionalindex[word2].keys()
        list3=[value for value in list1 if value in list2]   #list of documents that are common in terms of query term

        for i in range(len(list3)):
            position_word1=positionalindex[word1][list3[i]]      #getting position list for a given term document
            position_word2=positionalindex[word2][list3[i]]      #getting position list for a given term document

            for k in range(len(position_word1)):
                for l in range(len(position_word2)):
                    if abs(position_word1[k] - position_word2[l])<=differ:  #checking if the two user queried words appear in any sequence but within the required distance
                        if list3[i] not in result:
                            result.append(list3[i])

    print(result)           #print results for user query

mainprog()