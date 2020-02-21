# Dependencies
from bs4 import BeautifulSoup
import requests

from splinter import Browser

import re

import pandas as pd

import pymongo


def get_from_db(conn_string) :
	conn = conn_string
	client = pymongo.MongoClient(conn)

	db = client.marsDB

	mars_collection = db.mars_collection

	cursor = mars_collection.find().limit(1)#.sort({$natural:-1})

	#for record in cursor :
		#print(record)
	#	for k in record :
	#		print(k)

	data_dict = cursor[0]
	del data_dict["_id"]
	#print(data_dict)

	print("Done reading from DB.")	

	return data_dict

def add_to_db(conn_string, data_dict) :
	conn = conn_string
	client = pymongo.MongoClient(conn)

	db = client.marsDB

	#test_collection = db.test_collection
	#test_dict_1 = {"title" : "Animal", "name" : "Monkey"}
	#test_dict_2 = {"title" : "Bird", "name" : "Chicken"}
	#rec_id_1 = test_collection.insert_one(test_dict_1)
	#rec_id_2 = test_collection.insert_one(test_dict_2)
	#print(data_dict)

	mars_collection = db.mars_collection 

	#mars_collection.remove({}) # delete the old data
	mars_collection.delete_many({}) # delete the old data

	rec_id_1 = mars_collection.insert_one(data_dict)

	print("Data added to the DB.")

	return str(data_dict) + "</br></br>" + "Data added to the DB."  

def scrape() :

	scape_dict = dict()

	executable_path = {'executable_path': 'C:\local\chromedriver_win32\chromedriver.exe'}
	#browser = Browser('chrome', **executable_path, headless=False)
	#browser = Browser('chrome', **executable_path)

	# URL of page to be scraped
	url = 'https://mars.nasa.gov/news/'
	# Retrieve page with the requests module
	response = requests.get(url)
	# Create BeautifulSoup object; parse with 'html.parser'
	soup = BeautifulSoup(response.text, 'html.parser')
	# Examine the results, then determine element that contains sought info
	#print(soup.prettify())

	title_results = soup.find_all("div", class_="content_title", limit=1)
	#print(len(title_results))
	news_title = title_results[0].text.strip()
	print(news_title)

	paragraph_results = soup.find_all("div", class_="rollover_description_inner", limit=1)
	#print(len(paragraph_results))
	news_p = paragraph_results[0].text.strip()
	print(news_p)

	scape_dict["News"] = [{"news_title" : news_title, "news_paragraph" : news_p}]

	# URL of page to be scraped
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

	#browser = Browser('chrome')

	featured_image_url = ""

	with Browser('chrome', **executable_path) as browser :
	    browser.visit(jpl_url)
	    button = browser.find_by_id('full_image')
	    #print(len(button))
	    button.click()

	    featured_image = browser.find_by_xpath('//img[@class="fancybox-image"]')
	    #print(len(featured_image))
	    featured_image_url = featured_image["src"]
	    print (featured_image_url)

	scape_dict["Image"] = [{"featured_image" : featured_image_url}]

	# URL of page to be scraped
	twitter_url = "https://twitter.com/marswxreport?lang=en"
	# Retrieve page with the requests module
	twitter_response = requests.get(twitter_url)
	# Create BeautifulSoup object; parse with 'html.parser'
	twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
	#print(twitter_soup)

	#twitter_results = twitter_soup.find_all("p", class_="TweetTextSize", limit=1)
	#print(len(twitter_results))

	#for r in twitter_results :
	#    print(r.text.strip())
	    
	twitter_results = twitter_soup.find_all("p", string = re.compile('^InSight .*'), limit=1)
	#print(len(twitter_results))
	mars_weather = twitter_results[0].text.strip()
	print(mars_weather)

	scape_dict["Weather"] = [{"mars_weather" : mars_weather}]

	# URL of page to be scraped
	facts_url = "https://space-facts.com/mars/"
	facts_df = pd.read_html(facts_url, attrs={'id': 'tablepress-p-mars'})[0]
	facts_df

	facts_table_html = facts_df.to_html(index=False, header=False)
	facts_table_html

	scape_dict["Facts"] = [{"facts_table_html" : facts_table_html}]

	ast_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	strip_word = "Enhanced"

	#browser = Browser('chrome')

	hemisphere_image_urls = []

	with Browser('chrome', **executable_path) as browser :

		browser.visit(ast_url)
		links_found = browser.links.find_by_partial_href('Viking')
		#print(len(links_found))

		links_set = set()

		for l in links_found :
			#print(l["href"])
			links_set.add(l["href"])
			#print(len(links_set))

		for l in links_set :
			browser.visit(l)
			title_element = browser.find_by_xpath('//h2[@class="title"]')
			title_string = title_element.text.strip(strip_word).strip()
			print(title_string)
			img_sample_element = browser.find_by_text("Sample")
			print(img_sample_element["href"])
			tmp_dict = {"title" : title_string, "img_url" : img_sample_element["href"]}
			hemisphere_image_urls.append(tmp_dict)

	hemisphere_image_urls

	scape_dict["Hemispheres"] = hemisphere_image_urls

	return scape_dict

