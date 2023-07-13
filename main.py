import re
import sys
import requests
from flask import Flask, request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__)

rlc_regex = "rescue-good-food-becoming-waste"

coalition_regex = "staff-mobile-soup-kitchen"

base_url = "https://www.newyorkcares.org"

login_url = "/user"

# Create the payload
payload = {
    "name": "",
    "pass": "",
    "form_id": "user_login",
    "op": "Log in",
}


def sign_up(is_coalition=False, is_rlc=False):
    with requests.Session() as s:
        # Get the page first for https
        s.get(urljoin(base_url, login_url))

        # Post the payload to the site to log in
        s.post(urljoin(base_url, login_url), data=payload)

        # Navigate to the project listings page
        l = s.get("https://www.newyorkcares.org/search/projects/results?location=496")

    soup = BeautifulSoup(l.text, "html.parser")

    # Go to the last page
    last_page_url = soup.find("a", class_="last")["href"]

    last_page = s.get(urljoin(base_url, last_page_url))

    soup = BeautifulSoup(last_page.content, "html.parser")

    # Find Coalition
    if is_coalition:
        project_link = soup.find("a", href=re.compile(r".*" + coalition_regex + "*"))

    # Find RLC
    elif is_rlc:
        project_link = soup.findAll("a", href=re.compile(r".*" + rlc_regex + "*"))

        # Find the Usq project
        for link in project_link:
            if link.find_parent("div", class_="project").find(
                string=re.compile(".*Union Square.*")
            ):
                project_link = link
                break

    while not project_link and soup.find("a", class_="prev"):
        prev = soup.find("a", class_="prev")["href"]

        prev_page = s.get(urljoin(base_url, prev))

        soup = BeautifulSoup(prev_page.content, "html.parser")

        # Find Coalition
        if is_coalition:
            project_link = soup.find(
                "a", href=re.compile(r".*" + coalition_regex + "*")
            )

        # Find RLC
        elif is_rlc:
            project_link = soup.findAll("a", href=re.compile(r".*" + rlc_regex + "*"))

            # Find the Usq project
            for link in project_link:
                if link.find_parent("div", class_="project").find(
                    string=re.compile(".*Union Square.*")
                ):
                    project_link = link
                    break

        else:
            pass

    if not project_link:
        return

    # sign up
    proj = project_link.find_parent("div", class_="project")

    proj_signup_link = proj.find("div", class_="sign-up").find("a")["href"]

    success = s.get(urljoin(base_url, proj_signup_link))

    print(success)


# @app.route('/projects/coalition', methods=['GET'])
def get_coalition():
    sign_up(True, False)
    return ("Signed up Coalition", 200)


# @app.route('/projects/rlc', methods=['GET'])
def get_rlc():
    sign_up(False, True)
    return ("Signed up RLC", 200)


# @app.route('/', methods=['GET'])
def hello_world():
    return ("Hello World!", 200)


def main():
    is_coalition = False
    is_rlc = True

    if len(sys.argv) != 2:
        sys.exit("Add project name to sign up for")
    elif bool(re.match("coalition", sys.argv[1])):
        is_coalition = True
    elif bool(re.match("rlc", sys.argv[1])):
        is_rlc = True
    else:
        sys.exit()

    sign_up(is_coalition, is_rlc)


if __name__ == "__main__":
    # app.run(debug=True)
    main()
