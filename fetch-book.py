from sys import stdout
from time import sleep

import requests

page_id = 1

url_pattern = "http://resources.huygens.knaw.nl/retroapp/service_generalemissiven/gm_02/images/gm_2_112_{}.jpg"
dir = "C:\\Users\\Thomas\\Documents\\Dutch East indies\\books\\gm_02"
file_name = "{}\\{}.jpg"

while page_id <= 825:
    url = url_pattern.format(str(page_id).zfill(4))
    with open(file_name.format(dir, str(page_id)), "wb") as file:
        response = requests.get(url)
        file.write(response.content)

    print("Fetched " + url)
    stdout.flush()
    page_id = page_id + 1
    sleep(1)
