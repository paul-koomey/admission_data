import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
from IPython.core.debugger import Tracer
import os


# link to the grad cafe website
url_form = "https://www.thegradcafe.com/survey/?per_page=40&program=Computer+Science&degree=&page={0}"

# get directory where data will be stored
DATA_DIR = os.getcwd() + "/data"


if __name__ == '__main__':
    
  # get number of pages and make the range go to pages - 1
  r = requests.get(url_form.format(1))
  soup = BeautifulSoup(r.text, features="html.parser")
  pages = soup.find(class_="pagination").findAll(class_="page-link")
  max_pages = int(pages[-2].next)
  print("retreiving {0} pages of full content".format(max_pages - 1))
  
  # create folder for data to be stored into
  os.mkdir("data")
  for i in range(1, max_pages):
    
    # get the html for a given page
    url = url_form.format(i)
    r = requests.get(url)
    
    # set the name of the file
    fname = "{data_dir}/{page}.html".format(
      data_dir=DATA_DIR,
      page=str(i)
    )
    
    # write to the file
    with open(fname, 'w') as f:
      f.write(r.text)
    print("getting {0}...".format(i))
