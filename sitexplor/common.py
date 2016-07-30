"""
Sitexplor common functions
"""

import logging
import os
import re
import requests

from hashlib import sha1
from psh import sh

from sitexplor import exceptions
from sitexplor import settings

LOG = logging.getLogger(".".join([settings.PROGRAM_NAMESPACE, __name__]))


def error(error_obj):
    LOG.error(error_obj)

    raise error_obj


def make_url(scheme, domain, rest=""):
    return "%s://%s%s" % (scheme, domain, rest)


def add_to_url_database(url, url_tuple):
    with open(settings.URLS_FILE, "a") as fid:
        fid.write("{0} [{1}, {2}, {3}]\n".format(
            url, url_tuple[0], url_tuple[1], url_tuple[2])
        )


def delete_empty(li):
    return filter(lambda x: x != "", li)


def get_first(li):
    iterable = (list, tuple, set)
    if isinstance(li, iterable):
        if len(li) > 0:
            if isinstance(li[0], iterable):
                return get_first(li[0])
            else:
                return li[0]
        else:
            return li
    else:
        return li


def left_slash(string):
    parts = string.split("/")
    if not re.match("^([A-Za-z0-9-_\.]*?)$", parts[0]):
        parts.pop(0)
    url = "/".join(delete_empty(parts))
    return "/" + url if url != "" else ""


def delete_url_hash(string):
    return string.split("#")[0]


def canonize(url):
    # perm_url = url
    regexps = [
        r"^(http[s]?://).*?",
        r"^((www\.)?[A-Za-z0-9\-\.]*\.[A-Za-z]{2,})"
    ]
    result = []
    for rexp in regexps:
        res = delete_empty(re.findall(rexp, url))
        if len(res) > 0:
            result.append(get_first(res))
            url = re.sub(rexp, "", url)
        else:
            result.append(False)
    result.append(url)

    # print perm_url, result

    scheme = "http" if not result[0] else result[0][:-3]
    domain = result[1].strip("/") if result[1] else ""
    rest = left_slash(delete_url_hash(result[2]))

    return scheme, domain, rest


def link_hash(scheme, domain=None, rest=None):
    if domain is None and rest is None and scheme != "":
        url = scheme
        return sha1(url).hexdigest()
    else:
        if domain is None:
            error(exceptions.IncorrectDomainName(domain))
        rest = rest if rest is not None else ""

        return sha1(make_url(scheme, domain, rest)).hexdigest()


def test_url(scheme, domain):
    site = make_url(scheme, domain)
    try:
        res = requests.head(site)
    except requests.exceptions.ConnectionError as e:
        error(exceptions.PageNotAvailible(site, e.message))

    if res.is_redirect:
        if "Location" in res.headers:
            scheme, domain, r = canonize(res.headers["Location"])

    return scheme, domain


def uniqueze_file(filename):
    if not os.path.exists(filename):
        return False

    LOG.info("Make %s unique" % filename)

    tmp_file = filename + ".tmp"
    process = sh.sort(filename) | sh.uniq()
    try:
        with open(tmp_file, "w") as fid:
            fid.write(process.execute().stdout())
    except Exception as e:
        LOG.error(e)
        return False

    sh.mv(tmp_file, filename).execute()
