import requests
from bs4 import BeautifulSoup
import json

# URL адреса сайту
base_url = 'http://quotes.toscrape.com'
# Пусті списки для цитат і авторів
quotes = []
authors = []

# Функція для отримання інформації про автора
def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    born_date = soup.find('span', class_='author-born-date').get_text()
    born_location = soup.find('span', class_='author-born-location').get_text()
    description = soup.find('div', class_='author-description').get_text()
    return {
        'fullname': soup.find('h3', class_='author-title').get_text(),
        'born_date': born_date,
        'born_location': born_location,
        'description': description.strip()  # Видаляємо зайві пробіли з опису
    }

# Функція для парсингу сторінки і отримання цитат
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author_url = base_url + quote.find('a')['href']
        author_info = get_author_info(author_url)
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        
        # Додаємо інформацію про цитату до списку
        quotes.append({
            'quote': text,
            'author': author_info['fullname'],
            'tags': tags
        })

        # Перевіряємо, чи доданий вже автор до списку, якщо ні, додаємо
        if not any(auth['fullname'] == author_info['fullname'] for auth in authors):
            authors.append(author_info)

    # Перевіряємо, чи є наступна сторінка для парсингу
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.find('a')['href']
        scrape_quotes(next_page_url)

# Викликаємо функцію для парсингу цитат
scrape_quotes(base_url)

# Зберігаємо інформацію про цитати у файл quotes.json
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)

# Зберігаємо інформацію про авторів у файл authors.json
with open('authors.json', 'w') as f:
    json.dump(authors, f, indent=4)

print("Інформація про цитати та авторів успішно збережена!")
