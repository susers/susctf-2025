import requests
import functools

original_get = requests.get
original_post = requests.post
original_put = requests.put


def patched_get(*args, **kwargs):
    response = original_get(*args, **kwargs)
    if response.status_code != 200:
        raise requests.HTTPError(response.text)
    return response


def patched_post(*args, **kwargs):
    response = original_post(*args, **kwargs)
    if response.status_code != 200:
        raise requests.HTTPError(response.text)
    return response


def patched_put(*args, **kwargs):
    response = original_put(*args, **kwargs)
    if response.status_code != 200:
        raise requests.HTTPError(response.text)
    return response


def raise_for_status(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        requests.get = patched_get
        requests.post = patched_post
        requests.put = patched_put
        try:
            return func(*args, **kwargs)
        finally:
            # Restore original methods to avoid side effects
            requests.get = original_get
            requests.post = original_post
            requests.put = original_put

    return wrapper
