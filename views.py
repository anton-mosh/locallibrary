# /locallibrary/catalog/views.py
# a

from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from catalog.serializers import BookSerializer

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import APIException

import json
import requests

import logging, logging.config
import sys



def index(request):
    """View function for home page"""

    # Generate counts of objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.count() # 'all() is implied by default

    # Available books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    visits = request.session.get('visits', 0)
    request.session['visits'] = visits+1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_visits': visits,
        'other_context': {
            'p1': 'Hello',
            'p2': 'World',
        }
    }

    return render(request, 'index.html', context=context)



class BookListView(generic.ListView):
    model = Book 
    paginate_by = 3

    # your own name for the list as a template variable
    #context_object_name = 'my_book_list'   

    # Get 3 books #containing the title war
    queryset = Book.objects.all()#[:3]#filter(title__icontains='war')[:3] 

    # Specify your own template name/location       
    template_name = 'book_list.html'  

class BookDetailView(generic.DetailView):
    model = Book
    # Specify your own template name/location       
    #template_name = 'book_detail.html'  


class BookAPIView(APIView):

    parser_classes = (MultiPartParser,FormParser,JSONParser)

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)


        LOGGING = {
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                }
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO'
            }
        }

        logging.config.dictConfig(LOGGING)
        logging.info('Hello')


        return Response({"books": serializer.data})        
    
    def post(self, request):

        def get_answ(msg, sender_name):
            msg = msg.strip().lower()
            answ = ''
            if msg == 'hi':
                answ = 'Hi '+sender_name
            elif msg == 'oxik':
                answ = "Oxik is cute!"
            elif msg == 'how are you':
                answ = "Best of the best"
            elif msg.startswith('/'):
                answ = ''
            else:
                answ = 'What is '+msg+'?'

            return answ


        #book = request.data.get('text')



        LOGGING = {
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                }
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO'
            }
        }

        logging.config.dictConfig(LOGGING)

        logging.info('===')
        try:
            tlg_data = request.data
            logging.info(json.dumps(tlg_data))
        except ParseError as ParseError1:
            logging.info('parse===')
            pass
        except UnsupportedMediaType as UnsupportedMediaType1:
            logging.info('unsupported===')
            pass

        
        sender_name = tlg_data.get('message').get('from').get('first_name')
        chat_id = tlg_data.get('message').get('chat').get('id')
        msg = tlg_data.get('message').get('text')
        answ = get_answ(msg, sender_name)

        logging.info('---')

        aws_url = 'https://qg9jefu6ul.execute-api.eu-west-1.amazonaws.com/default/tlg-api-gateway'
        aws_req = {
            'url': 'https://api.telegram.org/bot',
            'token': '916498389:AAGTrR0ddJwgl07HExUM74uCm5EYh_uvdv0',
            'method': 'sendMessage',
            'body': {
                'chat_id': chat_id,
                'text': answ,
                }
                }        

        logging.info(aws_req)
        logging.info('...')

        #aws_response = requests.post(aws_url, data=json.dumps(aws_req))
        aws_response = requests.post(aws_url, json=aws_req)
        logging.info(aws_response.json())

        return Response(str(aws_response.content), status=status.HTTP_201_CREATED)        

        #return Response('ok', status=status.HTTP_201_CREATED)        
