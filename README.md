# ECE_G15
This is a repository for the project of Group15 at ECE143.


# Summary
Our project consisted of 3 phases: Data Extraction, Data Processing, Data visualization, and our analysis. We began with scraping the data from Steam website into a .jl file. We then took this .jl file and sorted it into a general csv adn assigned each game a ranking based in number of positive comments. We then took this file and truncated it into a file containg the top 1000 games with positive comments. This file was then seperated into several other csvs for us to plot the data and generate a text cloud of the comments. Alot of our functions were cut for the purpose of simplicity, so for the purpose of rerunning our project all you must do is run 'ECE143_G15_Main.ipynb' which runs all the functions that were crucial to our analysis.
  
  
# Introdutions to the directories
1. Steam Scraper Master
contains our scraper that generates the .jl file from steam website based on which we preprocess and analyze the data. 
NOTE: It is not integral to run this scraper again to make our .jl file (as it will take several days), but you are welcome
to look through the directory and its README.md for more information about it.

2. Trash
Leftover code from our analysis after consilidating our programs into a final submission. Again, not neccessary to the final project but you are welcome to look through it 


# Modules
A full list of modules we used [If you are missing any of the following run “pip install [module_name]” to install these modules]:
wordcloud
chartify
matplotlib
zipfile
ast
re
json
numpy
string
pandas
IPython.display -> display
IPython.display -> HTML


# Python files:
- Counts_genres_in_publisher.py
- plot_functions_top_1000.py
- processing_functions_for_plots as processing.py 
- DATA_PROCESSING.py
- Text_cloud.py


# Additional files:
- text_reviews.zip: contains the text files of reviews for our text cloud
- products_all.jl: contains all the scraped data for our games. There are over 39k games within this dataset


# Steps to Reproduce
1) Ensure all modules from our list are installed on your local machine
2) Open ECE143_G15_Main.ipynb
3) Run the cell containing the main method

Expected Result: The visuals for our project should display within the notebook


