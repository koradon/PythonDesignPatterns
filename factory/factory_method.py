import abc
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulStoneSoup


class Connector(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self, content):
        """
        Redefined in the runtime
        :return:
        """
        pass

    def read(self, host, path):
        """
        Generic method for all classes. Reads web content
        :param host:
        :param path:
        :return:
        """
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print("Connecting to {}".format(url))
        return urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        """
        Factory method. Must be redefined in subclasses.
        :return:
        """
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        """
        Factory method. Must be redefined in subclass.
        :return:
        """
        return FTPPort()


class HTTPConnector(Connector):
    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def parse(self, content):
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPConnector(Connector):
    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


class Port(object):
    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    def __str__(self):
        return '443'


class FTPPort(Port):
    def __str__(self):
        return '21'


if __name__ == "__main__":
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = int(input('Connecting to {}. Which Protocol to use?'
                     '(0-http, 1-ftp):'.format(domain)))

    if protocol == 0:
        is_secure = bool(input('Use secure connection? (1-yes, 0-no): '))
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)

    content = connector.read(domain, path)
    print(connector.parse(content))
    # try:
    #     content = connector.read(domain, path)
    # except URLError:
    #     print("Can not access resource with this method")
    # except Exception:
    #     print("Can not access resource with this method")
    # else:
    #     print(connector.parse(content))
















