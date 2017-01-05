Requirements:
MongoDB: sudo apt-get install mongodb
Scrapy:  pip install scrapy
Scrapy-mongodb: pip install scrapy-mongodb

shell commands:
cd /path/to/AppCrawler-masterR/app
scrapy crawl google -s JOBDIR=app/jobs

-s JOBDIR=app/jobs: save crawled pages to directory app/jobs, if interepted, continue from where stop
