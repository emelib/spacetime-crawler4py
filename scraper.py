import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup
import requests

# referenced here https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
def scraper(url, resp):
    if resp.status == 200:
        links = extract_next_links(url, resp)
        valid_links = [link for link in links if is_valid(link)]
        for link in valid_links:
            new_resp= requests.get(link)
            if new_resp.status_code == 200:
                soup = BeautifulSoup(new_resp.text, 'xml')
                #add this to a file perhaps and the link it belongs to
                readable_text = soup.get_text()
        return valid_links
    else:
        return []

#referenced this link- https://www.crummy.com/software/BeautifulSoup/bs4/doc/       
def extract_next_links(url, resp):
    next_links = []
    soup = BeautifulSoup(resp.raw_response.content, 'xml')
    all_anchors = soup.findAll('a')
    for anchor in all_anchors:
        link = anchor.get("href")
        if link:
            newLink, fragString = urldefrag(link)
            next_links.append(newLink)
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return next_links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    valid_domains = ("ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu", "today.uci.edu" )
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        for domain in valid_domains:
            if parsed.netloc.endswith(domain):
                if parsed.netloc == "today.uci.edu" and parsed.path != "/department/information_computer_sciences":
                    return False
                return True
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    except TypeError:
        print ("TypeError for ", parsed)
        raise
