import os
import yagmail
import csv
import concurrent.futures as cf
import time
import re

from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

# Regular expression for validating an email
REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def check(email):
    """"Check if email valid"""
    # pass the regular expression and email into the fullmatch() method
    if (re.fullmatch(REGEX, email)):
        return True  # valid

    else:
        return False  # invalid


def send_email(person, email):
    """Send email with attachment and return email and whether valid"""
    valid_email = check(email)
    if valid_email:
        try:
            body = f"Hello {person}. This is a test email from Right of Zero."
            filename = ('/home/mfsd1809/dev-environment/FullStackWebDeveloper/'
                        'GitRepos/bulk-email-with-attachment/test.txt')

            yag = yagmail.SMTP(
                user=os.environ.get('usr'),
                password=os.environ.get('pwd')
            )
            yag.send(
                to=email,
                subject="Right of Zero test with attachment",
                contents=body,
                attachments=filename,
            )
            result = True
        except Exception as e:
            print(e)
            result = False
    else:
        result = False
    return result, email


# Start timer
start = time.perf_counter()

# Get list of emails from CSV file
people = []
emails = []

# Opening the CSV file
with open(
    '/home/mfsd1809/dev-environment/FullStackWebDeveloper/GitRepos/'
        'bulk-email-with-attachment/people.csv', mode='r')as csvfile:

    # Reading the CSV file
    data = csv.reader(csvfile)
    next(data)  # Skip header row

    # Obtaining the emails from the file
    for record in data:
        people.append(record[0])
        emails.append(record[1])


# Send emails
success_count = 0
success = []
failure_count = 0
failure = []
with cf.ThreadPoolExecutor() as executor:
    for result, email in executor.map(send_email, people, emails):
        if result:
            success_count += 1
        else:
            failure_count += 1
            failure.append(email)


# Stop timer
end = time.perf_counter()

print(
    f'\nScript completed {len(emails)} emails in {round(end-start, 2)}'
    ' second(s).'
    )

print(
    f'\nA total of {success_count} successful email(s).'
    ' second(s).'
)

print(f'\nA total of {failure_count} email(s) failed:')

for bad_email in failure:
    print(f'\t{bad_email}')
