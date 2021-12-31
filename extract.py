import requests
from bs4 import BeautifulSoup

# Fungsi scrapping_web
def scraping_web(url, page):
    """
    Fungsi untuk scraping data berdasarkan nomor halaman
    
    param page int: nomor halaman web
    """
    
    url = f"{url}{page}"
    return requests.get(url).text


# get html content
def get_html_content(url, pages):
    html_content = ""
    for page in range(1, pages+1):
        temp = scraping_web(url, page)
        html_content += temp
    return html_content


# extract html content
def extract_html_content(url, pages, parser_type):
    html_content = get_html_content(url, pages)
    return BeautifulSoup(html_content, parser_type)


# get elemen function
def get_elemen(tag, parsed_content, class_name=None):
    elements = parsed_content.find_all(tag, class_ = class_name)
    
    list_elements = []
    
    for element in elements:
        list_elements.append(element.text)
    
    return list_elements