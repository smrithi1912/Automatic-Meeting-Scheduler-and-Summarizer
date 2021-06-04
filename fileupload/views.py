from django.shortcuts import render
from .forms import TextForm
from .models import Text
from django.core.files import File
import nltk
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
import matplotlib.pyplot as plt
import io
import urllib, base64
from PIL import Image
from wordcloud import WordCloud,STOPWORDS
from employee.models import meeting
# Create your views here
def welcome_view(request):
    return render(request,'fileupload/index.html')
def speech(request,eid,mid):
    if request.user.is_authenticated is True:
        if request.user.id is eid:
            if request.method=='POST':
                form=TextForm(request.POST)
                context={
                    'form':form
                }
                return redirect(text_paste_view,eid,mid)
            else:
                form=TextForm()
                context={
                    'form':form,
                    "eid":eid,
                    "mid":mid

                }
                return render(request, 'fileupload/speech.html', context)
        else:
            return redirect(dashboard_view,request.user.id)
    else:
        return redirect(register_view)

def text_paste_view(request,eid,mid):
    if request.user.is_authenticated is True:
        if request.user.id is eid:
            if request.method== 'POST':
                text_form=TextForm(request.POST)
                if text_form.is_valid():
                    text_form.save(commit=False)
                    text_form.name = 'mini-project'
                    text_form.save()
                    transs=text_form.cleaned_data['transcript']
                    context={
                        'trans':transs
                    }
                    with open('mini_project.txt', 'w') as f:
                        myfile = File(f)
                        myfile.write(transs)
                    from nltk.cluster.util import cosine_distance
                    import numpy as np
                    import networkx as nx
                    def sentence_similarity(sent1, sent2): 
                        sent1 = [w.lower() for w in sent1]
                        sent2 = [w.lower() for w in sent2]
                    
                        all_words = list(set(sent1 + sent2))
                    
                        vector1 = [0] * len(all_words)
                        vector2 = [0] * len(all_words)
                    
                        # build the vector for the first sentence
                        for w in sent1:
                            if w in stopwords:
                                continue
                            vector1[all_words.index(w)] += 1
                    
                        # build the vector for the second sentence
                        for w in sent2:
                            if w in stopwords:
                                continue
                            vector2[all_words.index(w)] += 1
                    
                        return 1 - cosine_distance(vector1, vector2)
                    
                    # ARTIFICIAL INTELLIGENCE PROJECT - Automatic Story Summarization 

                    # ALGORITHM NAME - Automatic summarization based on weighting

                    #OWN
                    import os
                    import math
                    import nltk
                    from nltk.tokenize import RegexpTokenizer, sent_tokenize
                    from nltk.corpus import stopwords
                    from nltk.stem.snowball import SnowballStemmer
                    import operator
                    import matplotlib.pyplot as plt

                    stopwords = stopwords.words('english')
                    stopwords.append('Aayush')
                    stopwords.append('Kawathekar')
                    tokenizer = RegexpTokenizer(r'\w+')

                    stemmer = SnowballStemmer('english')
                    f1 = open('mini_project.txt')

                    # OWN - read the files
                    text1 = f1.read()
                    text2 = f1.read()
                    text3 = f1.read()

                    # OWN - tokenize and form nltk objects
                    tk1 = nltk.Text(tokenizer.tokenize(text1))
                    tk2 = nltk.Text(tokenizer.tokenize(text2))
                    tk3 = nltk.Text(tokenizer.tokenize(text3))

                    # OWN - remove punctuations and digits and change to lower case
                    tk1 = [w.lower() for w in tk1 if w.isalpha() and not w.isdigit()]
                    tk2 = [w.lower() for w in tk2 if w.isalpha() and not w.isdigit()]
                    tk3 = [w.lower() for w in tk3 if w.isalpha() and not w.isdigit()]

                    # OWN - remove stop words and stem the words
                    tk1 = [stemmer.stem(w) for w in tk1 if w not in stopwords]
                    tk2 = [stemmer.stem(w) for w in tk2 if w not in stopwords]
                    tk3 = [stemmer.stem(w) for w in tk3 if w not in stopwords]
                    mask_array=np.array(Image.open("fileupload\static\cloud.png"))
                    wc = WordCloud(background_color = '#bdbdbd', max_words=200000,mask=mask_array)
                    wc=wc.generate(text1)
                    plt.imshow(wc,interpolation= 'bilinear')
                    plt.axis("off")
                    image = io.BytesIO()
                    # plt.savefig('fileupload/static/image.png', format='png')
                    image.seek(0)  # rewind the data
                    string = base64.b64encode(image.read())
                    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
                    # OWN - find word frequencies
                    index1 = nltk.FreqDist(tk1)
                    index2 = nltk.FreqDist(tk2)
                    index3 = nltk.FreqDist(tk3)
                    # OWN - document frequencies
                    comb = list(index1.keys())
                    comb.extend(index2.keys())
                    comb.extend(index3.keys())
                    cindex = nltk.FreqDist(comb)
                    # OWN - split document into sentences
                    sent1 = sent_tokenize(text1)
                    tsent=len(sent1)
                    # print(tsent)
                    idf={}
                    for sentence in sent1:
                        words = tokenizer.tokenize(sentence)
                    for word in words:
                        cnt_idf=index1[word]
                        cnt_idf=(math.log(1+tsent/1+cnt_idf)+1)*index1[word]
                        if(word in idf):
                            idf[word]+=cnt_idf
                        else:
                            idf[word]=cnt_idf
                    sent2 = sent_tokenize(text2)
                    sent3 = sent_tokenize(text3)

                    # OWN - create word list of title
                    t1 = text_form.cleaned_data['title']
                    title1 = [stemmer.stem(w.lower()) for w in tokenizer.tokenize(t1) if w.isalpha() and w not in stopwords]
                    similarity_matrix = np.zeros((len(sent1), len(sent1)))
                    for idx1 in range(len(sent1)):
                        for idx2 in range(len(sent1)):
                            if idx1 == idx2: #ignore if both are same sentences
                                continue 
                            similarity_matrix[idx1][idx2] = sentence_similarity(sent1[idx1], sent1[idx2])
                    sentence_similarity_graph = nx.from_numpy_array(similarity_matrix)
                    scores = nx.pagerank(sentence_similarity_graph)
                    print(scores)
                    # Step 4 - Sort the rank and pick top sentences
                    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sent1)), reverse=True)

                    # OWN - calculate score for every sentence

                    scores1 = {}
                    sentence_lengths = []
                    for sentence in sent1:
                        sentence_lengths.append(len(sentence))
                        if len(sentence) < 81 and len(sentence)>10:
                            # OWN - find all words in the sentence
                            words = tokenizer.tokenize(sentence)
                            words = [stemmer.stem(w.lower()) for w in words if w.isalpha() and not w.isdigit()]
                            score = 0.0
                            titlewords = 0.0
                            idf_score = 0.0
                            cnt=-1
                            for word in words:
                                cnt+=1     
                                score = score + index1[word] / (1+cindex[word])
                                if(cnt==0):     
                                    factor=score/scores[1]        
                                if word in title1:
                                    titlewords += 1
                                if word in idf:
                                    idf_score += (idf[word]*idf[word])
                            # OWN - number of words in sentence / number of those words present in title
                            titlewords = 0.1 * titlewords / len(title1)
                            scores1[sentence] = score + titlewords + math.sqrt(idf_score)
                    scores2 = {}
                    sentence_lengths2 = []
                    for sentence in sent2:
                        sentence_lengths2.append(len(sentence))
                        if len(sentence) < 120:
                            # OWN - find all words in the sentence
                            words = tokenizer.tokenize(sentence)
                            words = [stemmer.stem(w.lower()) for w in words if w.isalpha() and not w.isdigit()]

                            # OWN - sum of term frequencies and doc frequencies
                            score = 0.0
                            titlewords = 0.0
                            for word in words:
                                score = score + index2[word] / (1+cindex[word])
                                if word in title2:
                                    titlewords += 1

                            # OWN - number of words in sentence / number of those words present in title
                            titlewords = 0.1 * titlewords / len(title2)
                            scores2[sentence] = score + titlewords
                    # print(scores2)

                    scores3 = {}
                    sentence_lengths3 = []
                    for sentence in sent3:
                        sentence_lengths3.append(len(sentence))
                        if len(sentence) < 90:
                            # OWN - find all words in the sentence
                            words = tokenizer.tokenize(sentence)
                            words = [stemmer.stem(w.lower()) for w in words if w.isalpha() and not w.isdigit()]

                            # OWN - sum of term frequencies and doc frequencies
                            score = 0.0
                            titlewords = 0.0
                            for word in words:
                                score = score + index3[word] / (1+cindex[word])
                                if word in title3:
                                    titlewords += 1


                            # OWN - number of words in sentence / number of those words present in title
                            titlewords = 0.1 * titlewords / len(title3)
                            scores3[sentence] = score + titlewords
                    summarize_text = []
                    for i in range(2):
                        summarize_text.append("".join(ranked_sentence[i][1]))
                    from rouge import Rouge
                    rouge = Rouge()
                    string_output=''
                    string_output=string_output.join(summarize_text)
                    scores_rouge = rouge.get_scores(transs,string_output)
                    string_output=''
                    string_output=string_output.join(summarize_text)
                    with open('summary.txt', 'w') as f:
                        myfile = File(f)
                        myfile.write(string_output) 
                    
                    context={
                        'summary': summarize_text,
                        'rouge_output':scores_rouge,
                        'mid':mid,
                        'eid':eid,
                    }
                    m = meeting.objects.get(id=mid)
                    m.summary=summarize_text
                    m.save()
                    #to-do
                    # max (of rec (calculated below) should equals iska max score sentence)
                    sorted1 = sorted(scores1.items(), key = operator.itemgetter(1))
                    fig,ax = plt.subplots(1,1)
                    ax.hist(scores1.values(), bins = 30)
                    ax.set_title("Sentence lengths histogram")
                    ax.set_xlabel('Number of characters')
                    ax.set_ylabel('Number of sentences')
                    image = io.BytesIO()
                    ax.figure.savefig('fileupload/static/histogram.png', format='png')
                    image.seek(0)  # rewind the data
                    string = base64.b64encode(image.read())
                    image_64 = 'data:histogram/png;base64,' + urllib.parse.quote(string)
                    # OWN - print the summary generated for each story
                    res = 0
                    max=0
                    for val in scores1.values():
                        if(val > max):
                            max=val
                            res += val            
                    # using len() to get total keys for mean computation
                    if(len(scores1)!=0):
                        res = res / len(scores1)
                    res=res+(max-res)/2
                    for sentence in scores1.keys():
                        if scores1[sentence] >= res:
                            print(sentence)
                    plt.close()
                    # fig.close()
                    return render(request,'fileupload/output.html',context)
            else:
                form=TextForm()
                context={
                    'form':form,
                    'mid':mid,
                    "eid":eid
                }
                return render(request,"fileupload/input.html",context)
        else:
            return redirect(dashboard_view,request.user.id)
    else:
        return redirect(register_view)




def analysis_view(request,eid,mid):
    if request.user.is_authenticated is True:
        if request.user.id is eid:
            context={}
            f=open ("mini_project.txt","r")
            transs=''
            for x in f:
                transs= transs.join(x)
            f=open ("summary.txt","r")
            string_output=''
            for x in f:
                string_output= string_output.join(x)
            from rouge import Rouge
            rouge = Rouge()
            scores_rouge = rouge.get_scores(transs,string_output)
            from summarizer import Summarizer
            model = Summarizer()
            result = model(transs, min_length=30)
            bert_summary = "".join(result)
            rouge = Rouge()
            scores_rouge = rouge.get_scores(bert_summary,string_output)
            context={
                'bert_output': bert_summary,
                'rouge_output':scores_rouge,
            }    

            return render(request,"fileupload/analysis.html",context)
        else:
            return redirect(dashboard_view,request.user.id)
    else:
        return redirect(register_view)

