from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm, TagForm
from django.contrib import messages

# Create your views here.


# Create your views here.
def quotes_list(request):
	quotes_list = Quote.objects.all().order_by('-id')
	paginator = Paginator(quotes_list, 15)
	page_number = request.GET.get('page', 1)
	quotes = paginator.page(page_number)
	return render(request,'app_quotes/quotes/quotes_list.html',{'quotes': quotes})

def quote_detail(request, id):
	try:
		quote = Quote.objects.get(id=id)
		if quote.tags == None:
			tags = []
		else:
			tags = quote.tags.all()
	except Quote.DoesNotExist:
		raise Http404("No Post found.")
		
	return render(request,'app_quotes/quotes/quote_details.html',{'quote': quote, 'tags':tags })

def authors_list(request):
	authors_list = Author.objects.all().order_by('-id')
	paginator = Paginator(authors_list, 15)
	page_number = request.GET.get('page', 1)
	authors = paginator.page(page_number)
	return render(request,'app_quotes/authors/authors_list.html',{'authors': authors})

def author_detail(request, id):
	try:
		author = Author.objects.get(id=id)
		qoutes = Quote.objects.filter(owner = author).all()
	except Quote.DoesNotExist:
		raise Http404("No Post found.")
	return render(request,'app_quotes/authors/author_details.html',{'quotes': qoutes, 'author':author })

def top_authors(request):
	top_authors = Author.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
	return render(request,'app_quotes/authors/top_authors.html',{'top_authors': top_authors })



def tag_detail(request, id):
	try:
		tag = Tag.objects.get(id=id)
		quotes = Quote.objects.filter(tags=tag)
	except Quote.DoesNotExist:
		raise Http404("No Post found.")
	return render(request,'app_quotes/tags/tag_detail.html',{'tag': tag, 'quotes': quotes })

def top_tags(request):
	top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
	return render(request,'app_quotes/tags/top_tags.html',{'top_tags': top_tags })


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        print(form)
        if form.is_valid():
            is_exists = Author.objects.filter(fullname = form.cleaned_data['fullname'])
            if is_exists:
                return render(request, 'app_quotes/authors/author_form.html', {'form': form})
            else:	
                form.save()
                return redirect(to='quotes:quotes_list')
        else:
            messages.error(request, 'Error updating author.')
            return render(request, 'app_quotes/authors/author_form.html', {'form': form})
    return render(request, 'app_quotes/authors/author_form.html', {'form': AuthorForm()})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():	
            form.save()
            return redirect(to='quotes:quotes_list')
        else:
            messages.error(request, 'Error updating author.')
            return render(request, 'app_quotes/quotes/quote_form.html', {'form': form})
    return render(request, 'app_quotes/quotes/quote_form.html', {'form': QuoteForm()})

@login_required
def add_tag(request):
    if request.method == 'POST':
        tagform = TagForm(request.POST)
        if tagform.is_valid():	
            tagform.save()
            return redirect(to='quotes:add_quote')
        else:
            messages.error(request, 'Error updating author.')
            return render(request, 'app_quotes/tags/add_tag.html', {'tagform': tagform})
    return render(request, 'app_quotes/tags/add_tag.html', {'tagform': TagForm()})