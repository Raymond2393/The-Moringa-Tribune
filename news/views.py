import datetime as dt
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Article
from django.contrib.auth.decorators import login_required
from .forms import NewArticleForm, NewsLetterForm





# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to the Moringa Tribune')

def past_days_news(request,past_date):
	try:
	    # Converts data from the string Url
	    date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
	except ValueError:
		# Raise 404 error when ValueError is thrown
		raise Http404()
		assert False

	if date == dt.date.today():
		return redirect(news_today)

	news = Article.days_news(date)

	return render(request,'all-news/past-news.html',{"date": date,"news":news})

def news_today(request):
    date = dt.date.today()
    return render(request, 'all-news/today-news.html', {"date": date,})


def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html',{"date": date,"news":news})
# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})
