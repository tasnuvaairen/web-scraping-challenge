import sys
import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from scrape_mars_impl import scrape
from scrape_mars_impl import show_scarpped_html
from scrape_mars_impl import show_html
from scrape_mars_impl import add_to_db
from scrape_mars_impl import get_from_db

app = Flask (__name__)

@app.route("/root")
def welcome ():
    return (
        f"Root.<br/>\n"
)

@app.route("/scrape")
def scrape_url ():
	print("Scraping ... ")
	#return scrape()
	db_conn_string = 'mongodb://localhost:27017'
	html_string = "<html><body><div>" + str(add_to_db(db_conn_string, scrape())) + "<div></body></html>"
	return html_string 

@app.route("/")
def show_scarpped_html_url ():
	print("Fetching data ... ")
	#html_string = "<html>" + show_scarpped_html(scrape()) + "</html>" # live scraping
	db_conn_string = 'mongodb://localhost:27017'
	#html_string = "<html>" + show_scarpped_html(get_from_db(db_conn_string)) + "</html>"
	html_template_file = "index.html"
	html_string = show_html(html_template_file, get_from_db(db_conn_string))
	return html_string

if __name__ == '__main__':
	#scrape()
	app.run()    