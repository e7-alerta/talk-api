from requests.exceptions import HTTPError, ConnectionError, TooManyRedirects, Timeout

import requests as requests

from chatwoot import ChatwootParams
from chatwoot.constants import BASE_URL, API_VERSION, HASBRO, USER_EMAIL


class AuthClient:

    def __init__(self, session: requests.Session, chatwoot_params: ChatwootParams):
        self.session = session
        self.base_url = chatwoot_params.base_url
        pass

    def login(self, email, password):
        """
        :return:
        """
        try:
            print("AuthClient.login | ", email, password, f"{BASE_URL}/auth/sign_in")
            response = self.session.post(f"{BASE_URL}/auth/sign_in", json={
                 "email": email,
                 "password": password
            })
            if response.status_code == 200:
                print("AuthClient.login | response.status_code == 200 ", response.json())
                return response.json()
            else:
                print("AuthClient.login | response.status_code != 200", response.status_code)
                print(response.json())
                return None
        except (HTTPError, ConnectionError, Timeout, TooManyRedirects) as e:
            print("AuthClient.login | error ", e)
            return None
        pass

    def logout(self, user):
        """
        :return:
        """
        try:
            response = self.session.delete(f"{BASE_URL}/{API_VERSION}/auth/sign_out")
            if response.status_code == 200:
                return response.json()
            else:
                print("AuthClient.logout | response.status_code != 200", response.status_code)
                return None
        except (HTTPError, ConnectionError, Timeout, TooManyRedirects) as e:
            print("AuthClient.logout | error ", e)
            return None
        pass
