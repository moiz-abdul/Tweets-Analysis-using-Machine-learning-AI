from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('usermessage',views.usermessage,name="usermessage"),
    path('signout',views.signout,name="signout"),
    path('forgetpassword',views.forgetpassword,name="forgetpassword"),
    path('otp',views.OTP,name='OTP'),
    path('newpassword',views.newpassword,name='newpassword'),
    path('changepassword',views.changepassword, name='changepassword'),
    path('dashboard',views.dashboard,name="dashboard"),
    path('trending-hashtags/', views.display_trending_hashtags, name='trending-hashtags'),
    path('hashtag-tweets/',views.display_tweets_for_hashtag,name='hashtag_tweets'),
    path('faqs',views.faqs,name='faqs'),
    path('contact',views.contact,name='contact'),
    path('tweetpredict/', views.tweetpredict, name='tweetpredict'),
    path('tweetresult/<str:label>/<str:percentage_score>/', views.tweetresult, name='tweetresult')
]