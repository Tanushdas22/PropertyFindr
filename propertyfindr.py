import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler


def scrape_apartments(max_price):
    """
    Scrapes apartment listings from the Blueground website that are priced below the specified maximum price.
    
    Args:
    - max_price (float): The maximum price to filter apartments.

    Returns:
    - list of tuples: Each tuple contains the title, price, and URL of an apartment.
    """
    # URL of the Blueground website
    blueground_url = f"https://www.theblueground.com/furnished-apartments-dubai-uae"
    
    # HTTP headers to simulate a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Proxy configuration
    proxy_host = 'gw.dataimpulse.com'
    proxy_port = 823
    proxy_login = ''  # Username for proxy authentication
    proxy_password = ''  # Password for proxy authentication
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

    proxies = {
        'http': proxy,
        'https': proxy
    }

    # Send a GET request to the website using the configured proxy
    response = requests.get(blueground_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all apartment listings on the page
    apt_list = soup.find_all('a', class_="property")
    filtered_apartments = []

    for apt in apt_list:
        # Extract URL, title, and price of each apartment
        url = apt.get('href')
        title = apt.find('span', class_='property__name').text.strip() if apt.find('span', class_='property__name') else 'No title available'
        price = apt.find('span', class_='price__amount').text.strip() if apt.find('span', class_='price__amount') else 'No price available'

        # Remove currency symbol and commas, then convert price to float for comparison
        price_value = float(price.replace('AED', '').replace(',', '').strip())

        # Check if the apartment price is within the specified maximum price
        if price_value <= max_price:
            full_url = f"https://www.theblueground.com{url}"
            filtered_apartments.append((title, price, full_url))

    return filtered_apartments


def send_email(apartments, recipient_email):
    """
    Sends an email with the filtered apartment listings to the specified recipient.

    Args:
    - apartments (list of tuples): The list of apartments to include in the email.
    - recipient_email (str): The email address to send the email to.
    """
    sender_email = "your_email@example.com"  # Replace with your email address
    sender_password = "your_password"  # Replace with your email password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Filtered Apartment Listings from Blueground"

    # Create the email body
    body = "Here are the apartments with a price lower than your specified amount:\n\n"
    for title, price, url in apartments:
        body += f"Title: {title}\nPrice: {price}\nLink: {url}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    # Send the email via Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()


def job():
    """
    Executes the job of scraping apartments and sending an email with the results.
    """
    # Get user input for maximum price and recipient email address
    max_price = float(input("Enter the maximum price: "))
    recipient_email = input("Enter your email address: ")
    
    # Scrape apartments and send an email if any apartments are found
    apartments = scrape_apartments(max_price)
    if apartments:
        send_email(apartments, recipient_email)
        print(f"Email sent to {recipient_email} with {len(apartments)} listings.")
    else:
        print("No apartments found within the specified price range.")


if __name__ == "__main__":
    # Set up a scheduler to run the job daily
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', days=1)
    try:
        print("Starting the scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
