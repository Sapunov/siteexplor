"""
Sitexplor exceptions
"""


class SchemeRequired(Exception):
    def __init__(self):
        Exception.__init__(self, "Write url with http or httpd scheme")


class PageNotAvailible(Exception):
    def __init__(self, site, msg):
        Exception.__init__(
            self, "Sorry, {0} now is not availible. Error: {1}".format(
                site, msg))


class IncorrectDomainName(Exception):
    def __init__(self, domain):
        Exception.__init__(self, "Domain: %s is invalid." % domain)


class Empty(Exception):
    def __init__(self):
        Exception.__init__(self)
