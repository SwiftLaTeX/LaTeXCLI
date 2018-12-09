import string
import random
import hashlib


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "pdf"


def gen_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=N))


def hash_filename(name):
    hash_object = hashlib.md5(name.encode())
    return hash_object.hexdigest()
