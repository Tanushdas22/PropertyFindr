import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler


def scrape_apartments(max_price):
    blueground_url = f"https://www.theblueground.com/furnished-apartments-dubai-uae"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Proxy configuration with login and password
    proxy_host = 'gw.dataimpulse.com'
    proxy_port = 823
    proxy_login = ''
    proxy_password = ''
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

    proxies = {
        'http': proxy,
        'https': proxy
    }

    # Send a GET request using the proxy
    response = requests.get(blueground_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    apt_list = soup.find_all('a', class_="property")
    filtered_apartments = []

    for apt in apt_list:
        url = apt.get('href')
        title = apt.find('span', class_='property__name').text.strip() if apt.find('span',
                                                                                   class_='property__name') else 'No title available'
        price = apt.find('span', class_='price__amount').text.strip() if apt.find('span',
                                                                                  class_='price__amount') else 'No price available'

        # Remove currency symbol and commas, then convert to float for comparison
        price_value = float(price.replace('AED', '').replace(',', '').strip())

        if price_value <= max_price:
            full_url = f"https://www.theblueground.com{url}"
            filtered_apartments.append((title, price, full_url))

    return filtered_apartments


def send_email(apartments, recipient_email):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    # Email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Filtered Apartment Listings from Blueground"

    body = "Here are the apartments with a price lower than your specified amount:\n\n"
    for title, price, url in apartments:
        body += f"Title: {title}\nPrice: {price}\nLink: {url}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    # Sending the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()


def job():
    max_price = float(input("Enter the maximum price: "))
    recipient_email = input("Enter your email address: ")
    apartments = scrape_apartments(max_price)
    if apartments:
        send_email(apartments, recipient_email)
        print(f"Email sent to {recipient_email} with {len(apartments)} listings.")
    else:
        print("No apartments found within the specified price range.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', days=1)
    try:
        print("Starting the scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
