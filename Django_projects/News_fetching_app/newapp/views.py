from django.shortcuts import render
from newsapi.newsapi_client import NewsApiClient
# Create your views here.


def index(request):
    newsApi = NewsApiClient(api_key = "0a86e664118a4b95afd01a53604a43c2")
    headLines = newsApi.get_top_headlines(sources ='engadget')
    articles = headLines['articles']
    desc = []
    news = []
    image = []

    for i in range(len(articles)):
        article = articles[i]
        desc.append(article['description'])
        news.append(article['title'])
        image.append(article['urlToImage'])

    List = zip(news, desc, image)


    return render(request, "main/mainbody.html", context={"List": List})