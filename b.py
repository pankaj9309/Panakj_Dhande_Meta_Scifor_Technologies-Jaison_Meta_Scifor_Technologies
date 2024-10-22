from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import time

def get_video_links_and_ids(url, max_links=500):
    """Extracts video links and IDs from Dailymotion up to a specified limit.

    Args:
        url (str): The URL of the Dailymotion channel or playlist.
        max_links (int, optional): The maximum number of links to extract. Defaults to 500.

    Returns:
        list, dict: A list of video links and a dictionary containing video IDs and their counts.
    """

    driver = webdriver.Chrome()  # Replace with your preferred WebDriver
    driver.get(url)

    links = set()  # Use a set to ensure unique links
    video_id_counts = Counter()

    while len(links) < max_links:
        old_links_length = len(links)
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Find video elements
        new_links = driver.find_elements(By.XPATH, "//a[@data-testid='video-card']")
        for link in new_links:
            href_value = link.get_attribute('href')
            if href_value and href_value not in links:
                links.add(href_value)
                # Extract video ID
                video_id = href_value.split('/')[-1]
                video_id_counts[video_id] += 1

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(3)  # Adjust wait time as needed

        # Check if scrolling reached the end or we have 500 links
        new_height = driver.execute_script("return document.body.scrollHeight")
        if old_links_length == len(links) and last_height == new_height:
            break
        if len(links) >= max_links:
            break

    # Truncate the links list to exactly max_links if it exceeds
    links = list(links)[:max_links]

    driver.quit()
    return links, video_id_counts

# Example usage
url = "https://www.dailymotion.com/tseries2"
links, video_id_counts = get_video_links_and_ids(url)

print("You can find the Video ID by looking for the hash value that comes after \"video/\" in the URL.")

print("\nExtracted video links (exactly 500):")
for link in links:
    print(link)

# Find the most frequent character and its count
all_video_ids = "".join(video_id_counts.keys())
char_counts = Counter(all_video_ids)
most_frequent_char, max_count = char_counts.most_common(1)[0]

print("\nMost frequent character:", most_frequent_char)
print("Frequency:", max_count)
print(f"{most_frequent_char}:{max_count}")
