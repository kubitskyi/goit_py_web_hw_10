from django.urls import path
from . import views

app_name = 'quotes'
urlpatterns = [
		# представлення поста
		path('', views.quotes_list, name='quotes_list'),
		path('<int:id>/', views.quote_detail, name='quote_detail'),
  		path('authors/', views.authors_list, name='authors_list'),
    	path('authors/<int:id>/', views.author_detail, name='author_detail'),
     	path('tags/<int:id>/', views.tag_detail, name='tag_detail'),
      	path('top-tags/', views.top_tags, name='top_tags'),
       	path('top-authorss/', views.top_authors, name='top_authors'),
        path('add_author/', views.add_author, name='add_author'),  
        path('add_quote/', views.add_quote, name='add_quote'),    
        path('add_tag/', views.add_tag, name='add_tag'),    
]