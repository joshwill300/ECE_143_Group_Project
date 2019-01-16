def convertJLtoDataFrame(fname='products_all.jl', \
                         key_list_used=['id','title','specs','tags',\
                         'app_name','all_ratio','recent_ratio',\
                         'metascore','developer','publisher','genres',\
                         'sentiment','price','platform','release_date']):
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

    data_length = len(mylist)
    data_list = []

    # Convert the strings to dictionaries
    import json
    for i in mylist:
        d=json.loads(i)
        data_list.append(d)
        
    list_keys = list(data_list[0].keys())

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


def match_100_to_1000(fname1 = 'top_100_file.csv', fname2 = 'dataframe_1000.csv'):
    '''match those top played apps in recent 48 hours to the top 1000 reviewed apps'''
    assert '.csv' in fname1
    assert '.csv' in fname2
    import pandas as pd
    import numpy as np

    top = pd.read_csv(fname1, index_col=0)
    for index1, row1 in top.iterrows():
        top.loc[index1, 'Current_Players'] = int(row1['Current Players'].replace(',',''))
    top['Top_Played_Rank'] = top['Current_Players'].rank(ascending=0,method='min')
    top = top.sort_values(by = ['Top_Played_Rank'])
    top_dict = dict(zip(top['Game'], top['Top_Played_Rank']))
    print(top_dict)

    data5 = pd.read_csv(fname2, index_col=0)
    for index2, row2 in data5.iterrows():
        if row2['app_name'] in top_dict.keys():
            data5.loc[index2, 'Top_Played_Rank'] = top_dict[row2['app_name']]
        else:
            data5.loc[index2, 'Top_Played_Rank'] = None

    data5 = data5.sort_values(by = ['Top_Played_Rank'])
    return(data5)
    
    
def df_preprocessing(data1):
    ''' Extract informations from the developer column'''
    import pandas as pd
    assert isinstance(data1, pd.DataFrame)
    import numpy as np
    import string
    data2 = data1

    developer = []
    publisher = []
    release_date = []

    for index, row in data2.iterrows():
        if isinstance(row['developer'], str):
            if 'Publisher' in row['developer']:
                translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
                s = row['developer'].translate(translator)
                l = s.split()
                for i1 in range(len(l)):
                    for i2 in range(len(l)):

                        if 'Publisher' in l[i1] and 'Release' in l[i2]:
                            e1 = l[i1].replace('Publisher','')
                            nl1 = l[0:i1]
                            e2 = l[i2].replace('Release','')
                            nl2 = l[i1+1:i2]
                            nl3 = l[i2+2:]

                            if len(nl1) == 0 and len(e1) == 0:
                                data2.loc[index,'Developer'] = None
                            if len(nl1) == 0 and len(e1) != 0:
                                data2.loc[index,'Developer'] = e1
                            if len(nl1) != 0 and len(e1) == 0:
                                data2.loc[index,'Developer'] = ' '.join(nl1)
                            if len(nl1) != 0 and len(e1) != 0:
                                data2.loc[index,'Developer'] = ' '.join(nl1)+' '+e1

                            if len(nl2) == 0 and len(e2) == 0:
                                data2.loc[index,'Publisher'] = None
                            if len(nl2) == 0 and len(e2) != 0:
                                data2.loc[index,'Publisher'] = e2
                            if len(nl2) != 0 and len(e2) == 0:
                                data2.loc[index,'Publisher'] = ' '.join(nl2)
                            if len(nl2) != 0 and len(e2) != 0:
                                data2.loc[index,'Publisher'] = ' '.join(nl2)+' '+e2

                            if len(nl3) != 0:
                                data2.loc[index,'Release_Date'] = ' '.join(nl3)
                            if len(nl3) == 0:
                                data2.loc[index,'Release_Date'] = None


            else:
                data2.loc[index,'Developer'] = None
                data2.loc[index,'Publisher'] = None
                data2.loc[index,'Release_Date'] = None
        else:
            data2.loc[index,'Developer'] = None
            data2.loc[index,'Publisher'] = None
            data2.loc[index,'Release_Date'] = None
    return(data2)


def df_processing(data2):
    ''' this file is to generate the Positive_Review_Rank feature
    on the basis of which the new dataframe is created'''
    import pandas as pd
    assert isinstance(data2, pd.DataFrame)
    import numpy as np
    data3 = data2

    # generate the positive_review feauture
    for index, row in data3.iterrows():
        if 'positive' in row['all_ratio']:
            for i in row['all_ratio'].split():
                if i.isdigit():
                    all_review = int(i)
                if '%' in i:
                    for j in i.split('%'):
                        if j.isdigit():
                            all_ratio = int(j)
                if ',' in i:
                    all_review = int(i.replace(',', ''))
            data3.loc[index,'Positive_Review'] = round(all_review*all_ratio/100)
        else:
            data3.loc[index,'Positive_Review'] = None

    #sort out the dataframe according to positive_review_rank
    data3['Positive_Review_Rank'] = data3['Positive_Review'].rank(ascending=0,method='min')
    data3 = data3.sort_values(by = ['Positive_Review_Rank'])
    return(data3)


def final_to_1000(fname = 'dataframe_final.csv'):
    '''Convert the whole dataframe to the one containing the top1000'''
    assert '.csv' in fname

    import pandas as pd
    import numpy as np

    data4 = pd.read_csv('dataframe_final.csv', index_col=0)
    data4['Positive_Review_Rank'] = data4['Positive_Review_Rank'].fillna(16711).astype(int)
    data4 = data4.loc[data4['Positive_Review_Rank'].isin(range(1,1001))]

    data4.to_csv('dataframe_1000.csv')