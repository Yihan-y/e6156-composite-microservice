class Base(object):
    BOOKMARK_URL = 'http://18.118.156.69.nip.io:5000'
    POST_URL = 'http://3.141.31.120.nip.io:5000'
    USER_URL = 'http://18.117.179.170.nip.io:5000'


class Test(Base):
    BOOKMARK_URL = ''
    POST_URL = ''
    USER_URL = ''


class Dev(Base):
    BOOKMARK_URL = ''
    POST_URL = ''
    USER_URL = ''


class Pro(Base):
    BOOKMARK_URL = ''
    POST_URL = ''
    USER_URL = ''
