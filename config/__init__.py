from abc import ABCMeta, abstractmethod
from typing import Iterable


class BaseConfig(metaclass=ABCMeta):
    @abstractmethod
    def get_urls(self) -> Iterable: """ collection of urls for screens """


class SampleConfig(BaseConfig):
    __host = 'https://ya.ru'

    def get_urls(self): return map(lambda url: '%s%s' % (self.__host, url), (
        '/',
    ))


def get_config(name: str) -> BaseConfig:
    return _configs.get(name)


_configs = {
    'sample': SampleConfig(),
}
