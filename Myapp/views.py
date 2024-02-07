from django.shortcuts import render,redirect
from Myapp.models import Uzerlogin,PasswordResetOTP,UserMessage
from Myapp.forms import CreateUserForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.password_validation import validate_password,CommonPasswordValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.forms import ModelForm
from django.contrib.auth import authenticate,login,logout
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.utils import timezone
import random
#from django.conf import Settings
from django.core.mail import send_mail
from Myproject import settings
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.service import Service
from .MLmodel import predict_tweet

#from Scraping.Selenium import extract_data     ---->> THIS IS FOR SCRAPING DIRECTORY <<----


# Create your views here.



# HOME  FUNCTION 


def home(request):
    return render(request,"Myapp/index.html")


# HOME  FUNCTION END


# SIGN-UP  FUNCTION  


def signup(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirmPassword']

        try:
            CheckEmail = Uzerlogin.objects.get(Email = email)
            messages.error(request,"Email already exist !")   
        except:
            if len(password1) < 8:
                messages.error(request," Password must be atleast 8 characters long !")
            else:
                try:
                    validate_password(password1,password_validators=[CommonPasswordValidator()])
                except ValidationError:
                    messages.error(request,'password is too common !')
                if(password1 == password2):
                    encryptedPassword = make_password(password1)
                    Newuser = Uzerlogin.objects.create(Username = username, Email = email, password = encryptedPassword)
                    Newuser.save()
                    messages.success(request,'Your account has been created successully ! ')
                    return redirect('signin')
                else:
                    messages.error(request,'Password do not match')
   
    return render(request,"Myapp/signup.html")


# SIGN-UP  FUNCTION  END

# SIGN-In  FUNCTION 

def signin(request):
    
    if request.method == "POST":
        Useremail = request.POST["email"]
        Userpass = request.POST["password"]

        try:
            Checkemail = Uzerlogin.objects.get(Email= Useremail)
            #print("user exist")
        
            if Checkemail.is_active:
                if check_password(Userpass , Checkemail.password):
                    request.session['Uzerlogin-ID'] = Checkemail.id
                    username = Checkemail.Username
                    # messages.success(request,'You have Sucessfully logged in !')
                    #return redirect('trending-hashtags')
                    return render(request,"Myapp/trendinghashtags.html",{'username': username})
                else:
                    messages.error(request, 'Password do not match !')
            else:
                messages.error(request,"Sorry you are blocked by admin !")

        except Uzerlogin.DoesNotExist:
            messages.error(request,"User does not exist ! ")  
            
    return render(request,"Myapp/signin.html",{})


# SIGN-In  FUNCTION OUT


# SIGNOUT  FUNCTION    

def signout(request):
    logout(request)
    # messages.success(request,"Logout successfully !")
    return redirect('signin')

# SIGNOUT  FUNCTION  END


# User Message FUNCTION 


def usermessage(request):
    if request.method == "POST":
        Name = request.POST['name']
        email = request.POST['email']
        PoNumber = request.POST['phonenumber']
        message = request.POST['Message']

        NewMessage = UserMessage.objects.create(PersonName = Name , Email = email , PhoneNumber = PoNumber , Message = message)
        NewMessage.save()

    return render(request, "Myapp/Usermessage.html")

# User Message FUNCTION END 


# FORGOT PASSWORD FUNCTION 

def forgetpassword(request):

    if request.method == "POST":
        email = request.POST['email']
        
        try:
            UserEmail = Uzerlogin.objects.get(Email = email)
            
            user_Otp = random.randint(0,9)
            expiration_time = timedelta(minutes=5)

            otp_instance = PasswordResetOTP.objects.create(
                User_login = UserEmail,
                OTP = user_Otp,
                OTP_create = timezone.now(),
                OTP_expire = timezone.now() + expiration_time     
            )

            request.session['Reset_email'] = email

            """
            Subject = "Password Reset OTP"
            Message = f"<p>Please enter the OTP from you Email , To reset your password ! </p>"
            From_Email = settings.EMAIL_HOST_USER
            recipient_list = [UserEmail.Email]

            send_mail(Subject,Message,From_Email,recipient_list)
            request.session['Reset_email '] = email

            """
            messages.success(request,'OTP send to your Email, Plase enter OTP to reset your password')
            messages.success(request,user_Otp)
            return redirect('OTP')
            
        except  Uzerlogin.DoesNotExist:
            messages.error(request, ' Sorry account with that email does not exist')

    return render(request,"Myapp/forgetpassword.html")


# FORGOT PASSWORD FUNCTION END 


# OTP FUNCTION 


def OTP(request):
    email = request.session.get('Reset_email')
    if request.method == 'POST':

        OTP = request.POST['OTP']
    
        if not OTP:
            print("Enter OTP from Email ! ")
        else:
            try:
                user = Uzerlogin.objects.get(Email = email)  
                otp_instance = PasswordResetOTP.objects.filter(User_login=user).latest('OTP_create')

                if otp_instance.is_expired():
                    return HttpResponse("OTP has expired , please enter the new one !")
                
                else:
                    if str(OTP) == str(otp_instance.OTP):
                        return redirect('newpassword')
                    else:
                        return HttpResponse("Invalid OTP, Please enter again !")
                    
            except Uzerlogin.DoesNotExist:
                return HttpResponse("Invalid Email address ! ")
            
    return render(request,"Myapp/OTP.html")


# OTP FUNCTION END


# New Password FUNCTION


def newpassword(request):
    email = request.session.get('Reset_email')
    # user = email
    if request.method == "POST":
        new_pass = request.POST['newpassword']
        confirm_pass = request.POST['confirmpassword']
        if new_pass != confirm_pass:
            messages.error(request,"Both Password should be match")
        else:
            if len(new_pass) < 8:
                messages.error(request, " Password must be atleast 8 characters !")
            else:
                try:
                    
                    user = Uzerlogin.objects.get(Email = email)  
                    user.password = make_password(new_pass)
                    user.save()
                    messages.success(request,"Your password has changed sucessfully ")
                    return redirect('signin')
                except Uzerlogin.DoesNotExist:
                    messages.error(request,"Invalid Email address ! ")
                
    #print(user)
    return render(request,"Myapp/Newpassword.html")

# New Password FUNCTION END

def changepassword(request):
    if request.method == "POST":
        email = request.POST['email']
        old_pass = request.POST['oldpassword']
        new_pass = request.POST['newpassword']
        retype_pass = request.POST['confirmpassword']
        try:
            user = Uzerlogin.objects.get(Email = email)
            if user:
                passmatched = check_password(old_pass, user.password)
                if passmatched:
                    #messages.success(request,"  Password Matched !")

                    if new_pass != retype_pass:
                        messages.error(request,"Both Password should be match")
                    else:
                        if len(new_pass) < 8:
                            messages.error(request,"Password must me at least 8 character")
                        else:    
                            user.password = make_password(new_pass)
                            user.save()
                            messages.success(request," Your password has changed successfully ") 
                            return redirect('signin')
                else:
                    messages.error(request,"  Password not match !")
            else:
                messages.error(request," Account with this email does not exist !")

            
            
        except Uzerlogin.DoesNotExist:
            messages.error(request," Old Password Incorrect !")
    
    return render(request, "Myapp/changepassword.html")


# TWITTER Political HASHTAGS & Keywords FUNCTION



def display_trending_hashtags(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        # Assuming the username is stored in a field called 'username'
        username = request.user.username  # Retrieve the username of the logged-in user
        print(username)
    else:
        # Handle the case if the user is not logged in
        username = None 

    # Pass the trending hashtags to the template
    return render(request, 'Myapp/trendinghashtags.html' , {'username': username})



# TWITTER Political HASHTAGS & Keywords FUNCTION END


def display_tweets_for_hashtag(request):
    ''' if request.user.is_authenticated:  # Check if the user is logged in
        # Assuming the username is stored in a field called 'username'
        username = request.user.username  # Retrieve the username of the logged-in user
        print(username)
    else:
        # Handle the case if the user is not logged in
        username = None '''

    key = request.GET.get('key', '') 
    # Initialize the WebDriver (e.g., Chrome)
    #chrome_driver_path = 'D:/Abdullah Work/FYP/Chrome drivers/chromedriver'
    #driver = webdriver.Chrome(chrome_driver_path)
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()

    # Open Twitter
    try:
        driver.get("https://twitter.com")
        # Wait for the page to load
        time.sleep(5)
        sign_in_btn = driver.find_element(By.CSS_SELECTOR, "a[data-testid='loginButton']")
        sign_in_btn.click()

        wait = WebDriverWait(driver, 10)
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        username_input.send_keys('@MoizWork')
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]")))
        next_btn.click()
        time.sleep(5)

        password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys('Moiz123Work')

        Login_btn = driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']")
        Login_btn.click()
        time.sleep(5)

        search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='SearchBox_Search_Input']")))
        search_input.send_keys(key)
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)

        for _ in range (20):
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            time.sleep(5)

        tweet_elements = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
        
        tweets_for_hashtag = []

        # Tweet Data extraction
        
        for tweet_index, tweet_now in enumerate(tweet_elements[:10]):
            
            User_avatar = tweet_now.find_element(By.CSS_SELECTOR,"div[data-testid='Tweet-User-Avatar']")
            Image = User_avatar.find_element(By.CSS_SELECTOR,"img")
            Image_url = Image.get_attribute("src")
            #print(f"User Profile Image URL is : {Image_url}")

            User_name = tweet_now.find_element(By.CSS_SELECTOR,"div[data-testid='User-Name']")
            span_elements_1 = User_name.find_elements(By.CSS_SELECTOR,"span")
            user_name = ""

            for span_now_1 in span_elements_1:
                user_name += span_now_1.text + " "
                #print(f"Name index No : {tweet_index + 1 } is : {span_now_1.text}")
            
            user_name = " ".join(sorted(set(user_name.strip().split()), key=lambda x: user_name.strip().split().index(x)))
                
            try:
                Verified_profile = tweet_now.find_element(By.CSS_SELECTOR,"svg[data-testid='icon-verified']")
                verify_icon = Verified_profile.find_element(By.CSS_SELECTOR,"path")
                verify_icon = verify_icon.get_attribute("d")
                #print(f"<p>User is verified : {verify_icon} </p>")
            except NoSuchElementException:
                verify_icon = None
            
            Tweet_time = tweet_now.find_element(By.CSS_SELECTOR,"time")
            Tweet_time = Tweet_time.text

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
            #print(f"Tweet Text with Emojis: {tweet_text_with_emojis}")

            #tweets_for_hashtag = []

            Tweet_media = tweet_now.find_elements(By.CSS_SELECTOR,"div[data-testid='tweetPhoto'] , div[data-testid='videoPlayer']")

            for media_index , tweet_media_now in enumerate(Tweet_media[:3]):
                media_dict = {}
                
                try:
                    Media = tweet_media_now.find_element(By.CSS_SELECTOR,"div[data-testid='tweetPhoto'] img")
                    media_dict["Media_Type"] = "Photo"
                    media_dict["Media_URL"] = Media.get_attribute('src')
                except NoSuchElementException:
                    try:
                        Media = tweet_media_now.find_element(By.CSS_SELECTOR,"div[data-testid='videoPlayer'] video")
                        media_dict["Media_Type"] = "Video"
                        media_dict["Media_URL"] = Media.get_attribute('poster')
                    except NoSuchElementException:
                        media_dict["Media_Type"] = "None"

            reply = tweet_now.find_element(By.CSS_SELECTOR, "div[data-testid='reply']")
            reply = reply.text

            retweet = tweet_now.find_element(By.CSS_SELECTOR, "div[data-testid='retweet']")
            retweet = retweet.text

            view = 9500
            View = view

            def parse_k_number(text):
                text = text.strip().replace(',', '')  
                if text[-1] == 'K':
                    return int(float(text[:-1]) * 1000) 
                return int(text)

            # Example usage:
            like = tweet_now.find_element(By.CSS_SELECTOR, "div[data-testid='like']")
            like_text = like.text
            like_count = parse_k_number(like_text)


            tweets_for_hashtag.append({
                            "User_Profile_Image_URL": Image_url,
                            "User_Name": user_name.strip() ,
                            "User_Verified": verify_icon,
                            "Tweet_Time": Tweet_time,
                            "Tweet_Text_with_Emojis": tweet_text_with_emojis,
                            "Tweet_Media": media_dict,
                            "Comments": reply,
                            "Retweets": retweet,
                            "Likes": like_count,
                            "Views": view
                        })

        return render(request,'Myapp/hashtag_tweets.html',{'tweets_for_hashtag': tweets_for_hashtag})
    
    
    except Exception as e:
        print("Error:",str(e))
    
    finally:
        driver.quit()
    
    return render(request,"Myapp/hashtag_tweets.html",{'tweets_for_hashtag':[]})

