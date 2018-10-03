from bs4 import BeautifulSoup
import newspaper
from urllib.request import urlopen
import requests
import re
from lxml import html
from newspaper import Article
import pandas as pd
from datetime import date

def main():
	url = 'https://www.google.com/search' 
	var = input("Please enter a name to search for in the news: ")
	payload = {'q': var, 'tbm':'nws', 'num':'100'}

	code = requests.get(url, params=payload)
	soup = BeautifulSoup(code.text, 'html.parser')
	headlines = soup.find_all('div', {'class':'g'})
	primary_articles = []

	for headline in headlines:
		section_links = []

		for link in headline.find_all('a', href=True):
			section_links.append(link['href'])
			
		primary_articles.append(section_links[0])

	primary_articles = [str(r) for r in primary_articles]

	url_LIST, first_author_LIST, date_LIST, article_bodies_LIST, article_keywords_LIST, title_LIST = [],[],[],[],[],[]

	for item in primary_articles:
		url = item[7:]
		article = Article(url)
		article.download()
		try:
			article.parse()
			article.nlp()

			#getting author, text, keywords, pubdate, title, url
			try:
				first_author_LIST.append(article.authors[0])
			except IndexError:
				first_author_LIST.append("NOTRETRIEVED")
			article_bodies_LIST.append(article.text)
			','.join(article.keywords)
			article_keywords_LIST.append(article.keywords)
			fulldate = article.publish_date
			try:
				date_converted = fulldate.strftime('%m/%d/%Y')
			except AttributeError:
				date_converted = "NOTRETRIEVED"
			date_LIST.append(date_converted)
			title_LIST.append(article.title)
			url_LIST.append(url)

		except newspaper.article.ArticleException:	
			continue


	df = pd.DataFrame(list(zip(date_LIST, title_LIST, first_author_LIST, url_LIST, article_bodies_LIST, article_keywords_LIST)), columns=["date","title","first_author","url","text","keywords"])
	today = str(date.today()).strip('-')


	df.to_csv('topgooglenews_'+var+'__'+today+'.csv', index=False)




if __name__ == "__main__": main()