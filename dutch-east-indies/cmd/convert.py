import glob
import os
import re
import shutil
import sys
from argparse import ArgumentParser

from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient

from ocr.parse import parse

argumentsParser = ArgumentParser()
argumentsParser.add_argument("--data_dir", help="The data dir to read from", type=str,
                             default=os.environ.get('DATA_DIR', "/data/books"))
argumentsParser.add_argument("--processed_dir", help="The dir to store processed files", type=str,
                             default=os.environ.get('PROCESSED_DIR', "/data/processed"))
argumentsParser.add_argument("--number", type=int, dest="number", help="The number of files to parse",
                             default=os.environ.get('NUMBER', 500))
argumentsParser.add_argument("--mongo-host", type=str, dest="mongo_host", help="The mongo host",
                             default=os.environ.get('MONGO_HOST', "mongodb"))
argumentsParser.add_argument("--mongo-port", type=int, dest="mongo_port", help="The mongo port",
                             default=os.environ.get('MONGO_PORT', 27017))
argumentsParser.add_argument("--ocr-key", type=str, dest="ocr_key", help="The OCR api key",
                             default=os.environ.get('OCR_KEY'))

arguments = argumentsParser.parse_args()

sched = BlockingScheduler()


@sched.scheduled_job("cron", year="*", month="*", day="*", hour="14", minute="*",
                     args=[arguments.data_dir, arguments.processed_dir, arguments.mongo_host, arguments.mongo_port,
                           arguments.number, arguments.ocr_key])
def job(data_dir, processed_dir, mongo_host, mongo_port, number, ocr_key):
    location = data_dir + "/*/*.jpg"
    files = glob.glob(location)
    client = MongoClient(host=mongo_host, port=mongo_port)
    pages = client['dutch-east-indies'].pages

    counter = 0
    for file in files:
        if counter >= number:
            print("Done processing, " + str(counter) + " pages added")
            client.close()
            return

        result = re.search('^.*/(?P<book>\w+)/(?P<page>[0-9]+)\.(?P<extension>[a-z]+)$', file)
        book_id = result.group('book')
        page_id = result.group('page')
        extension = result.group('extension')

        try:
            data = parse(file,
                         api_key=ocr_key,
                         overlay=False,
                         language="dut",
                         filetype=extension.upper(),
                         scale=True
                         )
        except Exception as err:
            print('book_id: ' + book_id)
            print('page_id: ' + page_id)
            print(err)
            exit(1)

        page = {
            "book_id": book_id,
            "page_id": int(page_id),
            "data": data
        }

        inserted_id = pages.insert_one(page).inserted_id

        print("Book " + book_id + ", page " + page_id + " inserted, id: " + str(inserted_id))
        sys.stdout.flush()

        path = processed_dir + "/" + book_id
        if not os.path.exists(path):
            os.mkdir(path)

        newfile = path + "/" + page_id + "." + extension
        shutil.move(file, newfile)
        counter = counter + 1


sched.configure()
sched.start()
