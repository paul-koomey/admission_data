from bs4 import BeautifulSoup
import datetime, time
import IPython
import sys, re
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import pandas
import os

# data values will have both GPA and GRE
complete_data = []
# data values will have either GPA, GRE or both
partial_data = []

id = 0

# get the number of files in the data directory
list = os.listdir(os.getcwd() + "/data")
print("there are {0} files in the data directory".format(len(list)))

for year in range(1, len(list) + 1):
  with open('data/{0}.html'.format(year), 'r') as f:
    
    # convert html into soup so it can be parsed
    soup = BeautifulSoup(f.read(), features="html.parser")
    results = soup.find(id='results-container')
    
    # get rid of ads
    cols = results.findAll(class_='col')
        
    # weird bug where some pages didn't have 44 items in the list
    if len(cols) == 44:
        cols.pop(43)
        cols.pop(32)
        cols.pop(21)
        cols.pop(10)
    else:
        continue
    
    
    for col in cols:
        
        # variables being parsed
        row = [id]         # id number
        school = None      # university applying to
        degree = None      # Masters or PhD
        decision = None    # Accepted or Rejected
        gpa = None         # 0 to 4.00
        gre = None         # overall score 260 - 340
        gre_q = None       # quant score   130 - 170
        
        # easily pull attributes from the string version of the html
        attributes = str(col.findAll(class_="badge"))
        
        # get the type of degree
        if "Masters" in attributes:
            degree = "Masters"
        elif "PhD" in attributes:
            degree = "PhD"
        
        # get the type of decision
        if "Accepted" in attributes:
            decision = "Accepted"
        elif "Rejected" in attributes:
            decision = "Rejected"
        elif "Interview" in attributes:
            decision = "Interview"
        elif "Wait listed" in attributes:
            decision = "Wait listed"
            
        # get the GPA
        if "GPA" in attributes:
            gpa_i = attributes.find("GPA") + 4
            try:
                if float(attributes[gpa_i:gpa_i+4]) >= 0 and float(attributes[gpa_i:gpa_i+4]) <= 4.3:
                    gpa = attributes[gpa_i:gpa_i+4]
            except:
                gpa = None
                print("incorrect GPA on file", year, ":", attributes[gpa_i:gpa_i+4])
            
        # get the quant GRE score or total GRE score
        if "GRE" in attributes:
            gre_i = attributes.find("GRE") + 4
            gre_score = attributes[gre_i:gre_i+3]
            try:
                if int(gre_score) >= 130 and int(gre_score) <= 170:
                    gre_q = gre_score
                if int(gre_score) >= 260 and int(gre_score) <= 340:
                    gre = gre_score
            except:
                gre = None
                print("incorrect GRE on file", year, ":", gre_score)
        
        # get the school
        col = str(col)
        school = col[col.find(",") + 2:col.find("<s") - 2]
        
        
        if id and school and degree and (gpa or gre_q) and decision:
            partial_data.append([id, school, degree, gpa, gre_q, decision])
            if gpa and gre_q:
                complete_data.append([id, school, degree, gpa, gre_q, decision])
        
        id += 1
        
    print(year)

partial_df = pandas.DataFrame(partial_data)
partial_df.to_csv('cs_partial.csv')

complete_df = pandas.DataFrame(complete_data)
complete_df.to_csv('cs_complete.csv')
