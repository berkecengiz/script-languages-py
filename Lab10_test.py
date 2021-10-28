import unittest


class Http:

    def __init__(self, method, resource, protocol):
        self.method = method
        self.resource = resource
        self.protocol = protocol

    def toString(self):
        return '{0} {1} {2}'.format(self.method, self.resource, self.protocol)

    def getMethod(self):
        return self.method

    def getResource(self):
        return self.resource


def reqstr2obj(request_string):
    if type(request_string) is not str:
        raise TypeError


class BadRequestTypeError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


def createHTTP(http_request):
    http_info = http_request.split(" ")
    if len(http_info) == 3:
        if http_info[0] not in ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                                'TRACE', 'OPTIONS', 'CONNECT', 'PATCH']:
            raise BadRequestTypeError
        if http_info[1][0] != '/':
            raise ValueError
        if http_info[2] not in ["HTTP1.0", "HTTP1.1", "HTTP2.0"]:
            raise BadHTTPVersion
        else:
            return Http(http_info[0], http_info[1], http_info[2])
    else:
        return None


class MyTests(unittest.TestCase):
    def test_1(self):
        with self.assertRaises(TypeError):
            reqstr2obj(2)

    def test_2(self):
        self.assertIsInstance(createHTTP("GET / HTTP1.1"), Http)

    def test_3(self):
        temp = createHTTP("GET / HTTP1.1")
        self.assertEqual(temp.method, "GET")
        self.assertEqual(temp.resource, "/")
        self.assertEqual(temp.protocol, "HTTP1.1")

    def test_4(self):  # not sure about what question 7 asks??
        request = "GET / HTTP1.1"
        req_info = request.split(" ")
        temp = createHTTP(request)
        self.assertEqual(req_info[0], temp.method)
        self.assertEqual(req_info[1], temp.resource)
        self.assertEqual(req_info[2], temp.protocol)

    def test_5(self):
        self.assertIsNone(createHTTP("GET /"))
        self.assertIsNone(createHTTP("GET HTTP1.1"))
        self.assertIsNone(createHTTP("/Video.mp4"))
        
    def test_6(self):
        with self.assertRaises(BadRequestTypeError):
            createHTTP("DOWNLOAD /movie.mp4 HTTP1.1")

    def test_7(self):
        with self.assertRaises(BadHTTPVersion):
            createHTTP("GET / lol")

    def test_8(self):
        with self.assertRaises(ValueError):
            createHTTP("GET lol HTTP1.1")


if __name__ == "__main__":
    unittest.main()
