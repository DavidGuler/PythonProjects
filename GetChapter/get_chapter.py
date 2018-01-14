import urllib.request
import os.path
from sys import argv as args
from os import system

ROOT_PATH = "/data/data/com.termux/files/home"
# ROOT_PATH = r"/mnt/c/Users/david/Desktop"
OUTPUT_PATH = os.path.join(ROOT_PATH,"test.html")
BASE_URL = "http://haktuvim.co.il/static/bibles/{0}/{1}/{1}.{2}.html"
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
	<title>{0}. {1}</title>
	<style>
		.v-reference {{display: none;}}
	</style>
</head>
<body>
	{2}
</body>
</html>
"""

bible_type = args[1]
book = args[2]
chapter = args[3]
 
res = str(urllib.request.urlopen(BASE_URL.format(bible_type,book,chapter)).read()).replace('\\n', '\n')

with open (OUTPUT_PATH, 'w') as html_file:
    html_file.write(HTML_TEMPLATE.format(book, chapter, res))

os.system("termux-open {0}".format(OUTPUT_PATH))