def show_scarpped_html(data_dict) :

	imgae_file_type = ".jpg"

	html_body_string = ""

	html_body_string = html_body_string + '<head> \
	<title>Bootstrap Example</title> \
	<meta charset="utf-8"> \
	<meta name="viewport" content="width=device-width, initial-scale=1"> \
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"> \
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script> \
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script> \
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script> \
	</head>'

	html_body_string = html_body_string + '<body>'
	html_body_string = html_body_string + '<div class="container-fluid"><p><h1>Mission to Mars</h1></p>'
	html_body_string = html_body_string + '<button onclick="location.reload();">Scrape New Data</button></div>'

	for k, v in data_dict.items() :
		print (str(k) + " " + str(len(v)) )
		html_body_string = html_body_string + '<div class="container-fluid"><p><h2>' + str(k) + '</h2></p>'
		html_body_string = html_body_string + '<div>'

		for i in v :
			#print(i)
			for p, q in i.items() :
				print (str(p) + " " + str(q) )

				html_element_string =  "<div>" + str(q) + "</div>"

				if str(q).endswith(imgae_file_type) :
					html_element_string = "<div><img src=" + str(q) + " height='400' width='400'></div>"
				elif str(p) == "news_title" :
					html_element_string =  "<div><h5>" + str(q) + "<h5></div>"

				html_body_string = html_body_string + html_element_string

		html_body_string = html_body_string + "</div></div></br>"		
	html_body_string = html_body_string + "</body>"
	return html_body_string

def get_html(data_dict) :

	imgae_file_type = ".jpg"

	html_body_string = ""

	#html_body_string = html_body_string + '<head> \
	#<title>Bootstrap Example</title> \
	#<meta charset="utf-8"> \
	#<meta name="viewport" content="width=device-width, initial-scale=1"> \
	#<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"> \
	#<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script> \
	#<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script> \
	#<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script> \
	#</head>'

	#html_body_string = html_body_string + '<body>'
	#html_body_string = html_body_string + '<div><p><h1>Mission to Mars</h1></p>'
	#html_body_string = html_body_string + '<button onclick="location.reload();">Scrape New Data</button></div>'

	for k, v in data_dict.items() :
		print (str(k) + " " + str(len(v)) )
		html_body_string = html_body_string + '<div"><p><h2>' + str(k) + '</h2></p>'
		html_body_string = html_body_string + '<div>'

		for i in v :
			#print(i)
			for p, q in i.items() :
				print (str(p) + " " + str(q) )

				html_element_string =  "<div>" + str(q) + "</div>"

				if str(q).endswith(imgae_file_type) :
					html_element_string = "<div><img src=" + str(q) + " height='400' width='400'></div>"
				elif str(p) == "news_title" :
					html_element_string =  "<div><h5>" + str(q) + "<h5></div>"

				html_body_string = html_body_string + html_element_string

		html_body_string = html_body_string + "</div></div></br>"		
	#html_body_string = html_body_string + "</body>"
	return html_body_string

def show_html(html_template_file, data_dict) :
	#print(data_dict)

	#data_html_string = get_html(data_dict)
	#data_soup = BeautifulSoup(data_html_string, 'html.parser')

	soup = BeautifulSoup('<html><body>Empty.</body></html>', 'html.parser')

	with open(html_template_file, 'r') as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'html.parser')
		#print(soup.prettify())

		#html_body_element = soup.find_all('body', limit=1)[0]
		#print(str(html_body_element))

		html_element = soup.find_all("div", class_="container-fluid", limit=1)[0]
		
		data_soup = BeautifulSoup(get_html(data_dict), 'html.parser')

		#html_body_element.insert(1, data_soup)

		html_element.append(data_soup)	

	return str(soup)			

# Test code
def main():
	#print(scrape())
	#show_scarpped_html(scrape())
	#add_to_db('mongodb://localhost:27017', scrape())
	#print(get_from_db('mongodb://localhost:27017'))
	print(show_html('index.html', get_from_db('mongodb://localhost:27017')))

if __name__ == "__main__":
    main()