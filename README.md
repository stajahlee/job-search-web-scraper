# Job Search Web Scraper
This program scrapes the Ohio University jobs search page with a search query keyword that is input by the user as a command line argument. 

It then sends a Mac OS desktop notification with the results, which when clicked opens a browser window and automatically directs to that search result page at www.ohiouniversityjobs.com/postings/search.

Run by typing in the command line `python3 run.py software+developer` for example if you want to search for Software Developer jobs.

See screenshots:

No matching results:
https://user-images.githubusercontent.com/12398367/28953891-4dbfdc56-78a9-11e7-9682-a138d106e461.png

Result == 5 matches | Click on the Desktop Notification for further review:
https://user-images.githubusercontent.com/12398367/28953899-59ab05e0-78a9-11e7-93fe-2b07651ed6f2.png

After clicked, notification opens the appropriate link in the browser:
https://user-images.githubusercontent.com/12398367/28953900-5c3789c8-78a9-11e7-8608-5be80e1ebfc5.png
