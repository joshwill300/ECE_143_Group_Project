#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This notebook is to create .CSV files 
which show the number of genres 
in each top ten publisher.

@author: Zi He (Hertz) GitID:Terahezi
"""

def CartesianProduct_features(fname='dataframe_1000.csv',feature1='publisher',feature2='genres'):
    '''Generate a Cartesian product for two different features
    In this case it is genres and publishers'''
    
    assert isinstance(fname,str)
    assert fname=='dataframe_1000.csv'
    assert isinstance(feature1,str)
    assert isinstance(feature2,str)
    
    import pandas as pd
    import ast
    import itertools
    
    df_used=pd.read_csv(fname)
    list_all_Publisher=[]
    
    for i in df_used['developer']:
        if type(i)==str:
            index1=i.find('Publisher')
            index2=i.find('Release')
            if index1!=-1 and index2!=-1:
                list_all_Publisher.append([i[index1+10:index2]])
        else:
            list_all_Publisher.append(None)

    list_genres=list(df_used[feature2])

    for i in list_genres:
        if type(i)==str:
            list_genres[list_genres.index(i)]=ast.literal_eval(i)
        else:
            list_genres[list_genres.index(i)]=None
    
    list_genres_publisher=[]
    list_zipped=list(zip(list_genres,list_all_Publisher))
    for i in list_zipped:
        if type(i[0])==list and type(i[1])==list:
            for j in itertools.product(i[0],i[1]):
                list_genres_publisher.append(j)
    Cartesian_product=list(zip(*list_genres_publisher))
    return Cartesian_product

def Feature2_in_Feature1(publisher_list=['Paradox Interactive','Daedalic Entertainment','Ubisoft','Devolver Digital','SEGA','Sekai Project','SCS Software','Electronic Arts','AGM PLAYISM','Microsoft Studios']):
    
    '''According to the Cartesian product, generate individual dataframe
    for each publisher showing the number of each genre inside this publisher'''
    
    assert isinstance(publisher_list,list)
    
    from collections import Counter
    import pandas as pd
    
    b=CartesianProduct_features()
    list_indi_genre=list(b[0])
    list_indi_publisher=list(b[1])
    dic_indi_genre_indi_publisher={'genre':list_indi_genre,'publisher':list_indi_publisher}
    df_indi_genre_indi_publisher=pd.DataFrame(dic_indi_genre_indi_publisher)
    df_sorted=df_indi_genre_indi_publisher.sort_values(['publisher','genre'],ascending=True)
    
    
    for i in publisher_list:
        
        df_publisher=df_sorted[df_sorted.publisher.str.contains(i)]

        list_all_genres=df_publisher.genre

        
        d = Counter(list_all_genres)
    
        list_word=[]
        list_count=[]
    
        for word, count in d.most_common(10):
        
            list_word.append(word)
            list_count.append(count)
    
        dic_wordcount={'word':list_word,'count':list_count}
        df_wordcount=pd.DataFrame.from_dict(dic_wordcount)
        df_wordcount.to_csv('df_genrecount_{}.csv'.format(i))
        