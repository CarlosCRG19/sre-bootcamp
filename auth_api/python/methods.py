import jwt
import hashlib
import pandas as pd
import mysql.connector
from hmac import compare_digest


class Token:

    def __init__(self, secret):
        self.secret = secret

    def generate_token(self, username, password):
        """
        Generates the JWT token using the user's role in the payload
        :return: string
        """
        # Create connection with database
        db_connection = mysql.connector.connect(
            host='bootcamp-tht.sre.wize.mx',
            user='secret',
            password='noPow3r',
            database='bootcamp_tht'
        )

        # Get specified user from database
        query = "SELECT * FROM users WHERE username='{}'".format(username)

        # Check if user was found in database
        try:
            user_data = pd.read_sql(sql=query, con=db_connection).iloc[0]
        except IndexError:
            return None

        # Verify user credentials using static method
        if Authorization.verify_login(username, password, user_data):
            # If credentials are valid, generate token using PyJWT
            role = user_data.role
            token = jwt.encode(
                payload={"role": role},
                key=self.secret,
                algorithm="HS256"
            )
            # Return generated token
            return token
        else:
            # Otherwise, return None
            return None


class Restricted:

    def __init__(self, secret):
        self.secret = secret

    def access_data(self, authorization):
        """
        Verifies that the JWT was created with the given secret and the HS256 alg.
        :return: string  
        """
        # Try to decode JWT using secret
        try:
            jwt.decode(authorization, key=self.secret, algorithms=["HS256", ])
        except jwt.exceptions.InvalidSignatureError:
            # If verification fails, return "Unauthenticated"
            return "Unauthenticated"

        return "You are under protected data"


class Authorization:

    @staticmethod
    def verify_login(username, password, user_data):
        """
        Verifies that login credentials are correct
        :return: boolean (if credentials are valid)
        """
        # Encode password using salt
        salted_password = password + user_data.salt
        encoded_password = hashlib.sha512(salted_password.encode()).hexdigest()

        # Verify if encoded password corresponds to user's password in the database
        # will return True if password is correct
        return compare_digest(encoded_password, user_data.password)
