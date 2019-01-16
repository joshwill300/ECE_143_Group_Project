#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate word clouds out of text of reviews

@author: Zi He (Hertz) GitID:Terahezi
"""

def convertJLtoDataFrame(fname='reviews_Top.jl', key_list_used=['product_id','text']):
    '''
    Convert the raw data in .jl format to a DataFrame
    
    :fname: str name of a .jl file with data (defaults to 'products_all.jl' which is our data)
    
    :key_list_used: a list of strings that are the name of features in the data 
    (Defaults to just three features 'all_ratio, platform, genres' as a demo for our analysis)
    '''
    assert isinstance(fname, str) and '.jl' in fname, "fname is not a valid str name of a .jl file containing data!"
        
    assert isinstance(key_list_used, list), "key_list_used is not a valid list of genres"
        
    import pandas as pd
        
    # Make the data into a list of all strings
    
    with open(fname,'r',encoding='utf8') as f:
        mylist = [line.rstrip('\n') for line in f]

    data_list = []

    # Convert the strings to dictionaries
    import json
    for i in mylist:
        d=json.loads(i)
        data_list.append(d)

    value_list_used = []
    key_list = []
    
    for i in key_list_used:
        key_list.append(i)
        value_list_used.append([])

    for i in data_list:
        # features w/o any values return None
        index = 0
        for key in key_list:
            value_list_used[index].append(i.get(key))
            index += 1

    # value_list_used = [value_list1,value_list2,value_list3]
    dic_used = dict(zip(key_list_used,value_list_used))

    # Convert to DataFrame
    df_used = pd.DataFrame(dic_used)
    
    # Return dataframe of the data from the .jl file
    return df_used

def generateReviewTextfromRawData(fname1='text_reviews',fname2='text_reviews_common'):
    
    '''output two text files containing the text reviews from
    top ten games and other ordinary games'''
    
    assert isinstance(fname1,str)
    assert isinstance(fname2,str)
    
    df_used=convertJLtoDataFrame()
    df_used_10=convertJLtoDataFrame('444090.jl')
    df_used_common=convertJLtoDataFrame('reviews0.jl')
    
    with open(fname1,'w') as f:
        for i in df_used.text:
            f.write(i)
        for j in df_used_10.text:
            f.write(j)
            
    with open(fname2,'w') as g:
        for i in df_used_common.text:
            if type(i)==str:
                g.write(i)
                
def generateTextCloud_top10(fname='text_reviews'):
    
    '''output two text clouds from the text files generated'''
    
    assert isinstance(fname,str)
    
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    with open('text_reviews') as f:
        text=f.read()
        wordcloud = WordCloud().generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt.show

def generateTextCloud_ordinary(fname='text_reviews_common'):
    
    '''output two text clouds from the text files generated'''
    
    assert isinstance(fname,str)
    
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    with open('text_reviews_common') as f:
        text=f.read()
        wordcloud = WordCloud(max_font_size=40).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        return plt.show                