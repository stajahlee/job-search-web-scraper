# Job Search Web Scraper
This program scrapes the Ohio University jobs search page with a search query keyword that is input by the user as a command line argument. 

On Windows, the program will give you results in command line only.

On Mac OS X, the program gives results in command line and also sends a Mac OS desktop notification with the results, which when clicked opens a browser window and automatically directs to that search result page at www.ohiouniversityjobs.com/postings/search. This requires a package called _terminal-notifier_ which I installed before running the program using `brew install terminal-notifier`.

Run by typing in the command line `python3 run.py software+developer` for example if you want to search for Software Developer jobs.

See screenshots in this repo's Wiki: https://github.com/stajahlee/job-search-web-scraper/wiki
