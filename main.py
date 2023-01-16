# SuperPriceSpyder is a simple Python program designed to scrape the Amazon website data for product pricing
# information. It uses the requests library & BeautifulSoup library to make an HTTP request to the given product URL
# & parse the information from the page. It then compares the current price to a threshold value (in this case,
# $28). If the price is below the threshold, it uses the smtplib library to login to an email account & send a price
# alert message to that email address. Finally, it prints out the title, price and URL of the product to the console.

# Super Price Spyder
import smtplib
import requests
from bs4 import BeautifulSoup
import os

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

url = 'https://www.amazon.co.uk/Multivitamin-Vitamins-absorbable-research-evidence/dp/B01H08EUT6/?_encoding=UTF8' \
      '&pd_rd_w=27iON&content-id=amzn1.sym.174592a4-b448-4d40-b99a-45f7f86c619e&pf_rd_p=174592a4-b448-4d40-b99a' \
      '-45f7f86c619e&pf_rd_r=0RKBGBQMKJX75JQ90R46&pd_rd_wg=T6Eu7&pd_rd_r=8eef1976-28f1-47ff-adc1-e0d99479829c&ref_' \
      '=pd_gw_ci_mcx_mi '
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/16.2 Safari/605.1.15",
    "Accept-Language": "en-GB,en;q=0.9",
}

page = requests.get(url, headers=headers)

# print(page.text)

soup = BeautifulSoup(page.text, 'lxml')
# print(soup.prettify())
price = soup.find(class_="a-offscreen").getText()
price_float = float(price.replace("£", ""))
title = soup.find(id="productTitle").getText().replace("        ", "")

# print(price)

if price_float < 28:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert!\n\n{title}\n\n now ${price_float}\n\n{url}"
        )

print(f"{title}\n{price}\n{url}")
