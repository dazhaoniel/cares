import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

rlc_regex = 'rescue-good-food-becoming-waste'

coalition_regex = 'mobilize-get-food-hungry-people'

base_url = 'https://www.newyorkcares.org'

login_url = '/user'

# Create the payload
payload = {
    'name':'danielantoiny@gmail.com',
    'pass':'M1xQhG#SizxZy^NsF573',
    'form_id': 'user_login',
    'op': 'Log in'
}

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

    rlc = soup.find('a', href=re.compile(r'.*deliver-lunch-seniors*'))

    proj = rlc.find_parent('div', class_='project')

    proj_signup_link = proj.find('div', class_='sign-up').find('a')['href']

    success = s.get(urljoin(base_url, proj_signup_link))

    # print(success)








