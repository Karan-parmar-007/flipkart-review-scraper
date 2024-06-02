from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import pymongo

app = Flask(__name__)
application = app
@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            logging.info("post request")
            reviews = []
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            logging.info("search link formed")
            url_client = uReq(flipkart_url)
            flipkart_page = url_client.read()
            flipkart_html = bs(flipkart_page, 'html.parser')
            products_link = flipkart_html.findAll('div', {'class': '_75nlfW'})
            product_last_and_final_half_link = []
            for i in products_link:
                product = i.div.div.a['href']
                product_last_and_final_half_link.append(product)
            for one_product_link in product_last_and_final_half_link:
                logging.info("first for loop")
                final_link = 'https://www.flipkart.com'+ one_product_link
                first_product_link = requests.get(final_link)
                one_product_html = bs(first_product_link.text, 'html.parser')
                one_product_detail = one_product_html.findAll('div', {'class': 'pPAw9M'})
                all_review_link = ''
                for i in one_product_detail:
                    logging.info("third for loop")
                    all_review_link = one_product_detail[0].a['href']
                all_review_link_final = 'https://www.flipkart.com' + all_review_link
                url = all_review_link_final
                index = url.find('?')
                all_review_link_final_link = url[:index] + '?page=1'
                multiple_review_page = requests.get(all_review_link_final_link)
                multiple_review_page_html = bs(multiple_review_page.text, 'html.parser')
                number_of_pages = multiple_review_page_html.findAll('div', {'class': 'mpIySA'})
                number_of_pages_in_all = number_of_pages[0].span.text
                page_info = number_of_pages_in_all
                max_pages_str = page_info.split('of')[-1].strip()
                # max_pages = int(max_pages_str)
                # for i in range(1, max_pages + 1):
                for i in range(2):
                    logging.info("fourth for loop")
                    all_review_link_final_link = url[:index] + f'?page={i}'
                    multiple_review_page = requests.get(all_review_link_final_link)
                    multiple_review_page_html = bs(multiple_review_page.text, 'html.parser')
                    all_review_page_details = multiple_review_page_html.findAll('div', {'class': 'EPCmJX'})
                    for i in all_review_page_details:
                        logging.info("fifth for loop")

                        rating = i.div.div.text
                        # product_short_review = i.div.p.text
                        # product_short_review = i.div.div.div.text
                        if i.div.find("p"):
                            product_short_review = i.div.find("p").text
                        elif i.div.find("div"):
                            product_short_review = i.div.find("div").text
                        main_review = i.find('div', {'class': 'ZmyHeo'}).div.div.text
                        person_who_wrote_review = i.find('div', {'class': 'gHqwa8'}).div.p.text
                        mydict = {"Product": searchString, "Name": person_who_wrote_review, "Rating": rating, "CommentHead": product_short_review, "Comment": main_review}
                        reviews.append(mydict)
            client = pymongo.MongoClient("mongodb+srv://pw_course:pw_course@cluster0.amara6i.mongodb.net/?retryWrites=true&w=majority")
            db = client['review_scrap']
            review_col = db['review_scrap_data']
            review_col.insert_many(reviews)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            logging.info(e)
            return 'something is wrong'
        
        else:
            return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
