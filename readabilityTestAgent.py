try:
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import sent_tokenize
    from nltk.corpus import cmudict
    import nltk
    import urllib2
    from bs4 import BeautifulSoup
    from matplotlib import pyplot as plt
    import sys
    import re
    import numpy as np
    from collections import Counter
    import matplotlib.patches as mpatches
    import pickle
    from ctypes.test.test_errno import threading
    import os
    import json
    import random
    import bodyTemplates
    import webbrowser
except:
    print "Few of the libraries are not import.. Kidly re check.."

random.seed(1024)

d = cmudict.dict()
def nsyl(word):
    '''
    Referred from https://groups.google.com/forum/#!topic/nltk-users/mCOh_u7V8_I
    '''
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
        #return len([list(y for y in alphabet if y[-1].isdigit()) for alphabet in d[word.lower()]])
    except KeyError:
        #if word not found in cmudict
        return syllables(word)

def syllables(word):
    '''
    This will be called only if word not in cmudict
    referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    '''
    if word.isdigit() or len(word)<=3:
        #return if word is a digit or a small word(most probably it will be an acronym)
        return 0
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def getSchoolLevel(fresScore):
    '''
    Get the corresponding school level from fres score
    '''
    if fresScore is None:
        return
    if fresScore > 90:
        return '5th Grade'
    elif fresScore > 80:
        return '6th Grade'
    elif fresScore > 70:
        return '7th Grade'
    elif fresScore > 60:
        return '8 & 9th Grade'
    elif fresScore > 50:
        return '10 & 12th Grade'
    elif fresScore > 30:
        return 'College'
    else:
        return 'College Graduate'
    
def drawGraph(results):
    '''
    Plot book vs readibility score graph
    '''
    if len(results) < 3:
        print "\nPlease evaluate at least 2 books for the graph to appear..\n"
        return
    plt.rcdefaults()
    fig, ax = plt.subplots()
    
    y_pos = range(len(results))
    fres = [result['fres'] for result in results]
    
    for i, result in enumerate(results):
        ax.text(1, i + .09, str(result['title'])+" \n("+str(result['schoolLevel'])+")")
    
    ax.barh(y_pos, fres)
    ax.set_yticks(y_pos)
    ax.invert_yaxis() 
     
    ax.set_ylabel('Books')
    ax.set_xlabel('Fleash Readibility Ease Score')
    ax.set_title("Book vs Flesch  Readibility Ease score plot")
    
    #Display a full scren plot
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    
    plt.show()
    
def preprocess(document):
    '''
    Pre processes the document, by extracting sentences, tokenizing words and pos tagging
    '''
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def evaluateAndPlot(interactionsDict):
    '''
    Evaluates interactions between 2 people and plots a heat map of interaction count
    '''
    allInteractions = {}
    for key in interactionsDict.keys():
        try:
            allInteractions[interactionsDict[key]['person1']].append(interactionsDict[key]['person2'])
            allInteractions[interactionsDict[key]['person2']].append(interactionsDict[key]['person1'])
        except:
            allInteractions[interactionsDict[key]['person1']] = [interactionsDict[key]['person2']]
            allInteractions[interactionsDict[key]['person2']] = [interactionsDict[key]['person1']]
            
    frequency = []
    #get frequency of all interactions
    for key in allInteractions.keys():
        interactionCount = []
        count = Counter(allInteractions[key])
        for key in allInteractions.keys():
            interactionCount.append(count[key])
        frequency.append(interactionCount)
        
    column_labels = allInteractions.keys()
    row_labels = allInteractions.keys()
    data = np.array(frequency)
    
    createHeatMap(data, row_labels, column_labels)

def createHeatMap(data, row_labels, column_labels):  
    '''
    Plot the heat map using the data evaulated above
    '''
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(1-data)
    
    # put the major ticks at the middle of each cell, notice "reverse" use of dimension
    ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
    
    ax.set_xticklabels(row_labels, minor=False, rotation=45)
    ax.set_yticklabels(column_labels, minor=False)
    
    ax.set_xlabel('People predicted by NLTK')
    ax.set_ylabel('People predicted by NLTK')
    ax.set_title("Heatmap of no. of interactions between people")
    
    y_patch = mpatches.Patch(color='yellow', label='No interactions')
    g_patch = mpatches.Patch(color='seagreen', label='1 interaction')
    b_patch = mpatches.Patch(color='darkslateblue', label='2 interactions')
    plt.legend(handles=[y_patch,g_patch,b_patch])
    
    #Display a full scren plot
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    
    plt.show()

