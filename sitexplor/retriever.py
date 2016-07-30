"""
Sitexplor retriever
"""

import logging
import os
import requests
import time

from bs4 import BeautifulSoup
import multiprocessing

from sitexplor import common
from sitexplor import exceptions
from sitexplor import settings
from sitexplor.core import set_logger

set_logger()

LOG = logging.getLogger(".".join([settings.PROGRAM_NAMESPACE, __name__]))


def error(error_obj):
    LOG.error(error_obj)

    raise error_obj


class Retriever(object):
    def __init__(self, url, debug=False, n_proc=10):
        if debug:
            settings.DEBUG = True

        self.n_proc = n_proc if n_proc is not None else 10
        self.queue = multiprocessing.Queue()
        self.processes = []

        self.lock = multiprocessing.Lock()

        manager = multiprocessing.Manager()
        self.links = manager.dict()

        scheme, domain, _ = common.canonize(url)

        if domain != "":
            scheme, domain = common.test_url(scheme, domain)
        else:
            error(exceptions.IncorrectDomainName(domain))

        self.scheme = scheme
        self.domain = domain

        self._new_item(
            common.link_hash(scheme, domain),
            common.make_url(scheme, domain)
        )

        msg = "- Retriever initilized.\n"
        msg += "- Scheme: {0}, Domain: {1}, Max_processes: {2}".format(
            scheme, domain, self.n_proc)
        print msg

    def _relink(self, link_tuple):
        static_files = ["jpg", "png", "pdf", "css", "js", "bmp", "jpeg"]

        domain = link_tuple[1] if link_tuple[1] != "" else self.domain
        if domain != self.domain:
            return False

        for st in static_files:
            if link_tuple[2].endswith("." + st):
                return False

        return common.make_url(link_tuple[0], domain, link_tuple[2])

    def _new_item(self, key, url, state="unwatched"):
        self.links[key] = {
            "url": url,
            "state": state
        }

    def _state_item(self, key, state="watched"):
        if key in self.links:
            self._new_item(key, self.links[key]["url"], state="watched")

    def _explore(self, key, url):
        try:
            res = requests.get(url)
        except requests.exceptions.ConnectionError:
            LOG.error("Page %s is not availible" % url)

        try:
            soup = BeautifulSoup(res.text, "lxml")
        except Exception as e:
            LOG.error(e)
            self._state_item(key)
            return False

        links = soup.find_all("a", href=True)

        self._state_item(key)

        if len(links) > 0:
            for link in links:
                u = self._relink(common.canonize(link["href"]))
                if u:
                    url_hash = common.link_hash(u)

                    if url_hash not in self.links:
                        self._new_item(url_hash, u)

    def _get_next_url(self):
        for k, v in self.links.items():
            if v["state"] == "unwatched":
                self._state_item(k, state="busy")
                return k, v["url"]

        raise exceptions.Empty

    def explore(self, num):
        print "% Process {0} started".format(num)
        try:
            count = 0
            while True:
                try:
                    next_key, next_url = self._get_next_url()

                    count = 0

                    print "+ ({0:02d}) ({2:02d}) {1}".format(
                        num, next_url, len(self.links))
                    self._explore(next_key, next_url)
                except exceptions.Empty:
                    if count < 10:
                        time.sleep(1)
                        count += 1
                    else:
                        print "% Process {0} stoped _empty".format(num)
                        break
        except Exception as e:
            print "% Process {0} stoped {1}".format(num, e.message)

    def _get_export_file(self):
        name = self.domain + ".sitemap"
        name_path = os.path.join(settings.SITES_DIR, name)

        if os.path.exists(name_path):
            os.rename(name_path, name_path + ".old")

        return name_path

    def multi(self):
        for n in xrange(self.n_proc):
            self.processes.append(
                multiprocessing.Process(target=self.explore, args=(n,))
            )
            self.processes[-1].start()

        while len(self.processes) > 0:
            for proc in self.processes:
                if not proc.is_alive():
                    proc.join()
                    self.processes.remove(proc)

            time.sleep(0.1)

        self.stop()

    def stop(self):
        print "- Stopping Retriever..."

        while len(self.processes) > 0:
            print "- Waiting for stop all processes"
            for proc in self.processes:
                proc.terminate()
                self.processes.remove(proc)

        export_file = self._get_export_file()
        with open(export_file, "w") as fid:
            for i in self.links.values():
                fid.write(i["url"] + "\n")

        print "- Export to {} completed".format(export_file)

        if not settings.DEBUG:
            print "- Start uniqueze files"
            common.uniqueze_file(settings.URLS_FILE)
