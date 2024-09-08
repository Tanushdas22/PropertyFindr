# PropertyFindr
This repository contains a Python script that scrapes apartment listings from Blueground and sends email notifications with filtered results based on user-defined criteria. The script uses web scraping to find apartments below a specified price and sends an email with the filtered listings.

## Features
Web Scraping: Extracts apartment listings from Blueground using BeautifulSoup.

Email Notification: Sends filtered apartment listings to a specified email address.

Scheduled Execution: Uses APScheduler to run the script daily.

## Note
Before running the script, ensure you have the following Python libraries installed:

requests

beautifulsoup4

apscheduler

smtplib

You can install these libraries using pip:
pip install requests beautifulsoup4 apscheduler

The script uses a proxy to send requests.

Do not forget to update the email configuration in the send_email function.

## Code Explanation
1. scrape_apartments(max_price):

Scrapes apartment listings from Blueground.
Filters listings based on the maximum price specified.
Returns a list of apartments that match the criteria.

2. send_email(apartments, recipient_email):

Composes and sends an email with the filtered apartment listings to the specified recipient.

3. job():

Prompts the user for input, executes the scraping function, and sends an email with the results.

4. Scheduler:

Uses APScheduler to run the job() function daily.