def createScatterPlot(relationsDict):
    '''
    Evaluates interactions between 2 people and plots a scatterplot of relation count
    '''
    allRelations = {}
    people = set()
    locations = set()
    
    for key in relationsDict.keys():
        try:
            allRelations[relationsDict[key]['person']].append(relationsDict[key]['location'])
            people.add(relationsDict[key]['person'])
            locations.add(relationsDict[key]['location'])
        except:
            allRelations[relationsDict[key]['person']] = [relationsDict[key]['location']]
            people.add(relationsDict[key]['person'])
            locations.add(relationsDict[key]['location'])
    
    people = list(people)
    locations = list(locations)
    
    circles = {}
    
    for person in allRelations.keys():
        for location in allRelations[person]:
            circle = (people.index(person)+1,locations.index(location)+1)
            if circles.has_key(circle):
                circles[circle]+=0.35
            else:
                circles[circle]=0.35

    x = [key[0] for key in circles.keys()]
    y = [key[1] for key in circles.keys()]

    colors = circles.values()
    area = [np.pi * (15 * radius)**2 for radius in circles.values()]  # 0 to 15 point radii
    
    fig, ax = plt.subplots()
     
    ax.set_xticks(np.arange(len(people))+1, minor=False)
    ax.set_yticks(np.arange(len(locations))+1, minor=False)
    # put the major ticks at the middle of each cell, notice "reverse" use of dimension
    ax.set_xticklabels(people, minor=False, rotation=45, rotation_mode="anchor")
    ax.set_yticklabels(locations, minor=False)
    ax.grid(linestyle='-', linewidth=0.5)
    
    ax.set_xlabel('Predicted People')
    ax.set_ylabel('Predicted Locations')
    ax.set_title("Scatter plot of relations between people and locations")
    
    g_patch = mpatches.Patch(color='slateblue', label='1 interaction')
    b_patch = mpatches.Patch(color='yellow', label='2 interactions')
    plt.legend(handles=[g_patch,b_patch])
    
    #Display a full scren plot
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    
    plt.scatter(x, y, s=area, c=colors, alpha=0.6)
    plt.show()

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

class GoogleTextSearch(threading.Thread):
    '''
    Threaded google text search
    '''
    def __init__(self, q, textCorpus):
        threading.Thread.__init__(self)
        self.searchURL = "https://www.google.com/search?&q="+q.replace(" ","+")
        self.textCorpus = textCorpus
        self.q = q
    
    def run(self):
        try:
            print "Getting text for "+self.q
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            res = get_soup(self.searchURL, header)
            url = res.find('h3',{'class':'r'}).find('a')['href']
            res = get_soup(url, header)
            text = ""
            count = 0
            for p in res.find_all('p'):
                if len(p.get_text()) < 150:
                    continue
                text+=p.get_text()
                if count == 15:
                    break
                count+=1
            self.textCorpus[self.q] = text
        except:
            #Handle all scraping errors like page not found, parsing errors, forbidden, etc
            pass
        
class FetchGoogleImages(threading.Thread):
    '''
    Threaded google image search and saver
    '''
    def __init__(self, q, imageID):
        threading.Thread.__init__(self)
        self.searchURL = "https://www.google.co.in/search?source=lnms&tbm=isch&q="+q.replace(" ","+")
        self.imageID = imageID
        self.q = q
        
    def run(self):
        try:
            print "Searching image for query",self.q
            path = os.getcwd()+"\\jythonMusic\\imagesAndData\\"
            if not os.path.exists(path):
                os.makedirs(path)
            header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
            req = get_soup(self.searchURL, header)
            
            ActualImages=[]# Referred from https://stackoverflow.com/questions/35809554/how-to-download-google-image-search-results-in-python
            a = req.find("div",{"class":"rg_meta"})
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
                
            ###print images
            for i , (img , Type) in enumerate( ActualImages):
                try:
                    req = urllib2.Request(img, headers={'User-Agent' : header})
                    raw_img = urllib2.urlopen(req).read()
                    
                    filename = self.imageID
                    if len(Type)==0:
                        f = open(os.path.join(path, filename+".jpg"), 'wb')
                    else :
                        f = open(os.path.join(path , filename+"."+Type), 'wb')
                    
                    f.write(raw_img)
                    print "Image saved for ",self.q
                    f.close()
                except Exception as e:
                    pass
        except:
            #Handle all scraping errors like page not found, parsing errors, forbidden, etc
            pass
            

