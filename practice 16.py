import os
import requests
import json
from bs4 import BeautifulSoup
import string
from urllib.parse import urljoin

def stage_1():
    """Етап 1: Отримання цитати з API"""
    url = input("Input the URL: ").strip()
    try:
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response.status_code != 200:
            print("Invalid quote resource!")
            return
        
        data = response.json()
        if 'content' not in data:
            print("Invalid quote resource!")
            return
            
        print(data['content'])
        
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print("Invalid quote resource!")

def stage_2():
    """Етап 2: Парсинг інформації про фільм з IMDb"""
    url = input("Input the URL: ").strip()
    if 'imdb.com/title/' not in url:
        print("Invalid movie page!")
        return
    
    try:
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response.status_code != 200:
            print("Invalid movie page!")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Отримання назви
        title_tag = soup.find('title')
        if not title_tag:
            print("Invalid movie page!")
            return
        title = title_tag.text.replace(' - IMDb', '').strip()
        
        # Отримання опису
        meta_desc = soup.find('meta', {'name': 'description'})
        if not meta_desc:
            print("Invalid movie page!")
            return
        description = meta_desc['content'].strip()
        
        print(json.dumps({"title": title, "description": description}, ensure_ascii=False))
        
    except requests.exceptions.RequestException:
        print("Invalid movie page!")

def stage_3():
    """Етап 3: Збереження HTML-коду сторінки"""
    url = input("Input the URL: ").strip()
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"The URL returned {response.status_code}!")
            return
            
        with open('source.html', 'wb') as f:
            f.write(response.content)
        print("Content saved.")
        
    except requests.exceptions.RequestException:
        print(f"The URL returned {response.status_code}!")

def stage_4():
    """Етап 4: Парсинг статей з Nature та збереження у файли"""
    base_url = "https://www.nature.com"
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2022&page=3"
    
    try:
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response.status_code != 200:
            print(f"The URL returned {response.status_code}!")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        saved_articles = []
        
        for article in articles:
            # Перевірка типу статті
            type_span = article.find('span', {'data-test': 'article.type'})
            if not type_span or type_span.text.strip() != 'News':
                continue
                
            # Отримання посилання на статтю
            link = article.find('a', {'data-track-action': 'view article'})
            if not link:
                continue
            article_url = urljoin(base_url, link.get('href'))
            
            # Отримання вмісту статті
            article_response = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if article_response.status_code != 200:
                continue
                
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            body = article_soup.find('div', {'class': 'article__body'})
            if not body:
                continue
                
            # Обробка назви файлу
            title = article_soup.find('h1').text.strip()
            translator = str.maketrans(' ', '_', string.punctuation)
            filename = title.translate(translator) + '.txt'
            
            # Збереження вмісту статті
            with open(filename, 'wb') as f:
                content = body.text.strip().encode('utf-8')
                f.write(content)
                
            saved_articles.append(filename)
            
        print("Saved articles:", saved_articles)
        
    except requests.exceptions.RequestException:
        print("Error during articles processing")

def stage_5():
    """Етап 5: Парсинг кількох сторінок та типів статей"""
    base_url = "https://www.nature.com"
    
    try:
        pages = int(input("Enter number of pages: "))
        article_type = input("Enter article type: ").strip()
        
        for page in range(1, pages + 1):
            url = f"{base_url}/nature/articles?sort=PubDate&year=2022&page={page}"
            response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if response.status_code != 200:
                print(f"Error fetching page {page}")
                continue
                
            # Створення директорії для сторінки
            dir_name = f"Page_{page}"
            os.makedirs(dir_name, exist_ok=True)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            saved_articles = []
            
            for article in articles:
                # Перевірка типу статті
                type_span = article.find('span', {'data-test': 'article.type'})
                if not type_span or type_span.text.strip() != article_type:
                    continue
                    
                # Отримання посилання на статтю
                link = article.find('a', {'data-track-action': 'view article'})
                if not link:
                    continue
                article_url = urljoin(base_url, link.get('href'))
                
                # Отримання вмісту статті
                article_response = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
                if article_response.status_code != 200:
                    continue
                    
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Пошук тіла статті (може відрізнятися для різних типів)
                body = article_soup.find('div', {'class': 'article__body'}) or \
                       article_soup.find('div', {'class': 'article-item__body'})
                if not body:
                    continue
                    
                # Обробка назви файлу
                title = article_soup.find('h1').text.strip()
                translator = str.maketrans(' ', '_', string.punctuation)
                filename = title.translate(translator) + '.txt'
                filepath = os.path.join(dir_name, filename)
                
                # Збереження вмісту статті
                with open(filepath, 'wb') as f:
                    content = body.text.strip().encode('utf-8')
                    f.write(content)
                    
                saved_articles.append(filename)
            
            print(f"Page {page}: Saved {len(saved_articles)} articles")
            
        print("Saved all articles.")
        
    except ValueError:
        print("Invalid number of pages")
    except requests.exceptions.RequestException:
        print("Error during processing")

def main():
    print("Практична робота №16 'Парсер веб-сторінок'")
    print("Оберіть етап для виконання:")
    print("1 - Отримання цитати з API")
    print("2 - Парсинг інформації про фільм з IMDb")
    print("3 - Збереження HTML-коду сторінки")
    print("4 - Парсинг статей з Nature (одна сторінка)")
    print("5 - Парсинг статей з Nature (кілька сторінок)")
    
    choice = input("Ваш вибір (1-5): ")
    {
        '1': stage_1,
        '2': stage_2,
        '3': stage_3,
        '4': stage_4,
        '5': stage_5
    }.get(choice, lambda: print("Невірний вибір"))()

if __name__ == "__main__":
    main()