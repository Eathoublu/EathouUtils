# coding:utf8
# SocketRequester
import socket


class SocketRequester:
    class Content:
        def __init__(self, raw):
            self.headers = {}
            self.content = ''
            self.raw = raw
            self.__parse()

        def __parse(self):
            lines = self.raw.split('\n')
            headers_len = 0
            for l in lines:
                if l == '\r':
                    break
                self.headers[l.split(':')[0]] = l[len(l.split(':')[0]):]
                headers_len += len(l) + 1
            self.content = self.raw[headers_len:]

    @classmethod
    def get(cls, host, port, url):
        sock = socket.socket()
        sock.connect((host, port))
        request_url = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(url, host)
        sock.send(request_url.encode())
        response = b''
        chunk = sock.recv(1024)
        while chunk:
            response += chunk
            chunk = sock.recv(1024)
        return cls.Content(response)

# Example code
if __name__ == '__main__':
    print(SocketRequester.get('127.0.0.1', 5000, '/').content)

