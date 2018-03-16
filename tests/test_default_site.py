
from tempfile import mkdtemp
from time import sleep
from shutil import rmtree
from multiprocessing import Process
import unittest

try: from pathlib import Path
except ImportError: from pathlib2 import Path
from requests import get

from dds import bootstrap, server

class TestSiteBootstrap(unittest.TestCase):

    def test_bootstrapping_site(self):
        # make the site
        workingD = mkdtemp()
        workingD = Path(workingD).resolve()
        siteDir = workingD.joinpath('site-1')
        bootstrap.bootstrap_site(siteDir)

        # run the site and fork it off
        config_file = siteDir.joinpath('server_config.json')
        p = Process(target=server.run_server, args=(config_file,))
        p.start()
        sleep(5)  # let the server spin up

        # try and pull the index page
        resp = get('http://127.0.0.1:8001/index.html')
        assert(resp.status_code in range(200, 300))

        # kill the server
        p.terminate()
        rmtree(str(siteDir))

if __name__ == '__main__':
    unittest.main()