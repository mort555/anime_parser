import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class GatherAnimeInfo:

    def __init__(self):
        self.session = requests.Session()

    def get_all_cards(self):
        page = 1
        all_cards = []

        with tqdm(desc="Парсинг страниц", unit="page") as pbar:
            while True:
                response = self.session.get(f"https://anime1.best/page/{page}/")
                soup = BeautifulSoup(response.text, "html.parser")

                content = soup.find("div", id="dle-content")
                if not content:
                    break

                cards = content.find_all("div", class_="shortstory")
                if not cards:
                    break

                all_cards.extend(cards)

                page += 1
                pbar.update(1)

        return all_cards

    def get_info_from_all_cards(self, cards):
        info_from_all_cards = []

        for card in cards:
            a_tag = card.find("a")
            img_tag = card.find("img")
            episode = card.find("div", itemprop="episode")
            amount_views = card.find("span", class_="short-images-views")

            title = a_tag.get("title") if a_tag else None
            link = a_tag.get("href") if a_tag else None
            image = img_tag.get("data-src") if img_tag else None
            episode_text = episode.text.strip() if episode else None
            views = amount_views.text.strip() if amount_views else None

            info = {
                "title": title,
                "link": link,
                "image": image,
                "episode": episode_text,
                "views": views,
            }

            info_from_all_cards.append(info)

        return info_from_all_cards

    def get_info_from_card_pages(self, links):

        result = []

        for link in tqdm(links, desc="Парсинг страниц аниме"):
            response = self.session.get(link)
            soup = BeautifulSoup(response.text, "html.parser")

           
            hat_info = soup.find("div", class_="fullstory-film")
            year = hat_info.find("time", attrs={"itemprop":"datePublished"} ).text
            genres = hat_info.find("div", attrs={"itemprop":"genre"} ).text
            cats = ", ".join([i.text for i in soup.find("div", class_ ="cat-list").find_all("a")])
            
            result.append({
                "link": link,
                "year": year,
                "genres": genres,
                "tags": cats
            })

        return result