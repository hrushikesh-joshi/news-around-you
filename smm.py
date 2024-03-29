import spacy
from spacy.lang.pt.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import pt_core_news_sm
nlp = pt_core_news_sm.load()
with open("RL.txt", "r", encoding="utf-8") as f:
        text = " ".join(f.readlines())
text=text.replace("The Indian Express is now on Telegram. Click here to join our channel (@indianexpress) and stay updated with the latest headlinesFor all the latest India News, download Indian Express App.","")     
doc =nlp(text)
corpus = [sent.text.lower() for sent in doc.sents ]
cv = CountVectorizer(stop_words=list(STOP_WORDS))   
cv_fit=cv.fit_transform(corpus)    
word_list = cv.get_feature_names();    
count_list = cv_fit.toarray().sum(axis=0)
word_frequency = dict(zip(word_list,count_list))
val=sorted(word_frequency.values())
higher_word_frequencies = [word for word,freq in word_frequency.items() if freq in val[-3:]]
print("\nWords with higher frequencies: ", higher_word_frequencies)
# gets relative frequency of words
higher_frequency = val[-1]
for word in word_frequency.keys():  
    word_frequency[word] = (word_frequency[word]/higher_frequency)
    sentence_rank={}
for sent in doc.sents:
    for word in sent :       
        if word.text.lower() in word_frequency.keys():            
            if sent in sentence_rank.keys():
                sentence_rank[sent]+=word_frequency[word.text.lower()]
            else:
                sentence_rank[sent]=word_frequency[word.text.lower()]
top_sentences=(sorted(sentence_rank.values())[::-1])
top_sent=top_sentences[:9]
summary=[]
for sent,strength in sentence_rank.items():  
    if strength in top_sent:
        summary.append(sent)
    else:
        continue
with open('ss.txt', 'w') as filehandle:
    for listitem in summary:
        filehandle.write('%s' % listitem)
    