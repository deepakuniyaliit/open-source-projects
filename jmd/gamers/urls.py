from django.contrib import admin
from django.urls import path
from gamers import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser, name="logout"),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('pubg',views.pubg,name='pubg'),
    path('services',views.services,name='services'),
    path('matchpt',views.matchpt,name='matchpt'),
    path('addme',views.addme,name='addme'),
    path('acceptr',views.acceptr,name='acceptr'),
    path('search',views.search,name='search'),
    path('autosuggest',views.autosuggest,name='autosuggest'),
    path('deleteid',views.deleteid,name='deleteid'),
    path('delotp',views.delotp,name='delotp'),
    path('addgame',views.addgame,name='addgame'),
    path('gnameautosuggest',views.gnameautosuggest,name='gnameautosuggest'),
]
