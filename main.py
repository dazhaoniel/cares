import re
# import sys
import requests
from flask import Flask, request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__)

rlc_regex = 'rescue-good-food-becoming-waste'

coalition_regex = 'mobilize-get-food-hungry-people'

base_url = 'https://www.newyorkcares.org'

login_url = '/user'

# Create the payload
payload = {
    'name':'',
    'pass':'',
    'form_id': 'user_login',
    'op': 'Log in'
}

def sign_up(
    is_coalition=False, 
    is_rlc=False
    ):
    with requests.Session() as s:
        # Get the page first for https
        s.get(urljoin(base_url, login_url))

        # Post the payload to the site to log in
        post = s.post(urljoin(base_url, login_url), data=payload)

        # Navigate to the project listings page
        l = s.get('https://www.newyorkcares.org/search/projects/results?location=496')

        soup = BeautifulSoup(l.text, 'html.parser')

        # Get last page
        last_page_url = soup.find('a', class_='last')['href']

        last_page = s.get(urljoin(base_url, last_page_url))

        soup = BeautifulSoup(last_page.content, 'html.parser')

        # Find Coalition
        if is_coalition:
            project_link = soup.find('a', 
            href=re.compile(r'.*'+coalition_regex+'*')
        )
        # Find RLC
        elif is_rlc:
            project_link = soup.find('a', 
            href=re.compile(r'.*'+rlc_regex+'*')
        )

        proj = project_link.find_parent('div', class_='project')

        proj_signup_link = proj.find('div', class_='sign-up').find('a')['href']

        success = s.get(urljoin(base_url, proj_signup_link))

        # print(success)

@app.route('/projects/coalition', methods=['GET'])
def get_coalition():
    sign_up(True, False)
    return ('Signed up Coalition', 200)


@app.route('/projects/rlc', methods=['GET'])
def get_rlc():
    sign_up(False, True)
    return ('Signed up RLC', 200)


@app.route('/', methods=['GET'])
def hello_world():
    return ('Hello World!', 200)

# def main():
#     is_coalition = False
#     is_rlc = False

#     if len(sys.argv) != 2:
#         sys.exit('Add project name to sign up for')
#     elif bool(re.match('coalition', sys.argv[1])):
#         is_coalition = True
#     elif bool(re.match('rlc', sys.argv[1])):
#         is_rlc = True
#     else:
#         sys.exit()

#     sign_up(is_coalition, is_rlc)


if __name__ == '__main__':
    app.run(debug=True)






