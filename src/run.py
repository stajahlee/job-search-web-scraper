# **********************************************************************************
#
#  PROGRAM THAT FINDS OHIO UNIVERSITY JOBS POSTINGS WITH KEYWORD PROVIDED AS A 
#  COMMAND LINE ARGUMENT AND NOTIFIES ON MAC DESKTOP
#
#  https://www.ohiouniversityjobs.com/postings/search
#  search keyword is input and direct link when notification clicked
#
#  Author: Stajah Lee Hoeflich | stajah@stajahlee.com
#  Fri Aug  4 22:52:06 2017
#
# **********************************************************************************
import urllib.request
import sys	
import ssl
import os

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
# FUNCTION:....set_search_url
# PURPOSE:.....uses the url for the OU job search page with specific keyword
# PARAMETERS:..string - keyword for search parameter
# RETURNS:.....string that is the url needed in current search
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def set_search_url(keyword):
	link = 'https://www.ohiouniversityjobs.com/postings/search?utf8=%E2%9C%93&query='
	link = link + keyword
	link = link +'&query_v0_posted_at_date=&225=&commit=Search'
	return link


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....make_page_string
# PURPOSE:.....with given keyword search parameter makes the entire html of a page
# 			   into one single string
# PARAMETERS:..keyword - a string
# RETURNS:.....a string - which is full html of a page
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def make_page_string(keyword):
	return (open_page(set_search_url(keyword)))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....find_jobs
# PURPOSE:.....given a specific keyword the OU job search link will find postings
#              with the keyword as a query parameter
# PARAMETERS:..keyword | string
# RETURNS:.....string describing how many jobs found and their titles, or if none
#              found, will return none-found-message 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #	
def find_jobs(keyword): 
	posts = make_postings_list(make_page_string(keyword))
	jobs = ""
	if (len(posts)!=0):
		for i in posts:
			jobs += (" " + i + "\n")
		print ("\n\nKeyword: " + keyword)
		print ("\n------------------------------------\n")
		print(str(len(posts)) + ' jobs found:\n' + jobs)
		return (str(len(posts)) + ' jobs found: ' + jobs)
	else:
		print ("\n\nKeyword: " + keyword)
		print ("\n------------------------------------\n")		
		print ('No ' + keyword + ' jobs found today - sorry :(')
		return ('No ' + keyword + ' jobs found today.')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....num_jobs
# PURPOSE:.....retrieve number of jobs found with a given search parameter
# PARAMETERS:..keyword | string
# RETURNS:.....integer - number of jobs found
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def num_jobs(keyword):
	return (len(make_postings_list(make_page_string(keyword))))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....notify
# PURPOSE:.....os desktop notification function
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def notify_me_about_awesome_OU_jobs_computer(keyword):
	result=find_jobs(keyword)
	result=result[:result.find(":")]

	# terminal-notifier options:
	title = '-title {!r}'.format("Job Search With Keyword:")
	subtitle = '-subtitle {!r}'.format(keyword)
	sound = '-sound {!r}'.format("Purr.aiff")
	url = '-open {!r}'.format(set_search_url(keyword))
	finish = '-actions {!r}'.format("Finish")
	timeout = '-timeout {!r}'.format(10)

	if (num_jobs(keyword) != 0):
		message = '-message {!r}'.format(result + ". Click to view results.")
	else:
		message = '-message {!r}'.format(result + ".")

	# terminal-notifier sends notification to Mac OS with above options
	os.system('terminal-notifier {}'.format(' '.join([message, title, subtitle, sound, url, finish, timeout])))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# FUNCTION:....main
# PURPOSE:.....scrape OU job posting site for specific keywords and display
#			   a desktop notification with results each morning
# PARAMETERS:..none
# RETURNS:.....none
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def main():	
	
	if (len(sys.argv)>1):
		notify_me_about_awesome_OU_jobs_computer(sys.argv[1])
	else:
		print('Run again with a search term provided')
		sys.exit()

if __name__ == "__main__":
	main()

