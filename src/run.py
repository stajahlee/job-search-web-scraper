import urllib.request
import sys
import ssl
import os


### returns the entire webpage as a string
def open_page(link):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	req = urllib.request.Request(link)
	response = urllib.request.urlopen(req, context=ctx)
	charset = response.headers.get_content_charset()
	webpage = response.read().decode(charset)
	return webpage


### returns an array containing a posted job opening in each element
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


# returns the url with query as a string
def set_search_url(keyword):
	link = 'https://www.ohiouniversityjobs.com/postings/search?utf8=%E2%9C%93&query='
	link = link + keyword
	link = link +'&query_v0_posted_at_date=&225=&commit=Search'
	return link


# returns a string of the webpage based on the query
def make_page_string(keyword):
	return (open_page(set_search_url(keyword)))


# returns a string of how many jobs and what they were	
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

	
# returns the number of jobs that were found
def num_jobs(keyword):
	return (len(make_postings_list(make_page_string(keyword))))


# OS X notification
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


def main():	
	
	if (len(sys.argv)>1):
		notify_me_about_awesome_OU_jobs_computer(sys.argv[1])
	else:
		print('Run again with a search term provided')
		sys.exit()

if __name__ == "__main__":
	main()
