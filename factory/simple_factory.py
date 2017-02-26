from httplib2 import HTTPConnectionWithTimeout
from ftplib import FTP


class SimpleFactory(object):
    @staticmethod
    def build_connection(protocol):
        if protocol == 'http':
            return HTTPConnectionWithTimeout
        elif protocol == 'ftp':
            return FTP
        else:
            raise RuntimeError('Unknown protocol')

if __name__ == '__main__':
    protocol = input('Which Protocol to use? (http or ftp): ')
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connect()
    print(protocol.get_response())
