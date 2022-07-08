import re
import requests
from bs4 import BeautifulSoup
import html

# Configuration
github_url = "https://github.com/HeroBuzz/herobuzz.github.io/tree/main/_posts"
github_news_url = (
    "https://raw.githubusercontent.com/HeroBuzz/herobuzz.github.io/main/_posts/"
)


def get_url(url):
    result = requests.get(url)
    return result.text


def get_newsletter_filename(url):

    result = get_url(url)

    # Parse the file names
    soup = BeautifulSoup(result, "html.parser")
    md_files = soup.find_all(title=re.compile("\.md$"))

    # Iterate the list to the the proper name
    filename_list = []
    for i in md_files:
        filename_list.append(i.extract().get_text())

    # Now we have a list with names and it's fortunately already ordered by name
    # So we just need to get the latest one
    return filename_list[-1]


def get_newsletter_title_and_test(url, filename):
    result = get_url(url + filename)
    convertkit_regex = '^link: "(.*)"$'
    convertkit_url = re.findall(convertkit_regex, result, re.MULTILINE)[0]

    # Convert kit time
    result = get_url(convertkit_url)

    # We have html, let's get the title
    soup = BeautifulSoup(result, "html.parser")

    title = soup.find("title").string

    iframe = soup.find("iframe")["srcdoc"]

    soup = BeautifulSoup(html.unescape(iframe), "html.parser")

    return title, soup.get_text()


filename = get_newsletter_filename(github_url)
_, text = get_newsletter_title_and_test(github_news_url, filename)
print(text)
