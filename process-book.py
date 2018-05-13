import json
import os

import pymongo

client = pymongo.MongoClient(host="192.168.99.100", port=27017)
books = client['documents'].books
missives = client['documents'].missives
file_name = 'sources/temp.txt'
handle = open(file_name, 'w+')

pages = books.find({"book_id": "gm_01"}).sort([("page_id", pymongo.ASCENDING)])

missive = {}

for page in pages:
    data = json.loads(page['data'])
    parsedText = data['ParsedResults'][0]['ParsedText']
    print(parsedText)

    new = input('New missive (y, n, s): ')

    if new == 's':
        print("Skipping to next page")

    if new == '':
        print("Stopping")
        exit()

    if new == 'y':
        if missive != {}:
            input("Prepare text before inserting. Press enter to continue")
            missive['text'] = handle.read()
            print("Inserting finished missive", missive)
            # missives.insert_one(missive)
            handle.close()
            os.remove(file_name)

        handle = open(file_name, 'w+')

        missive['governors'] = input('Governors: ')
        missive['date'] = input('Date: ')
        missive['location'] = input('Location: ')

        handle.write('\n' + parsedText.replace("\r\n\r\n", "\r\n"))

    if new == 'n':
        handle.write('\n' + parsedText.replace("\r\n\r\n", "\r\n"))