# EXTRACT TWITTER TRENDING HASHTAG TWEETS FUNCTION  END 



# ML MODEL Predict Tweet FUNCTION

def tweetpredict(request):
    if request.method == 'POST':
        # Get data from the form
        tweet_text = request.POST.get('tweet_text', '')
        
        # Convert the values to integers, or use 0 if the list is empty
        likes_count = int(request.POST.get('likes_count', 0) or 0)
        retweets_count = int(request.POST.get('retweets_count', 0) or 0)
        comment_count = int(request.POST.get('comment_count', 0) or 0)
        views_count = int(request.POST.get('views_count', 0) or 0)

        # Call the function to predict the tweet
        prediction = predict_tweet(tweet_text, likes_count, retweets_count, comment_count, views_count)

        # Set label and percentage score based on prediction
        percentage_score = '89%' if prediction == 1 else '17%'
        label = 'Real' if prediction == 1 else 'Fake'

        return redirect('tweetresult', label=label , percentage_score = percentage_score)

    return render(request, "Myapp/hashtag_tweets.html", {'tweets_for_hashtag': []})



# ML MODEL Predict Tweet FUNCTION END


# Tweet Result FUNCTION

def tweetresult(request, label, percentage_score):
    

    context = {
        'label': label,
        'percentage_score': percentage_score,
    }
    return render(request, 'Myapp/tweetresult.html', context)



# Tweet Result FUNCTION  END


# DASHBOARD PAGE FUNCTION

def dashboard(request):
    return render(request,"Myapp/dashboard.html")


# FAQ's PAGE FUNCTION 

def faqs(request):
    return render(request,"Myapp/faqs.html")

# DASHBOARD PAGE FUNCTION  END

def contact(request):
    return render(request,"Myapp/contactus.html")
