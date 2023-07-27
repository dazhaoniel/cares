import re
import requests
from flask import Flask
from urllib.parse import urljoin
from bs4 import BeautifulSoup

app = Flask(__name__)

RLC = "rescue-good-food-becoming-waste"

COALITION = "staff-mobile-soup-kitchen"

BASE_URL = "https://www.newyorkcares.org"

LOGIN_URL = "/user"

# Create the payload
payload = {
    "name": "",
    "pass": "",
    "form_id": "user_login",
    "op": "Log in",
}


def login():
    """Login New York Cares and return the current session"""
    with requests.Session() as s:
        # Get the page first for https
        s.get(urljoin(BASE_URL, LOGIN_URL))

        # Post the payload to the site to log in
        s.post(urljoin(BASE_URL, LOGIN_URL), data=payload)
    return s


def signup_project(session, project):
    """Sign up the project with the correct regex matching"""
    listing = session.get(
        "https://www.newyorkcares.org/search/projects/results?location=496"
    )

    soup = BeautifulSoup(listing.text, "html.parser")

    # Go to the last page
    last_page_url = soup.find("a", class_="last")["href"]

    last_page = session.get(urljoin(BASE_URL, last_page_url))

    soup = BeautifulSoup(last_page.content, "html.parser")

    project_links = soup.findAll("a", href=re.compile(r".*" + project + "*"))

    # Find the correct project
    for link in project_links:
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


@app.route("/projects/coalition", methods=["GET"])
def get_coalition():
    """Sign up Coalition for the homeless"""
    s = login()
    signup_project(s, COALITION)
    return ("Signed up Coalition", 200)


@app.route("/projects/rlc", methods=["GET"])
def get_rlc():
    """Sign up Rescue Leftover Cuisine"""
    s = login()
    signup_project(s, RLC)
    return ("Signed up RLC", 200)


@app.route("/", methods=["GET"])
def hello_world():
    """Test route for the API"""
    return ("Hello World!", 200)


def main():
    s = login()
    signup_project(s, COALITION)


if __name__ == "__main__":
    # app.run(debug=True)
    main()
