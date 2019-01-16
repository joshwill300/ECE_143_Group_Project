def display_csv(fname):
    '''
    Author: Joshua Williams
    
    Function to display a dataframe from a file name (this file must have the .csv extension!)
    fname: the name of a csv to be displayed
    '''
    import pandas as pd
    import json
    from IPython.display import display, HTML

    assert isinstance(fname, str) and '.csv' in fname, 'Input is not a valid name of a csv file'

    df = pd.read_csv(fname)
    display(df)


def countPlatform(fname='dataframe_1000.csv'):
    '''
    Author: Joshua Williams
    
    Function to count how many games support each platform (Windows, Mac, Linux)

    (fname): A string name of a dataframe
    '''
    import pandas as pd
    assert isinstance(fname, str) and '.csv' in fname, 'fname is not a string name of a .csv file'

    df = pd.read_csv(fname)

    platforms = df['platform'].tolist()
    platform_dict = {}

    for platform_string in platforms:

        if pd.isnull(platform_string):
            continue

        platform_list = list(platform_string.split(','))
        platform_list.remove('')

        index = 0
        while index < len(platform_list):
            if platform_list[index] in platform_dict.keys():
                platform_dict[platform_list[index]] += 1
            else:
                platform_dict[platform_list[index]] = 1
            index += 1

    platform_df = pd.DataFrame(platform_dict, index=["count"])

    return platform_df


def countQuantity(fname='dataframe_1000.csv', col_name=''):
    '''
    Author: Joshua Williams
    
    Function to count the quantity of appearencesof an attribute in a specfied column
    NOTE: This function is geared toward columns that have list type items

    (fname): A string name of a dataframe
    (col_name): string name of a column in the dataframe
    '''
    import pandas as pd
    import ast
    assert isinstance(fname, str) and '.csv' in fname, 'fname is not a string name of a .csv file'
    assert isinstance(col_name, str), 'col_name is not of string type'

    df = pd.read_csv(fname)

    assert col_name in df, 'Specified column name does not exist in the specified dataframe!'

    col_val_list = df[col_name].tolist()
    column_dict = {}

    for col_val in col_val_list:
        if pd.isnull(col_val):
            continue

        # Converts string of a list to a list
        col_val = ast.literal_eval(col_val)

        for val in list(col_val):
            if val in column_dict.keys():
                column_dict[val] += 1
            else:
                column_dict[val] = 1

    column_df = pd.DataFrame(column_dict, index=["count"])

    column_df = column_df.sort_values('count', axis=1, ascending=False)

    return column_df


def countPublishers(fname='dataframe_1000.csv'):
    '''
    Author: Joshua Williams
    
    Function to count the quantity of appearences of a developer in our data

    (fname): A string name of a dataframe
    '''
    import pandas as pd
    import re
    assert isinstance(fname, str) and '.csv' in fname, 'fname is not a string name of a .csv file'

    df = pd.read_csv(fname)

    developers = df['developer'].tolist()
    developer_dict = {}

    for developer in developers:
        # Get the publisher name between these two strings
        start = 'Publisher:'
        end = 'Release Date:'

        if pd.isnull(developer):
            continue

        developer = developer[developer.find(start) + len(start):developer.find(end)]

        if developer in developer_dict.keys():
            developer_dict[developer] += 1
        else:
            developer_dict[developer] = 1

    developer_df = pd.DataFrame(developer_dict, index=["count"])
    developer_df = developer_df.sort_values('count', axis=1, ascending=False)

    return developer_df