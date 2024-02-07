from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re


# Initialize the WebDriver (e.g., Chrome)

driver = webdriver.Chrome()
extracted_data = {}
# Open Twitter          
driver.get("https://twitter.com")
# Wait for the page to load
time.sleep(5)
sign_in_btn = driver.find_element(By.CSS_SELECTOR,"a[data-testid='loginButton']")
sign_in_btn.click()

wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "text")))

username_input.send_keys('@MoizWork') # User-Name enter maar idhr 

next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]")))
next_btn.click()
time.sleep(5)

password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

password_input.send_keys('Moiz123Work')  # Password enter maar idhr 

Login_btn = driver.find_element(By.CSS_SELECTOR,"div[data-testid='LoginForm_Login_Button']")
Login_btn.click()

time.sleep(5)

Search_btn = driver.find_element(By.CSS_SELECTOR,"a[data-testid='AppTabBar_Explore_Link']")
Search_btn.click()

time.sleep(10)

trending_elements = driver.find_elements(By.CSS_SELECTOR,"div[data-testid='trend']")

for index, trending in enumerate(trending_elements[:5]):
    span_elements = trending.find_elements(By.CSS_SELECTOR,("span"))
        
    for SpanNow in span_elements:
        print(f"Hashtag data {index + 1}: {SpanNow.text}")

trending_elements[2].click()
time.sleep(10)
tweet_elements = driver.find_elements(By.CSS_SELECTOR,"article[data-testid='tweet']")

for tweet_index, tweet_now in enumerate(tweet_elements[:1]):
        
    User_avatar = tweet_now.find_element(By.CSS_SELECTOR,"div[data-testid='Tweet-User-Avatar']")
    Image = User_avatar.find_element(By.CSS_SELECTOR,"img")
    Image_url = Image.get_attribute("src")
    print(f"User Profile Image URL is : {Image_url}")

    User_name = tweet_now.find_element(By.CSS_SELECTOR,"div[data-testid='User-Name']")
    span_elements_1 = User_name.find_elements(By.CSS_SELECTOR,"span")
    for span_now_1 in span_elements_1:
        print(f"Name index No : {tweet_index + 1 } is : {span_now_1.text}")
            
    try:
        Verified_profile = tweet_now.find_element(By.CSS_SELECTOR,"svg[data-testid='icon-verified']")
        verify_icon = Verified_profile.find_element(By.CSS_SELECTOR,"path")
        verify_icon = verify_icon.get_attribute("d")
        print(f"User is verified : {verify_icon}")
    except NoSuchElementException:
        print("User not verified")
        
    Tweet_time = tweet_now.find_element(By.CSS_SELECTOR,"time")
    print(f"Tweet Time is : {Tweet_time.text}")

    #Tweet_text = tweet_now.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[2]')
    # Tweet_text = tweet_now.find_element(By.CSS_SELECTOR,"div[data-testid='tweetText']")
    # Locate the tweet text element containing plain text
    tweet_text_element = tweet_now.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']")

    # Find all emoji images within the tweet
    emoji_elements = tweet_text_element.find_elements(By.CSS_SELECTOR, "img[src^='https://abs-0.twimg.com/emoji']")

    # Initialize an empty list to store parts of the tweet text
    tweet_parts = []

    # Iterate through the tweet content and emojis
    for element in tweet_text_element.find_elements(By.XPATH, "./*"):
        if element.tag_name == "img":
            # Handle emoji images
            emoji_src = element.get_attribute("src")
            #emoji_title = element.get_attribute("alt")
            emoji_text = emoji_src if emoji_src else ""
            tweet_parts.append(emoji_text)
        elif element.tag_name == "span":
            # Handle plain text
            tweet_parts.append(element.text)

        # Combine tweet parts into a single text
    tweet_text_with_emojis = " ".join(tweet_parts)

        # Print the tweet text with emojis
    print(f"Tweet Text with Emojis: {tweet_text_with_emojis}")



    Tweet_media = tweet_now.find_elements(By.CSS_SELECTOR,"div[data-testid='tweetPhoto'] , div[data-testid='videoPlayer']")
    for media_index , tweet_media_now in enumerate(Tweet_media[:3]):
        try:
            Tweet_photos = tweet_media_now.find_element(By.CSS_SELECTOR,"div[data-testid='tweetPhoto'] img")
            print(f"Tweet photo is index NO in { media_index + 1 } : {Tweet_photos.get_attribute('src')}")
        except NoSuchElementException:
            try:
                Tweet_video = tweet_media_now.find_element(By.CSS_SELECTOR,"div[data-testid='videoPlayer'] video")
                print(f"Tweet Video Poster is index NO in { media_index + 1 } : {Tweet_video.get_attribute('poster')}")
            except NoSuchElementException:
                print(f"Media {media_index + 1}: Neither Photo nor Video")
                
    
driver.quit()
