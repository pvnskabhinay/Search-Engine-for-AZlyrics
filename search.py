from scipy.spatial import distance
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import json
import string
import numpy as np
from scipy import spatial
from sklearn.cluster import KMeans
import copy
import heapq
import requests

def download_song_MDB():
    collection = 'songs_collections'
    params = {'apiKey': 'hyWayEWsxClXi-l7i8300GBwfkFvL9HV'}
    dbname = 'homework3'
    url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection + '?l=87066'
    response=requests.get(url, params, stream=True)
    #data=(response.text)
    dataset = json.loads(response.text)#data
    return(dataset)


### POSTING LIST
def download_posting_list_MDB():
    collection = 'posting_list'
    params = {'apiKey': 'hyWayEWsxClXi-l7i8300GBwfkFvL9HV'}
    dbname = 'homework3'
    url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection + '?l=87066'
    response=requests.get(url, params, stream=True)
    data=(response.text)
    dataset = json.loads(data)
    return(dataset)
    
    
def prep_query(query):
    stop_en = get_stop_words('english')
    stop_fr = get_stop_words('french')
    stop_it = get_stop_words('italian')
    stop_sp = get_stop_words('spanish')
    stop_po = get_stop_words('portuguese')
    stop_da = get_stop_words('german')
    stop_ru = get_stop_words('russian')
    all_stop = stop_sp + stop_it + stop_en + stop_fr + stop_po + stop_da + stop_ru # need stopwords for all song languages
    all_stop = set(all_stop)    
    for char in query:
        query = ''.join(char for char in str(query) if char not in string.punctuation).lower().split()
    for word in query:
        if word in all_stop:
            query.remove(word)
    ps = PorterStemmer() # stemming
    query = [ps.stem(word) for word in query]
    query = set(query)
    return query

    
def word_id(word, lst):
    return lst.index(word)    


def query_vectorizing (query, list_tf, testi_stemmati):
    set_songs = set()
    set_words = set()
    
    for word in query:
        if word in list_tf.keys():
            for song in list_tf[word].keys():
                set_songs.add(song)
                
    for song in set_songs:
        if song in testi_stemmati.keys():
            for word in testi_stemmati[song]['Lyrics']:
                set_words.add(word)
                            
    set_words = list(set_words)
    n = len(set_words)
    
    # query vectorizing now    
    vector_query = [0] * n
    
    for word in query:
        vector_query[word_id(word, set_words)] = np.log(len(testi_stemmati) / len(list_tf[word]))

    return vector_query, set_words, set_songs      
    


def search_song(vector_query, set_words, set_songs, stem, list_tf):
    
    best_k = []
    n = len(set_words)    

    for song in set_songs:
        vector_lyrics = [0] * n
        for word in set_words:
            try:
                vector_lyrics[word_id(word, set_words)] += (list_tf[word][song] * np.log(len(stem) / len(list_tf[word])))
            except:
                KeyError
                
        cosineSim = (1 - spatial.distance.cosine(vector_query, vector_lyrics))
        best_k.append([cosineSim, song])
        
    best_10 = heapq.nlargest(10, best_k, key=None)
    return best_10, best_k


def cluster(best_k, testi_stemmati, set_words):
    
    n = len(set_words)
    normalized = []

    for cosSim, song in best_k:
        norm = [0] * n
        for word in set_words:
            try:
                norm[word_id(word, set_words)] += (list_tf[word][song] * (np.log(len(testi_stemmati) / len(list_tf[word]))))
            except:
                KeyError
                
        normalized.append([float(i)/sum(norm) for i in norm])
        
    euc_mat = np.zeros((len(normalized), len(normalized))) # matrix (n*n)

    for i in range(len(normalized)):
        for j in range(len(normalized)):
            euc_mat[i, j] = (distance.euclidean(normalized[i], normalized[j]))

    
    return euc_mat, normalized

def kmeans(k , euc_mat, set_words, normalized):

    kmeans = KMeans(n_clusters = k)
    kmeans.fit(euc_mat)
    
    labels = kmeans.labels_
    
    clustered = ([list(np.where(labels == ind)[0]) for ind in np.unique(labels)]) # divide clusters into indexes
    song_clustered = copy.deepcopy(clustered)

    for i in range(len(song_clustered)): # from indexes to n_song inside the clusters
        for song in song_clustered[i]:
            song_clustered[i][song_clustered[i].index(song)] = best_k[song][1]
    
    cl_i = 0
    val_id = 2
    word_cluster_lab = []
    for i in range(len(clustered)): # from indexes to normalized vectors inside the clusters
        vect_to_sum = []
        for song in (clustered[i]):
            vect_to_sum.append(normalized[song])
            
        vec = [sum(i) for i in zip(*vect_to_sum)]
        word_id = vec.index(max(vec))
        lab = set_words[word_id]
        if lab not in word_cluster_lab:
            word_cluster_lab.insert(cl_i, lab)
        else: 
            word_cluster_lab.insert(cl_i, lab + str(val_id))
            val_id += 1
        cl_i += 1
        
    return word_cluster_lab, song_clustered        

# importiamo tutto
testi_stem=download_song_MDB() 
testi_stemmati={}
for i in range(len(testi_stem)):
    testi_stemmati.update(testi_stem[i])
del(testi_stem)

list_tf_prov=download_posting_list_MDB()
list_tf={}
for i in range(len(list_tf_prov)):
    list_tf.update(list_tf_prov[i])
del(list_tf_prov)        

query = list(prep_query(str(input("Please insert your query: ").split())))

vector_query, set_words, set_songs = query_vectorizing(query, list_tf, testi_stemmati)
best_10, best_k = search_song(vector_query, set_words, set_songs, testi_stemmati, list_tf)

i = 1
for c, song in best_10:
    print(i)
    print(testi_stemmati[song]['Artist'])
    print(testi_stemmati[song]['Title'])
    print(testi_stemmati[song]['Url'])
    print('--------------------------')
    i += 1

k = input('How many clusters do you want? Please insert an integer: ')
cluster_query = input('Do you want a cluster of all results(a) or just of the top 50?(b): ')
k = int(k)

if str(cluster_query) == 'a':
    euc_mat, normalized = cluster(best_k, testi_stemmati, set_words)
    word_cluster_lab, song_clustered = kmeans(k)

elif str(cluster_query) == 'b':
    best_50 = best_k[:50]
    set_words_cluster = set()
    
    for cosSim, song in best_50:
        if song in testi_stemmati.keys():
            for word in testi_stemmati[song]['Lyrics']:
                set_words_cluster.add(word)
    
    set_words = list(set_words_cluster)
    euc_mat, normalized = cluster(best_50, testi_stemmati, set_words)
    word_cluster_lab, song_clustered = kmeans(k, euc_mat, set_words, normalized)
    
    
for cl in range(len(song_clustered)):
    print('##########################################')
    print('CLUSTER LABEL: ' + word_cluster_lab[cl])
    print('##########################################')
    for song in song_clustered[cl]:
        print(testi_stemmati[song]['Artist'])
        print(testi_stemmati[song]['Title'])
        print(testi_stemmati[song]['Url'])
        print('--------------------------')