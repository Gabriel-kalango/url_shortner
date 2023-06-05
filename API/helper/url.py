from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
alphabet=['A','B','C','D','E','F','G','H','I','J''K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']