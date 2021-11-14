from urllib.parse import urlparse
from uuid import uuid4

import rest_framework.pagination
import scrapyd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import (ListView, CreateView, DeleteView)
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from scrapyd_api import ScrapydAPI

from .forms import UserUpdateForm, UserRegisterForm, UserLogin
from django.contrib.auth.forms import AuthenticationForm
from .models import ContractNotice
# Create your views here.
from .serializers import ContractNoticeSerializer


@login_required
def index(request):
    return render(request, 'index.html', {'title': 'Contract Tender Notices ScraperAPI'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created..!')
            return redirect('login')
    else:

        form = UserRegisterForm()
    myform = {
        'form': form

    }
    return render(request, 'registration/registration_form.html', myform)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': 'notices-list',
        'Search': 'search-by-date/<str:date>/',
        'Detail': 'detail-by-id/<str:pk>/',
    }

    return Response(api_urls)

rest_framework.pagination.LimitOffsetPagination.max_limit=10
@api_view(['GET'])
def noticeList(request):
    CNList = ContractNotice.objects.all()
    serializer = ContractNoticeSerializer(CNList, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def noticeSearch(request, date):
    CNList = ContractNotice.objects.filter(date=date)
    serializer = ContractNoticeSerializer(CNList, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getNoticeListByID(request, pk):
    CNList = ContractNotice.objects.get(id=pk)
    serializer = ContractNoticeSerializer(CNList, many=True)

    return Response(serializer.data)


# connect scrapyd service
# noinspection PyRedeclaration0
scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        url = request.POST.get('url', None)  # take url comes from client. (From an input may be?)

        if not url:
            return JsonResponse({'error': 'Missing  args'})

        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.

        # This is the custom settings for scrapy spider.
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd.as
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule('scrapy_app', 'cncrawler',
                                settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                # noinspection PyUnresolvedReferences
                item = ContractNotice.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
