import wikipedia as pywikibot
import pagegenerators as pg
import pywikibot.exceptions as pyWikiExceptions
import pdb
import re
import json

okazu_search = re.compile('http://www.akitashoten.co.jp/CGI/search/syousai_put.cgi?key=search&isbn=(?P<isbn>\d{6}) ')
old_string = 'http://www.akitashoten.co.jp/CGI/search/syousai_put.cgi?key=search&isbn='
new_string = 'http://www.akitashoten.co.jp/comics/4253'
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
    elif "archive" in page_title:
        print "%s is an archived page, not changing" % page_title
        return
    elif "Articles for deletion" in page_title:
        print "%s is an AfD page, not changing" % page_title
        return
    page_text = this_page.get()
    page_text = page_text.replace(old_string,new_string)
    this_page.put(page_text,
        comment='HasteurBot 11: Akita Shoten site restructuring replacement',
        minorEdit=False
    )
def find_pages():
    genFactory = pg.GeneratorFactory()
    genFactory.handleArg("-weblink:http://www.akitashoten.co.jp/CGI/search/syousai_put.cgi?key=search&isbn=")
    #genFactory.handleArg("-namespace:'0,1,4,5'")
    gen = genFactory.getCombinedGenerator()
    if gen:
        for page in gen:
            evaluatePage(page)

def main(*args):
    find_pages()
if __name__=="__main__":
    main()
