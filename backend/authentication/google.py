from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:  # pylint: disable=R0903
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            if "accounts.google.com" not in idinfo["iss"]:
                raise GoogleAuthError("Wrong issuer.")

            return idinfo

        except (ValueError, GoogleAuthError):
            return "The token is either invalid or has expired"
