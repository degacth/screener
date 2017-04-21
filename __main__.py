import os
from contextlib import contextmanager
from urllib.parse import urlparse

import click
from selenium import webdriver
from shutil import rmtree

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from config import get_config

BASE_DIR = os.path.dirname(__file__)


class Screener:
    __config = None
    __driver = webdriver.PhantomJS()
    __screens_base_dir = os.path.join(BASE_DIR, 'screens')
    __screen_directory = None

    def __init__(self, config_name: str):
        # init config
        self.__config = get_config(config_name)
        assert self.__config is not None, 'Can`t find config with name "%s"' % config_name

        # init screens dir
        self.__screen_directory = os.path.join(self.__screens_base_dir, config_name)
        try:
            os.stat(self.__screen_directory)
            rmtree(self.__screen_directory)
        except:
            pass
        finally:
            os.mkdir(self.__screen_directory)

        # driver settings
        self.__driver.implicitly_wait(10)
        self.__driver.maximize_window()

    def run(self):
        print('\r'.join(
            tuple(map(self.__make_screen, self.__config.get_urls()))
        ))

    def __make_screen(self, url: str):
        drv = self.__driver
        drv.get(url)
        parsed_url = urlparse(url)
        hostname, path = parsed_url.hostname, parsed_url.path
        screen_name = '%s%s.png' % (hostname, path.replace('/', '.'))
        drv.save_screenshot(os.path.join(self.__screen_directory, screen_name))
        return screen_name

    @classmethod
    @contextmanager
    def wait_for_page_load(cls, timeout=30):
        """ Check when page was reloaded """
        old_page = cls.__driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(cls.__driver, timeout).until(staleness_of(old_page))


@click.command()
@click.option('--config', '-c', prompt='You must input config', help='config for screener subclass of base config')
def run(config):
    """ Screener runner """
    screener = Screener(config)
    screener.run()


if __name__ == '__main__': run()
