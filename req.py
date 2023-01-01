import requests
import re
from bs4 import BeautifulSoup
from clint.textui import progress

# Url of the article
article_url = "https://towardsdatascience.com/springer-has-released-65-machine-learning-and-data-books-for-free-961f8181f189"

html_request = requests.get(article_url)
beautifulSoup = BeautifulSoup(html_request.content, "html.parser")

# Regular expression that matches the ISBN
isbn_regex = r'(\d{3}-\d{1}-\d{3}-\d{5}-\d{1})'

# Parsing book anchores using BeautifulSoup
book_links = beautifulSoup.findAll("a", {"class": "cq gv ie if ig ih"})
springer_book_base_url = "http://link.springer.com/openurl?genre=book&isbn="
book_isbns = [l['href'].replace(springer_book_base_url, "") for l in book_links]

# Parsing book titles using BeautifulSoup
book_titles = [p.text for p in beautifulSoup.findAll("strong", {"class": "hl id"})]

print(len(book_titles))
# Downloading books
print("Downloading")
for index, isbn in enumerate(book_isbns):
    download_url = f'https://link.springer.com/content/pdf/10.1007%2F{isbn}.pdf'
    pdf_request = requests.get(download_url, stream=True)
    with open(f'./{book_titles[index]}.pdf', mode='wb') as pdf_file:
        total_length = int(pdf_request.headers.get('content-length'))
        # pdf_file.write(pdf_request.content)
        for ch in progress.bar(pdf_request.iter_content(chunk_size = 1024), expected_size=(total_length/1024) + 1):
            if ch:
                pdf_file.write(ch)
print("Done")
