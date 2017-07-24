# **********************************************************************************
#
#  PROGRAM THAT FINDS OHIO UNIVERSITY JOBS POSTINGS WITH MY DESIRED KEYWORDS 
#  AND NOTIFIES ME ON MY DESKTOP
#
#  https://www.ohiouniversityjobs.com/postings/search
#  ->then input the keywords that found new postings
#
#  Author: Stajah Lee Hoeflich | stajah@stajahlee.com
#  Sun Jul 23 16:09:17 2017
#
# **********************************************************************************
import urllib.request	
import ssl
import os
import smtplib # to send emails
import schedule # script runs on timer
import time


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....open_page
# PURPOSE:.....from a given url this function takes the full HTML and returns it as 
#              a string
# PARAMETERS:..link | string 
# RETURNS:.....webpage | string of entire HTML of page at given URL
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def open_page(link):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	req = urllib.request.Request(link)
	response = urllib.request.urlopen(req, context = ctx)
	charset = response.headers.get_content_charset()		
	webpage = response.read().decode(charset)	
	return webpage


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....make_postings_list
# PURPOSE:.....given a string that contains a webpage's entire HTML this function
#              finds the job postings' title(s) and puts them in a list
# PARAMETERS:..page_str | string that contains entire HTML of a page
# RETURNS:.....list of job postings titles
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def make_postings_list(page_str):
	index = 0
	posts_indices = []
	posts = []
	while index < len(page_str):
		index = page_str.find('data-posting-title=', index)
		if index == -1:
			break
		posts_indices.append(index)
		index += 19
	for i in posts_indices:
		posts.append(page_str[i+20:i+100])
	count = 0	
	while count < len(posts):
		posts[count] = posts[count][:posts[count].find('"')]
		count += 1
	return posts


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....find_jobs
# PURPOSE:.....given a specific keyword the OU job search link will find postings
#              with the keyword as a query parameter
# PARAMETERS:..keyword | string
# RETURNS:.....string describing how many jobs found and their titles, or if none
#              found, will return none-found-message 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #	
def find_jobs(keyword):
	link = 'https://www.ohiouniversityjobs.com/postings/search?utf8=%E2%9C%93&query='
	link = link + keyword
	link = link +'&query_v0_posted_at_date=&225=&commit=Search'	 
	page_str = open_page(link)
	posts = make_postings_list(page_str)
	jobs = ""
	if (len(posts)!=0):
		for i in posts:
			jobs += (" " + i + "\n")
		print ("\n\nKeyword: " + keyword + "\n------------------------------------\n" + str(len(posts)) + ' jobs found:\n' + jobs)
		return (str(len(posts)) + ' jobs found: ' + jobs)
	else:
		print ("\n\nKeyword: " + keyword + '\n------------------------------------\nNo ' + keyword + ' jobs found today - sorry :(')
		return ('No ' + keyword + ' jobs found today - sorry :(')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....notify
# PURPOSE:.....os desktop notification function
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def notify():
	keywords = []
	keywords.append('software')
	keywords.append('developer')
	keywords.append('information+technology')
	count = 0
	while count < len(keywords):
		title = '-title {!r}'.format("My Job Search")
		subtitle = '-subtitle {!r}'.format("Keyword: " + keywords[count])
		message = '-message {!r}'.format(find_jobs(keywords[count]))
		sound = '-sound {!r}'.format("Purr.aiff")
		os.system('terminal-notifier {}'.format(' '.join([message, title, subtitle, sound])))
		count += 1


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....main
# PURPOSE:.....scrape OU job posting site for specific keywords and display
#			   a desktop notification with results each morning
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def main():	

	schedule.every(5).seconds.do(notify)
	# schedule.every().day.at("5:00").do(notify)
	while 1:
	    schedule.run_pending()
	    time.sleep(1)


if __name__ == "__main__":
	main()