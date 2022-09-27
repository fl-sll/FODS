from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd

list = []

session = HTMLSession()


for sn in range(1,10):
        response = session.get('https://www.imdb.com/title/tt0460649/episodes?season=' + str(sn))

        soup = BeautifulSoup(response.text, 'html.parser')

        episode_containers = soup.find_all('div', class_ = 'info')
        image_container = soup.find('div', class_ = 'image')

        for episodes in episode_containers:
                season = sn
                episode_number = episodes.meta['content']
                title = episodes.a['title']

                for image in image_container:
                        images = image_container.img['src']

                links = episodes.a['href']

                airdate = episodes.find('div', class_ = 'airdate').get_text()
                #! cleaning airdate
                airdate = airdate.replace('(',"").replace(')',"")

                rating = episodes.find('span', class_ = 'ipl-rating-star__rating').text

                total_votes = episodes.find('span', class_= 'ipl-rating-star__total-votes').text
                #! cleaning votes
                total_votes = total_votes.replace('(',"").replace(')',"")

                desc = episodes.find('div', class_ = 'item_description').text.strip()

                episodes_data = [season, episode_number, images, title, links, airdate, rating, total_votes, desc]

                list.append(episodes_data)

# response = session.get('https://www.imdb.com/title/tt0460649/episodes?season=2')
# soup = BeautifulSoup(response.text, 'html.parser')
# episode = soup.select('div.info div.airdate')
# print(episode[0])
    
df = pd.DataFrame(list, columns = ['season', 'episode_number', 'image', 'title', 'link', 'airdate', 'rating', 'total_votes', 'description'])
df.to_csv('HIMYM.csv', index=False)
