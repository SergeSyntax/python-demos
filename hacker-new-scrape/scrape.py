import requests
from bs4 import BeautifulSoup
from pprint import pprint

MIN = 60

def extract_hacker_news_info(page_num: int):
    """Extracts the titles and subtexts from the hacker news website"""
    all_titles = []
    all_subtexts = []
    for page in range(1, page_num + 1):
        res = requests.get(f"https://news.ycombinator.com/news?p={page}", timeout=MIN)
        soup = BeautifulSoup(res.text, "html.parser")
        titles = soup.select(".titleline > a")
        subtitles = soup.select(".subtext")
        all_titles += titles
        all_subtexts += subtitles
    return all_titles, all_subtexts

def sort_news_by_votes(news_list: list({"title": str, "link": str, "votes": int})):
    """Sorts the news by votes score in reverse order"""
    return sorted(news_list, key=lambda news_key: news_key["votes"], reverse=True)


def get_news_relevant_news(titles, subtext):
    """gets news with more than 99 votes"""

    news_list = []

    for idx, title in enumerate(titles):

        title_text = title.getText()
        href = title.get("href", None)
        vote = subtext[idx].select(".score")

        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                news_list.append({"title": title_text, "link": href, "votes": points})

    sorted_news = sort_news_by_votes(news_list)

    return sorted_news

def main():
    """Main process"""
    merged_titles, merged_subtexts = extract_hacker_news_info(2)
    news = get_news_relevant_news(merged_titles, merged_subtexts)
    pprint(news)


if __name__ == "__main__":
    main()
