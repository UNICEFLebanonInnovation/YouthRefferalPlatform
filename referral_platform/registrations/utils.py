

def generate_hash(string):
    # https://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/
    # https://stackoverflow.com/questions/3815656/simple-encrypt-decrypt-lib-in-python-with-private-key
    # from Crypto.Hash import SHA256
    # '{0:0>4}'.format(int(hashlib.sha1(full_name.encode('UTF-8')).hexdigest(), 16) % 10000)
    #https://gist.github.com/lkdocs/6519366
    #http://apprize.info/python/example/13.html
    import hashlib

    return hashlib.sha224(string).hexdigest()


def encode_string(string):
    pass


def decode_string(string):
    pass
