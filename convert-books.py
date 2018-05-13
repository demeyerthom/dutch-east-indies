import glob
import os
import re
import sys
from optparse import OptionParser
from time import sleep

from pymongo import MongoClient

from ocr.parse import parse

parser = OptionParser()
parser.add_option("-n", "--number", type=int, dest="number", help="The number of files to parse", metavar="N")

(options, args) = parser.parse_args()

dir = sys.path[0]
location = dir + "/sources/books/Generale_Missiven/[!processed]*/*.jpg"
files = glob.glob(location)

client = MongoClient(host="localhost", port=27017)
pages = client['dutch-east-indies'].pages

print("Started processing books")

counter = 0
for file in files:
    if counter >= options.number:
        print("Done processing, " + str(counter) + " added")
        exit()

    result = re.search("^(?P<root>.*)/(?P<book>\w+)/(?P<page>[0-9]+)\.jpg$", file)
    root = result.group('root')
    book_id = result.group('book')
    page_id = result.group('page')

    try:
        data = parse(file, api_key="a9f48e6f4e88957", overlay=True, language="dut")
    except Exception as err:
        print('book_id: ' + book_id)
        print('page_id: ' + page_id)
        print(err)
        exit()

    page = {
        "book_id": book_id,
        "page_id": int(page_id),
        "data": data
    }

    inserted_id = pages.insert_one(page).inserted_id

    print("Book " + book_id + ", page " + page_id + " inserted, id: " + str(inserted_id))
    sys.stdout.flush()

    path = result.group('root') + "/processed/" + result.group('book')
    if not os.path.exists(path):
        os.mkdir(path)

    newfile = path + "/" + result.group('page') + ".jpg"
    os.rename(file, newfile)
    counter = counter + 1
    sleep(1)
