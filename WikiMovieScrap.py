import requests
from bs4 import BeautifulSoup
import csv

def scrape_movies():
    base_url = 'https://en.wikipedia.org'

    # Create a CSV file to store the scraped data
    with open('movies_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Movie Name', 'Main Actor(s)', 'Year of Release']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Construct the URL for the Wikipedia page
        url = f"{base_url}/wiki/List_of_films:_A"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the movie table on the page
        divs = soup.find_all('div', class_='div-col')

        for div in divs:
            soup = BeautifulSoup(str(div.ul), 'html.parser')
            anchorTags = soup.find_all('a')
            for anchorTag in anchorTags:
                url = f"{base_url}"+anchorTag['href']
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                print(anchorTag.text + '  ' + url)
                releaseDate = soup.find_all('span', class_='bday dtstart published updated')
                if len(releaseDate) == 0:
                    releaseDate = soup.find_all('td', class_='infobox-data')

                releaseDateStr = ''
                if len(releaseDate) != 0:
                    releaseDateStr = releaseDate[0].text

                castdiv = soup.find("div", class_='mw-parser-output')
                soup = BeautifulSoup(str(castdiv), 'html.parser')
                castdiv = soup.find_all("li")

                if len(castdiv) != 0:
                    print(castdiv)

                writer.writerow({
                        'Movie Name': anchorTag.text,
                        #'Main Actor(s)': anchorTag.text,
                        'Year of Release': releaseDateStr
                })

    print("Scraping completed successfully.")

# Scrape the movies and store the data in a CSV file
if __name__ == "__main__":
    scrape_movies()