def searchAndDwnldLocImages(sentencesTuples):
    imageMetaData = {}
    threads = []
    for i, sentencesTuple in enumerate(sentencesTuples):
        if i==10:
            break
        imageMetaData[repr(i)] = sentencesTuple[0]
        q = sentencesTuple[1][sentencesTuple[1].rfind("[GPE: '"):len(sentencesTuple[1])-1].split("'")[1].split("/")[0]
        t = FetchGoogleImages(q, repr(i))
        t.start()
        threads.append(t)
    
    path = os.getcwd()+"\\jythonMusic\\imagesAndData\\"
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    f = open(os.path.join(path, 'imageMetaData.pickle'), 'wb')
    pickle.dump(imageMetaData, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()
        
    for t in threads:
        t.join() 
    
    print "\nAll images have been saved, kindly run program 'jythonMusic/SHANTANU_searchsonify.py' from Jython folder and editor\n"


def createAndLaunchWebPage(name, webpageText):
    '''
    Creates webpage with given name and launches the browser
    '''
    path = os.getcwd()+"\\jythonMusic\\imagesAndData\\"
    if not os.path.exists(path):
        os.makedirs(path)
    webPage = open(path+repr(name)+".html","w")
    webPage.write(webpageText)
    webPage.close()
    webbrowser.open_new_tab('file://' + os.path.realpath(path+repr(name)+".html"))

def getImage(i):
    '''
    returns ith image from all images
    '''
    return imageNames[i%len(imageNames)]+".jpg".replace(" ","+")

def getText(i, noOfwords=0):
    '''
    returns 'noOfwords' from ith text of the text corpus, if noOfWords = 0 returns whole text
    '''
    text = textCorpus[list(textCorpus)[i%len(imageNames)]]
    text = text.encode('ascii','ignore')
    if noOfwords!=0:
        words = text.split()
        if len(words) < noOfwords:
            return text
        else:
            return " ".join(word for word in words[0:noOfwords])
    return text   
    
def getMid(midTemplate, item1, item2, item3):
    '''
    returns mid element with mid template and 3 items followed by item
    '''
    mid = bodyTemplates.MIDS.values()[midTemplate]
    mid = mid.replace("$$image1$$",getImage(item1))
    mid = mid.replace("$$text1$$",getText(item1,100))
    mid = mid.replace("$$image2$$",getImage(item2))
    mid = mid.replace("$$text2$$",getText(item2,100))
    mid = mid.replace("$$image3$$",getImage(item3))
    mid = mid.replace("$$text3$$",getText(item3,100))
    return mid

#[banner1DNA,banner2DNA,midTemplateSequence[0,len(mid)]DNA,midDataSequence[0,len(data)]DNA]
def generateChromosome(imageNames):
    '''
    Chromosome contains 4 dna's, 2 for top and 2 for mid
    t - Template
    bt - Top banner template
    b1,b2 - Banner data
    ts - Mid Template sequence
    ds - Mid data sequence
    '''
    chromosome = {}
    t = random.randint(0,len(bodyTemplates.TEMPLATES)-1)
    bt = random.randint(0,len(bodyTemplates.TOPS)-1)
    b1 = random.randint(0,len(imageNames)-1)
    b2 = b1
    while True:
        if b1 != b2:
            break
        b2 = random.randint(0,len(imageNames)-1)
    midTemplates = bodyTemplates.MIDS
    ds = random.sample(xrange(len(imageNames)), len(imageNames)) 
    lenOfTS = len(ds)/3
    ts = []
    while lenOfTS!=0:
        lenOfTS-=1
        ts.append(random.randint(0,len(midTemplates)-1))
    chromosome['t'] = t
    chromosome['bt'] = bt
    chromosome['b1'] = b1
    chromosome['b2'] = b2
    chromosome['ts'] = ts
    chromosome['ds'] = ds
    return chromosome

def crossOverAndMutate(chromosome1, chromosome2, imageNames):
    '''
    Cross overs and mutates DNA's of the 2 chromosomes, to generate new list of 3 chromosome
    '''
    chromosomes = []
    for i in range(3):
        dominant = random.randint(0,1)
        if dominant == 1:
            chromosome = dict(chromosome1)
        else:
            chromosome = dict(chromosome2)
        randomSwap = random.randint(0,len(chromosome1)-1)
        swapKey = chromosome1.keys()[randomSwap]
        chromosome[swapKey] = chromosome2[swapKey]
        mutateOn = random.randint(0,10)
        if mutateOn < len(chromosome1):
            mutateKey = chromosome1.keys()[mutateOn]
            if mutateKey == 't':
                chromosome['t'] = random.randint(0,len(bodyTemplates.TEMPLATES)-1)
            elif mutateKey == 'bt':
                chromosome['bt'] = random.randint(0,len(bodyTemplates.TOPS)-1)
            elif mutateKey == 'b1':
                chromosome['b1'] = random.randint(0,len(imageNames)-1)
                while True:
                    if chromosome['b1'] != chromosome['b2']:
                        break
                    chromosome['b1'] = random.randint(0,len(imageNames)-1)
            elif mutateKey == 'b2':
                chromosome['b2'] = random.randint(0,len(imageNames)-1)
                while True:
                    if chromosome['b1'] != chromosome['b2']:
                        break
                    chromosome['b2'] = random.randint(0,len(imageNames)-1)
            elif mutateKey == 'ts':
                ds = random.sample(xrange(len(imageNames)), len(imageNames)) 
                lenOfTS = len(ds)/3
                ts = []
                while lenOfTS!=0:
                    lenOfTS-=1
                    ts.append(random.randint(0,len(bodyTemplates.MIDS)-1))
                chromosome['ts'] = ts
            elif mutateKey == 'ds':
                chromosome['ds'] = random.sample(xrange(len(imageNames)), len(imageNames))
        chromosomes.append(chromosome)
    
    return chromosomes
    
def convertChromosomeToHTML(chromosome, imageNames, title):
    '''
    Maps each element of DNA from the chromosome to appropriate sections in the website
    '''
    body = bodyTemplates.TEMPLATES.values()[chromosome['t']]

    #set top
    top = bodyTemplates.TOPS.values()[chromosome['bt']]
    top = top.replace("$$banner1$$",getImage(chromosome['b1']))
    top = top.replace("$$banner2$$",getImage(chromosome['b2']))
    top = top.replace("$$head1$$",getText(chromosome['b1'],10))
    top = top.replace("$$head2$$",getText(chromosome['b2'],50))
    body = body.replace("$$top$$",top)
    
    mid = ""
    dataCount = 0
    templateCount = 0
    while dataCount+3 < len(imageNames):
        template = bodyTemplates.MIDS.values()[chromosome['ts'][templateCount]]
        templateCount+=1
        template = template.replace("$$image1$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text1$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        template = template.replace("$$image2$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text2$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        template = template.replace("$$image3$$",getImage(chromosome['ds'][dataCount]))
        template = template.replace("$$text3$$",getText(chromosome['ds'][dataCount],100))
        dataCount+=1
        mid+=template
        
    body = body.replace("$$mid$$",mid)
    body = body.replace("$$title$$",title)
    
    return body
    


def dwnldDataAndCreateWebsite(sentencesChunk, title="The women in white"):
    '''
    Download data to design websites
    '''
    print "Scrapping data to create the website"
    threads = []
    global imageNames
    global textCorpus
    imageNames = []
    textCorpus = {}
    t = FetchGoogleImages(q=title,imageID=title)
    t.start()
    threads.append(t)
    t = GoogleTextSearch(title,textCorpus)
    t.start()
    threads.append(t)
    
    namedEntities = set()
    reParser = nltk.RegexpParser('''CHUNK: {<PERSON>}
                                            {<LOCATION>}
                                            {<FACILITY>}
                                            {<GPE>}''')  
         
    #Extracting interaction using regex                                                      
    for sentenceChunk in sentencesChunk:
        tree = reParser.parse(sentenceChunk)
        for subtree in tree.subtrees():
            if subtree.label() == 'CHUNK': 
                namedEntities.add(' '.join([list(name)[0] for name in subtree[0]]))
    
    namedEntities = list(namedEntities)
    for i in range(25):
        index = random.randint(0,len(namedEntities))
        t = FetchGoogleImages(q=namedEntities[index]+title,imageID=namedEntities[index])
        t.start()
        threads.append(t)
        t = GoogleTextSearch(namedEntities[index]+title, textCorpus)
        t.start()
        threads.append(t)
        
    print "\nKindly be patient, threads are grabbing awesome images from the internet.. This will take some time.."
    for t in threads:
        t.join()
        
    print "Website data scrapped successfully, starting website creation.."
    
    #f = open('websiteMetaData.pickle', 'wb')
    #pickle.dump(textCorpus, f, protocol=pickle.HIGHEST_PROTOCOL)
    #f.close()
    
    for key in textCorpus.keys():
        imageNames.append(key[:key.index(title)])
    
    
    ####Genetic Algorithm to create website########
    webpageTemplate = bodyTemplates.WEBPAGETEMPLATE
    webpageTemplate = webpageTemplate.replace("$$title$$",title)

    i = 0
    initialPopulation = []
    while i<3:
        i+=1
        chromosome = generateChromosome(imageNames)
        initialPopulation.append(chromosome)
        body = convertChromosomeToHTML(chromosome, imageNames, title)
        html = webpageTemplate.replace("$$body$$",body)
        createAndLaunchWebPage("webPage"+repr(i), html)
            
    while True:
        print "Genetically curated web pages:"
        for k,chromosome in enumerate(initialPopulation):
            print repr(k+1)+". Webpage"+repr(k+1)+".html"
        
        i = 0
        j = 0
        try:    
            print "Select 2 of the 3 web pages you liked the most, I will genetically evolve them to create new ones.. \n(Enter comma seperated options e.g. >>> 1,2 or >>> 2,3 )"
            userInput = raw_input("If you liked a page and want to stop, enter 'e'; grab the liked webpage's html from the parent directory..\n>>> ")
            if userInput=='e':
                break
            i = userInput.split(",")[0]
            j = userInput.split(",")[1]
            try:
                i = int(i)
                j = int(j)
            except:
                print "Kindly enter only integer options!"
                continue
            if i==j:
                print "Kindly select 2 different options!"
                continue
            if i>3 or k>3:
                print "Kindly enter correct options!"
                continue
        except:
            print "Kindly enter correct userInput (comma seperated options e.g. >> 1,2 or >> 2,3 )"
            continue
        
        print "Displaying in the browser 3 freshly brewed pages using the pages you liked.."
        initialPopulation = crossOverAndMutate(initialPopulation[i-1], initialPopulation[j-1], imageNames)
        for l,chromosome in enumerate(initialPopulation):
            body = convertChromosomeToHTML(chromosome, imageNames, title)
            html = webpageTemplate.replace("$$body$$",body)
            createAndLaunchWebPage("webPage"+repr(l+1), html)
    
        
class agent():
    def sensor(self, testText):
        tokenizer = RegexpTokenizer(r'\w+')
        self.words = tokenizer.tokenize(testText)
        self.sentences = sent_tokenize(testText)
        return self.function()
    def function(self):
        totalWords = len(self.words)
        totalSents = len(self.sentences)
        totalSylabl = 0
        for word in self.words:
            sylabl = nsyl(word)
            totalSylabl += sylabl
        self.fres = 206.835 - 1.015 * (totalWords/float(totalSents)) - 84.6 * (totalSylabl/float(totalWords))
        self.fkgl = 0.39 * (totalWords/float(totalSents)) + 11.8 * (totalSylabl/float(totalWords)) - 15.59
        return self.actuator()
    def actuator(self):
        return (self.fres, self.fkgl)
    
class environment():
    def textEvaluator(self):
        print "Fetching book categories, please be patient.."
        url = "https://www.gutenberg.org/wiki/Category:Bookshelf"
        html = urllib2.urlopen(url)
        raw = BeautifulSoup(html, 'html.parser')
        categoryHtml = raw.find("div",{"id":"mw-subcategories"})
        categoryList = categoryHtml.find_all('li')
        categoryMenu = {}
        categoryMenuText = "Select one of the category below:\n"
        for category in categoryList:
            categoryMenu[category.find('a').get_text().encode('ascii','ignore')] = category.find('a')['href'].encode('ascii','ignore')
        for i,key in enumerate(categoryMenu):
            categoryMenuText+=repr(i+1)+". "+key+"\n"
        categoryMenuText+="0. Exit\nEnter 'p' for the readability ease PLOT of explored books(Please explore atleast 2 books before plotting) \n"
        results = []
        while True:
            try:    
                catInput = raw_input(categoryMenuText+">>> ")
                if catInput.isdigit():
                    catInput = int(catInput)
                else:
                    if catInput == 'p':
                        drawGraph(results)
                        continue
                    else:
                        raise KeyError
                if catInput == 0:
                    break
                if catInput <= len(categoryMenu):
                    print "Fetching sub categories of category",list(categoryMenu)[catInput-1],", please be patient.."
                    html2 = urllib2.urlopen("https://www.gutenberg.org"+categoryMenu[list(categoryMenu)[catInput-1]])
                    subCategoryList = BeautifulSoup(html2, 'html.parser').find("div", {"id":"mw-pages"}).find_all('li')
                    subCategoryMenu = {}
                    subCategoryMenuText = "Select one of the subcategories below:\n"
                    for subCategory in subCategoryList:
                        subCategoryMenu[subCategory.find('a').get_text().encode('ascii','ignore')] = subCategory.find('a')['href'].encode('ascii','ignore')
                    for i,key in enumerate(subCategoryMenu):
                        subCategoryMenuText+=repr(i+1)+". "+key+"\n"
                    subCategoryMenuText+="0. Go back to category listing\nEnter 'p' for the readability ease PLOT of explored books(Please explore atleast 2 books before plotting)\n"
                    while True:
                        try:
                            subCatInput = raw_input(subCategoryMenuText+">>> ")
                            if subCatInput.isdigit():
                                subCatInput = int(subCatInput)
                            else:
                                if subCatInput == 'p':
                                    drawGraph(results)
                                    break
                                else:
                                    raise KeyError
                            if subCatInput == 0:
                                break
                            if subCatInput <= len(subCategoryMenu):
                                print "Fetching books under the sub category",list(subCategoryMenu)[subCatInput-1],", please be patient.."
                                html3 = urllib2.urlopen("https://www.gutenberg.org"+subCategoryMenu[list(subCategoryMenu)[subCatInput-1]])
                                bookHtml = BeautifulSoup(html3, 'html.parser').find("div", {"id":"mw-content-text"})
                                bookList = bookHtml.find_all("a",{"class":"extiw"})
                                bookMenu = {}
                                bookMenuText = "Select one of the books below:\n"
                                for book in bookList:
                                    bookMenu[book.get_text().encode('ascii','ignore')] = book['href'].encode('ascii','ignore')
                                for i,key in enumerate(bookMenu):
                                    bookMenuText+=repr(i+1)+". "+key+"\n"
                                bookMenuText+="0. Go back to sub category listing\nEnter 'p' for the readability ease PLOT of explored books(Please explore atleast 2 books before plotting)\n"
                                while True:
                                    try:
                                        bookInput = raw_input(bookMenuText+">>> ")
                                        if bookInput.isdigit():
                                            bookInput = int(bookInput)
                                        else:
                                            if bookInput == 'p':
                                                drawGraph(results)
                                                break
                                            else:
                                                raise KeyError
                                        if bookInput == 0:
                                            break
                                        if bookInput <= len(bookMenu):
                                            title = list(bookMenu)[bookInput-1]
                                            bookUrl =  bookMenu[title]
                                            print "Reading book '",title,"' and finding readability socre, please be patient.."
                                            bookUrl = "https://www.gutenberg.org/ebooks"+bookUrl[bookUrl.rindex("/"):len(bookUrl)]+".txt.utf-8"
                                            html4 = urllib2.urlopen(bookUrl)
                                            raw = html4.read().decode('utf8', 'ignore')
                                            print "\nTitle:",title
                                            try:
                                                author = raw[raw.find("Author:"):raw.find("Release Date:")]
                                                author = author.split(":")[1]
                                                author = author[0:author.find('\n')].encode('ascii','ignore').strip()
                                                print "Author:", author
                                            except:
                                                pass
                                            scores = agent().sensor(raw)
                                            schoolLevel = getSchoolLevel(scores[0])
                                            print "Flesch reading ease score:",scores[0],"\nFlesch Kincaid grade level:",scores[1],"\nSchool Level:",schoolLevel,"\n\n"
                                            result = {"author":author,"title":title,"fres":scores[0],"fkgl":scores[1],"schoolLevel":schoolLevel}
                                            results.append(result)
                                            resultInput = raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue and select another book\nEnter 'p' for the readability ease PLOT of explored books(Please explore atleast 2 books before plotting)\n>>> ")
                                            if resultInput == '0':
                                                break
                                            elif resultInput == 'p':
                                                drawGraph(results)
                                        else:
                                            print "Kindly enter value between 1 to", len(bookList),"\n"
                                            if '0' == raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue\n>>> "):
                                                break
                                    except AttributeError as e:
                                        print "Sorry, some error occured while parsing the web page, kindly try with a different value..","Technical Details ->", e
                                        if '0' == raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue and select another book\n>>> "):
                                            break
                                    except urllib2.HTTPError as e:
                                        print "Sorry, some error occured while parsing the url, kindly try with a different value..","Technical Details ->",e
                                        if '0' == raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue and select another book\n>>> "):
                                            break
                                    except UnicodeDecodeError as e:
                                        print "Sorry, some decoding error occured while parsing the webpage, kindly try with a different value..","Technical Details ->",e
                                        if '0' == raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue and select another book\n>>> "):
                                            break
                                    except:
                                        print "Kindly enter correct value..\n", sys.exc_info()
                                        if '0' == raw_input("Press 0 to go back to sub category listing page\nPress any other key to continue and select another book\n>>> "):
                                            break
                            else:
                                print "Kindly enter value between 1 to",len(subCategoryMenu),"\n"
                                if '0' == raw_input("Press 0 to go back to category listing page\nPress any other key to continue and enter correct sub category\n>>> "):
                                    break
                        except urllib2.HTTPError as e:
                            print "Sorry, some error occured while parsing the url, kindly try with a different value..","Technical Details ->",e
                            if '0' == raw_input("Press 0 to go back to category listing page\nPress any other key to continue and select another sub category\n>>> "):
                                break
                        except AttributeError as e:
                            print "Sorry, some error occured while parsing the web page, kindly try with a different value..","Technical Details ->", e
                            if '0' == raw_input("Press 0 to go back to category listing page\nPress any other key to continue and select another sub category\n>>> "):
                                break
                        except:
                            print "Kindly enter correct value..\n"
                            if '0' == raw_input("Press 0 to go back to category listing page\nPress any other key to continue and select another sub category\n>>> "):
                                break
                else:    
                    print "Kindly enter value between 1 to",len(categoryMenu),"\n"
                    if '0' == raw_input("Press 0 to go back to category listing page\nPress any other key to continue and select correct sub category\n>>> "):
                        print "Thank you!"
                        break
            except urllib2.HTTPError as e:
                print "Sorry, some error connecting the url, kindly try with a different value..","Technical Details ->",e
                if '0' == raw_input("Press 0 to exit\nPress any other key to continue and select another category\n>>> "):
                    break
            except AttributeError as e:
                print "Sorry, some error occured while parsing the web page, kindly try with a different value..","Technical Details ->", e
                if '0' == raw_input("Press 0 to exit\nPress any other key to continue and select another category\n>>> "):
                    break
            except:
                print "Kindly enter a correct value..\n"
                if '0' == raw_input("Press 0 to exit\nPress any other key to continue and select another category\n>>> "):
                    break
    
    def erExtraction(self):
        raw = ""
        title = ""
        try:
            print "Kindly be patient, scrapping book 'The Women in white' from Gutenberg website, tagging POS and analyzing interactions/relations.."
            erBookUrl = "http://www.gutenberg.org/files/583/583.txt" #Url of 'The Women in white' book
            response = urllib2.urlopen(erBookUrl)
            raw = response.read().decode('utf8', 'ignore').encode('ascii','ignore')
            title = raw[raw.find('Title:'):raw.find('Author')].split(":")[1].strip()
            raw = raw[raw.find("START OF THIS PROJECT GUTENBERG EBOOK"):raw.find("END OF THIS PROJECT GUTENBERG EBOOK")]
        except:
            print "Sorry, not able to connect to the url and parse the book.. Try after some time!"
            return 
        sentences = preprocess(raw)
        sentencesChunk = [nltk.ne_chunk(sentence) for sentence in sentences]
        
        interactions = []
        nameVerbNameParser = nltk.RegexpParser('''CHUNK: {<PERSON><V.*><PERSON>}''')  
         
        #Extracting interaction using regex                                                      
        for sentenceChunk in sentencesChunk:
            tree = nameVerbNameParser.parse(sentenceChunk)
            for subtree in tree.subtrees():
                if subtree.label() == 'CHUNK': 
                    interactions.append([subtree[0], subtree[1], subtree[2]])
        
        interactionsDict = {}
        for i,interaction in enumerate(interactions):
            person1 = ' '.join([list(name)[0] for name in interaction[0]])
            verb = interaction[1][0]
            person2 = ' '.join([list(name)[0] for name in interaction[len(interaction)-1]])
            interactionsDict[i] = {'person1':person1, 'verb':verb, 'person2':person2}
        
        #Extracting relation using extract_rels
        perLocRelations = []
        sentencesTuples = []
        IN = re.compile(r'.*')
        for sentence in sentencesChunk:
            for rel in nltk.sem.extract_rels('PERSON', 'GPE', sentence, pattern = IN):
                perLocRelations.append(nltk.sem.rtuple(rel))
                sentencesTuples.append((' '.join([w for w, t in sentence.leaves()]),nltk.sem.rtuple(rel)))
        
        relationsDict = {}
        for key,perLocRelation in enumerate(perLocRelations):
            person = perLocRelation[perLocRelation.rfind('PER:'):perLocRelation.index(']')]
            nameTokens = person.split()
            person = ''
            for i in range(1,len(nameTokens)):
                person += " "+nameTokens[i].split("/")[0]
            location = perLocRelation[perLocRelation.rfind('GPE:'):len(perLocRelation)-1]
            locationTokens = location.split()
            location = ''
            for i in range(1,len(locationTokens)):
                location += " "+locationTokens[i].split("/")[0]
            relationsDict[key] = {'person':person[2:len(person)], 'location':location[2:len(location)]}
            
        while True:
            try:
                userInput = int(raw_input("1. Heatmap of interaction between people (Person Verb Person)\n2. Scatterplot of relation between people and locations (Person Location)\n3. Search and Download location images, and sonify sentences (Good Performance)\n4. Genetically create a web-site from the book\n0. Previous Menu\n>>> "))
                if userInput == 1:
                    #evaluate and plot interaction
                    evaluateAndPlot(interactionsDict)
                elif userInput == 2:
                    #evaluate and plot relations
                    createScatterPlot(relationsDict)
                elif userInput == 3:
                    #search images and download
                    print "Using the tagged sentences to grab locations, below are the locations found, images are being downloaded for the same..\nOnce this is done, each sentence's sonified noise can be heard by running 'jythonMusic/SHANTANU_searchsonify.py' from the jythonMusic folder"
                    searchAndDwnldLocImages(sentencesTuples)
                elif userInput == 4:
                    #download data for website
                    dwnldDataAndCreateWebsite(sentencesChunk, title)
                elif userInput == 0:
                    break
                else:
                    print "Kindly enter correct value.."
                    continue
            except:
                print "Kindly enter correct value.."
                continue
        
        
if __name__ == '__main__':
    print "Welcome to the language processing agent!"
    while True:
        userInput = raw_input("Select one of the options below:\n1. Flesch Reading Ease score evaluator(Satisfactory Performance)\n2. Natural Language Processing and genetically creating website (Baseline, Good performance & Excellent)\n0. Exit\n>>> ")
        if userInput is None or not userInput.isdigit():
            print "Kindly enter correct option.."
            continue
        else:
            userInput = int(userInput)
        if userInput == 0:
            print "Thank you!"
            break
        elif userInput == 1:
            environment().textEvaluator()
        elif userInput == 2:
            environment().erExtraction()
    #environment().erExtraction()
    
