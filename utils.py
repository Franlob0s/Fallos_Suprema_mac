"""
UTILS
"""
import os
import requests
import cgi
import re
import time
#from win32com import client

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_immediate_files(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]

def get_extension(url):
    """
    return extension of file
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    value, params = cgi.parse_header(header['Content-Disposition'])
    filename = params["filename"]
    return filename.split(".")[1]

def convert_to_pdf(file_path):
    pass
    #if file_path.endswith(".docx") or file_path.endswith(".doc"):
        #word = client.DispatchEx("Word.Application")
        #try:
            #new_path = re.sub(r"(.doc)|(.docx)", ".pdf", file_path)
            #print("Convert " + file_path + " to " + new_path)
            #in_file = os.path.abspath(file_path)
            #new_file = os.path.abspath(new_path)
            #doc = word.Documents.Open(in_file)
            #doc.SaveAs(new_file, FileFormat = 17)
            #doc.Close()
        #except Exception as e:
            #print(e)
        #finally:
            #word.Quit()
    #else:
        #print("File extension of file '" + file_path + "' cannot be converted yet. Ask to the programmer")

class wait_for_page_load(object):
  def __init__(self, browser):
    self.browser = browser
  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')
  def page_has_loaded(self):
    new_page = self.browser.find_element_by_tag_name('html')
    return new_page.id != self.old_page.id
  def __exit__(self, *_):
    wait_for(self.page_has_loaded)

def wait_for(condition_function):
  start_time = time.time()
  while time.time() < start_time + 3:
    if condition_function():
      return True
    else:
      time.sleep(0.1)
  raise Exception('Timeout waiting for {}'.format(condition_function.__name__))





