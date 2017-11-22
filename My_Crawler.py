import requests
import urllib
from urllib.request import urlopen
from urllib import robotparser
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib import parse
import os

###################### create a file folder for storing the corpus ###########################
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.makedirs(directory)

###################### create files and name them with the url and write the web page content on it ####################
def generate_corpus(url):

    create_project_dir('Corpus')
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        # kill all script, style, link and head elements
        for script in soup(["script", "style", "a", "head"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        if len(text) > 1: # this is trying to avoid the empty file
            file_name = url.split('://') # using the url as the file name
            corpus_file = 'Corpus/' + file_name[1].replace('/', '--').replace('.', '_') + '.txt'
            print(corpus_file)

            with open(corpus_file, 'w', encoding='UTF-8', newline='') as f:
                f.write(text)
    except:
        pass

####################################################################################
def spider(deep):
    links = set()
    subLinks = set()
    urlSet = [
        #'https://www.concordia.ca/artsci/students/associations.html',
        #'https://csu.qc.ca/content/student-groups-associations',
        #'http://www.cupfa.org',
        'http://cufa.net'
    ]
    for urls in urlSet:
        links.add(urls)  # add 4 initial urls into a set
    print("=================================================================================================")
    print("Crawling the 1 layer")
    for link in links:
        rp = robotparser.RobotFileParser()
        rp.set_url(link)
        rp.read()
        permission = rp.can_fetch("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36",link)
        if permission == True:  # if is allowed by the robot parser

            # write the initial 4 web pages' contents onto the txt files
            generate_corpus(link)
    depth = deep
    layer = 1
    while depth > 0:
        layer += 1
        print("==================================================================================================")
        print("Crawling the {}".format(layer)+ " layer")
        # include garbage information in the url
        badHref = {'#', 'javascript:void(0)', 'tel:', 'telnet', 'mailto', "%s' %", 'whatsapp', 'http://bsaconcordia.ca', 'youtube', 'twitter', 'instagram', 'facebook', 'flickr'}
        for link in links:
            domainName = urlparse(link).netloc
            source_code = requests.get(link)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")

            # from the upper level links gather the new links only with the same domain name
            for anchor in soup.findAll('a'):
                href = anchor.get('href')
                if href is not None and not any(bad in href for bad in badHref): # eliminate garbage href
                    url = parse.urljoin(link, href)  # if the value is a relative url than it will combine the base url and the relative page url together
                    result = urlparse(url).netloc
                    try:
                        if result == domainName:
                            if not url.endswith((".pdf", ".jpg", ".png", ".zip", ".gif", ".doc", ".docx", ".xlsx", ".xls")):
                                print( "==================================================================================================")
                                print("Crawling the {}".format(layer) + " layer")
                                print(url + '\n')
                                subLinks.add(url) # add every sublinks which was found in the one more deeper layer
                    except:
                        pass
        links = set() # reset the links set to empty
        if len(subLinks) > 0:
            for link in subLinks:
                rp = robotparser.RobotFileParser()
                rp.set_url(link + "/robots.txt")
                try:
                    rp.read()
                    permission = rp.can_fetch("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36", link)
                    if permission == True: # if is allowed by the robot parser
                        # write the web page content onto the txt file
                        print("==================================================================================================")
                        print("Crawling the {}".format(layer) + " layer")
                        generate_corpus(link)
                except:
                    pass

            links = subLinks
            subLinks = set()
            depth -= 1

########################## function call, if you want to crawl 5 layers then you enter 4 as the parameter because the base layer does not be included in the while loop #############
spider(2)


