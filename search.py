#!/usr/bin/python
# encoding: utf-8

import sys
import urllib
import re
import htmlentitydefs

from hashlib import md5
from workflow import web, Workflow, ICON_WEB
from bs4 import BeautifulSoup as BS
from bs4 import Tag

USER_AGENT = 'Alfred-Docker-Hub/{version} (https://github.com/motty/alfred-docker-hub)'

log = None

def main(wf):
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None
    
    url = "https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=" + query + "&starCount=0"
    log.debug(url)
        
    user_agent = USER_AGENT.format(version=wf.version)
    log.debug(user_agent)

    r = web.get(url, headers={'User-Agent': user_agent})
    r.raise_for_status()

    soup = BS(r.content, b'html5lib')
    repositories = soup.find_all("a", class_="RepositoryListItem__flexible___3R0Sg")
    # log.debug(repositories)
    
    for repository in repositories:
        repository = "https://hub.docker.com" + repository["href"]
        wf.add_item(title=repository,
                     subtitle=repository,
                     arg=repository,
                     valid=True,
                     icon=ICON_WEB)

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))