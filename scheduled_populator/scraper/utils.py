import subprocess
import time

import requests
import re
from typing import List
from scheduled_populator.logging_config import logger


def get_site_name(url):
    """
    Get site name from url
    :param url: url string
    :return: string with site name
    """
    # Ensure the URL starts with http or https
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # Regex pattern to extract the domain name without subdomains or extensions
    pattern = r"https?://(?:www\.)?([a-zA-Z0-9-]+)\."

    match = re.search(pattern, url)

    if match:
        # Return the captured domain name
        return match.group(1)
    else:
        return None


def check_robots_txt(url) -> None:
    """
    To check robots.txt file of the given url
    :param url:  to check robots.txt file of the given url
    """

    # Check if URL starts with http or https
    if not url.startswith('http'):
        url = 'http://' + url

    # Append robots.txt to the url
    robots_txt_url = url + '/robots.txt'

    robots_txt_site_name = get_site_name(robots_txt_url)

    try:
        # Send a GET request to fetch the robots.txt
        response = requests.get(robots_txt_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f'Robots.txt file for {url} is obtained successfully.')
            with open(f'robots_txt_files/robots_{robots_txt_site_name}.txt', 'w') as file:
                file.write(response.text)
        else:
            print(f"Could not find robots.txt for {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"An error occurred: {e}")


def format_headline(headlines: List, index: int, source: str) -> str:
    """
    Format headlines according to index in headlines in a given format
    :param headlines: list of headlines
    :param index: index of headline to be formatted
    :param source: source of headline
    :return: formatted headline string
    """
    return f"{source} - {headlines[index].text.strip()} - {headlines[index]['href']}"


def start_selenium_container():
    logger.info("Starting Selenium container")
    docker_run_command = [
        'docker', 'run', '-d', '-p', '4444:4444', '-p', '5900:5900', '--name', 'selenium-chrome-debug', '--shm-size=4g', 'selenium/standalone-chrome-debug'
    ]
    subprocess.run(docker_run_command)
    time.sleep(5)  # Give the container time to start

def stop_selenium_container():
    logger.info("Fetching Selenium container logs before stopping")
    # Fetch and log the container logs
    result = subprocess.run(['docker', 'logs', 'selenium-chrome-debug'], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("Container logs:\n%s", result.stdout)
    else:
        logger.error("Failed to fetch container logs: %s", result.stderr)

    logger.info("Stopping Selenium container")
    subprocess.run(['docker', 'stop', 'selenium-chrome-debug'])
    subprocess.run(['docker', 'rm', 'selenium-chrome-debug'])


if __name__ == '__main__':
    check_robots_txt("http://www.ibef.com/")
    check_robots_txt("http://www.cnbc.com/")
    check_robots_txt("http://www.business-standard.com/")
