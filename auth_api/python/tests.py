import unittest
from methods import Token, Restricted


class TestStringMethods(unittest.TestCase):

    # Encryption secret key
    secret = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"

    def setUp(self):
        self.convert = Token(self.secret)
        self.validate = Restricted(self.secret)

    def test_generate_token(self):
        """
        Note: the PyJWT module changes the order of the JSON keys in the header used for the creation of the test JWT ({"alg": "HS256", "typ": "JWT"} to {"typ": "JWT", "alg": "HS256"})
        - this does change the generated token string. But in a real case the token will work even though it looks different, since the receiver
        will use the secret to decode the token and even though the headers or payload are in different order, the end result is the same.
        """
        self.assertEqual('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w',
                         self.convert.generate_token('admin', 'secret'))

    def test_access_data(self):
        self.assertEqual('You are under protected data', self.validate.access_data(
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'))


if __name__ == '__main__':
    unittest.main()
