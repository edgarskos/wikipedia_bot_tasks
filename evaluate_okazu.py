import wikipedia as pywikibot
import pagegenerators as pg
import pywikibot.exceptions as pyWikiExceptions
import pdb
import re
import requests
import json

okazu_search = re.compile('http://okazu.blogspot.com/(?P<year>\d{4})/(?P<month>\d{2})/(?P<title>.*?)\.html')
found_matches = {}
exempt_pages = [ 'Wikipedia:Bot requests'
]

def evaluatePage(this_page):
    print this_page
    page_title = this_page.title()
    if page_title in exempt_pages:
        print "%s is on the exempt list" % page_title
        return
    elif "User" in page_title:
        print "%s is an User page, not changing" % page_title
        return
    elif "Archive" in page_title:
        print "%s is an archived page, not changing" % page_title
        return
    page_text = this_page.get()
    matches = okazu_search.findall(page_text)
    for match in matches:
        fixed_url = lookup_match(match)
        if fixed_url is not None:
            old_url = 'http://okazu.blogspot.com/%s/%s/%s.html' % match
            page_text = page_text.replace(old_url,fixed_url)
    this_page.put(page_text,
        comment='HasteurBot 10: Replacing okazu.blogspot.com refs with yuricon.com equivilants',
        minorEdit=False
    )
def lookup_match(match):
    print match
    compound_key = ''.join(match)
    if found_matches.has_key(compound_key):
        #We've already found this replacement
        return found_matches[compound_key]
    else:
        #Time to look up the replacement from the new site
        for i in range(1,32):
            req_string = 'http://okazu.yuricon.com/'+match[0]+'/'+match[1]+"/%02d/"%i+match[2]+'/'
            r = requests.get(req_string)
            if r.status_code == 200:
                found_matches[compound_key] = req_string
                return req_string
def find_pages():
    genFactory = pg.GeneratorFactory()
    genFactory.handleArg("-weblink:*.okazu.blogspot.com")
    #genFactory.handleArg("-namespace:'0,1,4,5'")
    gen = genFactory.getCombinedGenerator()
    if gen:
        for page in gen:
            evaluatePage(page)

def main(*args):
    find_pages()
if __name__=="__main__":
    main()
