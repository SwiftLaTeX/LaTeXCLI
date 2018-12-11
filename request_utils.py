import requests
import logging



def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True, timeout=5)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        logging.error("Link %s has a TEXT mime type" % url)
        return False
    if 'html' in content_type.lower():
        logging.error("Link %s has a HTML mime type" % url)
        return False
    content_length = header.get('content-length', None)
    if content_length is None or int(content_length) > 2e7:
        logging.error("Link %s has a dirty content_length" % url)
        return False

    return True

def get_remote_file(url, dest):
    try:
        if is_downloadable(url):
            r = requests.get(url, allow_redirects=True, timeout = 10)
            with open(dest, 'wb') as fb:
                fb.write(r.content)
            return True
        else:
            return False
    except:
        logging.error("Link %s downloaded failed" % url)
        return False