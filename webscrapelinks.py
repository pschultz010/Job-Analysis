from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pickle

def get_num_pages(url, num_results_per_page):
	''' Scrapes the number of results to determine the number of pages necessary to loop through the entire search results:
	
	Args:
		url (str): The search results link to scrape the number of results off of.     
		num_results_per_page (int): Number of results per page
		
	Returns:
		num_pages (int): The number of pages to scrape    
		
	'''
	#instantiate an HTML session
	session = HTMLSession()
	#create an HTML session with the page
	r = session.get(url)
	#render the page
	r.html.render(sleep=1)
	#parse the html with BeautifulSoup
	bs=BeautifulSoup(r.html.raw_html,'html.parser')
	#extract the number of search results in numerical form
	num_results = bs.find(name='span', id='totalJobCount').text
	print(num_results)
	num_results = int(num_results.replace(',',''))
	print(num_results)
	#calculate the number of results
	if num_results % num_results_per_page > 0:
		num_pages = (num_results // num_results_per_page)+1
	else:
		num_pages = num_results // num_results_per_page
		
	return num_pages

	
def scrape_page(url):
	'''Scrapes all of the job listing links off of the results page
	
	Args:
		url (str): The search results link to scrape job listings off of.
		
	Returns:
		links (list): A list of the job links on the page.
	
	'''
	#instantiate an HTML session
	session = HTMLSession()
	#create an HTML session with the page
	r = session.get(url)
	#render the page
	r.html.render(sleep=0.5)
	#parse the html with BeautifulSoup
	bs=BeautifulSoup(r.html.raw_html,'html.parser')
	#extract all of the <a> tags on the page 
	jobs = bs.find_all(name='a', class_='card-title-link bold')
	#create a list of the href links for every <a> tag
	links = [job['href'] for job in jobs]
	return links

#set a master list to hold all of the links
master_list = []

terms = ['data', 'analyst']
for term in terms:
	url = f'https://www.dice.com/jobs?q={term}&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&language=en'
	print(url)
	num_pages = get_num_pages(url, 100)
	page = 1
	while page <= num_pages:
		inner_url = f'https://www.dice.com/jobs?q={term}&countryCode=US&radius=30&radiusUnit=mi&page={page}&pageSize=100&language=en'
		print('Processed:',inner_url)
		master_list.extend(scrape_page(inner_url))
		page+=1
with open('links.pkl', 'wb') as f:
	pickle.dump(master_list, f)


	
