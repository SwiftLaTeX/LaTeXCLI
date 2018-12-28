import string
import random
import hashlib
import re
import config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "pdf"


def gen_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=N))


def hash_filename(name):
    hash_object = hashlib.md5(name.encode())
    return hash_object.hexdigest()


def is_secure_filename(name):
    if not bool(re.match(r'^[a-zA-Z\-\.\d\/\-]+$', name)):
        return False

    if ".." in name or "//" in name:
        return False

    if name.startswith("/") or name.startswith("."):
        return False

    return True



def is_valid_sessionid(sessionid):
    if len(sessionid) != config.SESSION_LENGTH:
        return False

    if not bool(re.match(r'^[a-zA-Z\d]+$', sessionid)):
        return False

    return True