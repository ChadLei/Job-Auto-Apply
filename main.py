from greenhouse import *
from multiprocessing import Process
import os
# Use this url for testing success:
# https://boards.greenhouse.io/niantic/jobs/4787160002/confirmation
# https://boards.greenhouse.io/ultramobile/jobs/4179347003/confirmation

'''Reads in a file of job urls'''
def job_url_reader(file_name):
    with open(file_name, 'r') as filetoread:
        urls = filetoread.readlines()
    return urls

'''Removes job from 'scraped_jobs.txt' after successfully applying to them.'''
def file_rewrite(file_name,job_urls,job_index):
    updated_urls = job_urls.pop(job_index)
    with open(file_name, 'w') as filetowrite:
        filetowrite.writelines(job_urls)

'''Can be used for a quick test on a single url'''
def quickCall(url):
    greenhouse(url, 1)

def main():
    job_urls = job_url_reader('scraper_and_scraped_urls/scraped_jobs.txt')
    counter = 1
    urls_to_remove = []

    for job in job_urls:
        if (greenhouse(job.strip('\n'), counter)):
            counter += 1
            urls_to_remove.append(job)
    for job in urls_to_remove:
        file_rewrite('scraper_and_scraped_urls/scraped_jobs.txt',job_urls, job_urls.index(job))




if __name__ == '__main__':
    main()
    # quickCall('https://boards.greenhouse.io/smarkets/jobs/2388721#application')
