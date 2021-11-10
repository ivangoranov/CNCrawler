from urllib.parse import urlparse
from uuid import uuid4

import scrapyd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import (ListView, CreateView, DeleteView)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from scrapyd_api import ScrapydAPI

from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from .models import ContractNotice, Profile
# Create your views here.
from .serializers import ContractNoticeSerializer, ProfileSerializer


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'track/about.html', {'title': 'about '})  # title is optional


def first_view(request):
    return render(request, 'track/first_view.html')


def why(request):
    return render(request, 'track/why.html')


def benefits(request):
    return render(request, 'track/benefits.html')


def announce(request):
    return render(request, 'track/announcements.html')


# Create your views here.
class ContractNoticeViewSet(viewsets.ModelViewSet):
    # noinspection PyUnresolvedReferences
    queryset = ContractNotice.objects.all()
    serializer_class = ContractNoticeSerializer


class ContractNoticetListView(ListView):
    model = ContractNotice
    template_name = 'track/home.html'  # <app>/<model>_<viewtype>.html ...django searches for this covention template

    context_object_name = 'contract-notices'  # i dont understand where we defined this 'posts'...eariler home() was being called..there
    # 'posts' was defined but now when we give route as blog/ it will come diretly to postview class
    # we never defining  'posts':Post.objects.all(),.....but still it works
    ordering = ['-date']
    paginate_by = 1  # how manay pages you want to show on home page


class ContractNoticeCreateView(LoginRequiredMixin, CreateView):
    model = ContractNotice

    fields = ['date']
    #fields = ['date', 'notice_number', 'tender_name', 'procedure_state',
    #          'contract_type', 'type_of_procurement', 'estimated_value']
    # noinspection PyUnresolvedReferences
    context = {

        'products': ContractNotice.objects.all(),
        'title': 'Home'

    }

    #def form_valid(self, form):
    #    f = self.new_product(form)
    #    if f == 1:
    #        messages.success(
    #            self.request,
    #            'Product Added successfully! We will notify you via email when price drop under your desire price',
    #        )
#
    #        return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))
    #    if f == 0:
    #        messages.warning(
    #            self.request,
    #            "Invalid URL or couldn't find proper price of product..try again",
    #        )
#
    #        return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))
#
    #def new_product(self, form):
    #    print('attempting to insert new records')
    #    import time
#
    #    import sys
    #    # this path will remain in sys.path untill this program terminated
    #    sys.path.append("/app")
    #    sys.path.append("/app/price_scraper")  # in heroku we have base dir as /app
#
    #    # this path will be used in price_scraper.items,
    #    from data_collection.data_collection.spiders import contract_notices_spider
#
    #    from scrapy import signals
    #    from scrapy.crawler import Crawler
#
    #    from crochet import setup
#
    #    setup()
    #    print('hello' * 10)
#
    #    if form == -1:
#
    #        url = self.product_url
#
    #        settings = {
    #            'url': url,
    #            'USER_AGENT': 'price_scraper (+http://www.yourdomain.com)',
    #            'timepass': 'kya chal raha hai bhai'
    #        }
#
    #        def spider_closing(spider):
    #            """Activates on spider closed signal"""
    #            print("Spiderclose" * 10)
    #            # reactor.stop()
#
    #        crawler = Crawler(contract_notices_spider.contract_notices, settings)
#
    #        crawler.signals.connect(spider_closing, signal=signals.spider_closed)
#
    #        p_obj = self
#
    #        crawler.crawl(product_object=p_obj, check=1)
#
    #        while True:
    #            time.sleep(1)
    #            # print(crawler.stats.get_stats())
    #            try:
    #                fr = crawler.stats.get_stats()['finish_reason']
    #                if fr == 'finished':
    #                    break
    #            except:
    #                pass
#
#
#
    #    else:
    #        print("we are in else part")
    #        url = self.request.POST['product_url']
    #        d_price = self.request.POST['desire_price']
#
    #        settings = {
    #            'url': url,
    #            'USER_AGENT': 'price_scraper (+http://www.yourdomain.com)',
    #            'timepass': 'kya chal raha hai bhai'
    #        }
#
    #        def spider_closing(spider):
    #            """Activates on spider closed signal"""
    #            print("Spiderclose" * 10)
#
    #        def if_spyder_open(spider):
    #            print("spyderOpen__" * 10)
#
    #        u = self.request.user
    #        ulen1 = len(u.product_set.all())
#
    #        crawler = Crawler(contract_notices_spider.contract_notices, settings)
#
    #        crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    #        crawler.signals.connect(if_spyder_open, signal=signals.spider_opened)
#
    #        crawler.crawl(url=url, d_price=d_price, author=self.request.user, check=0, timepass='whats up..!!')
#
    #        while True:
    #            print(crawler.stats.get_stats())
    #            time.sleep(1)
    #            try:
    #                fr = crawler.stats.get_stats()['finish_reason']
    #                if fr == 'finished':
    #                    break
    #            except:
    #                pass
    #        ulen2 = len(u.product_set.all())
    #        if ulen2 > ulen1:
    #            return 1
    #        elif ulen2 == ulen1:
    #            return 0

# todo:
#class ContractNoticeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#    model = ContractNotice
#    fields = ['date', 'notice_number', 'tender_name', 'procedure_state',
#              'contract_type', 'type_of_procurement', 'estimated_value']
#    template_name = 'track/update_form.html'
#
#    def form_valid(self, form):
#        messages.success(self.request, f'Updated successfully!')
#        form.instance.author = self.request.user
#        return super().form_valid(form)
#
#    def test_func(self):  # this fucntion restric user to update others post..he can update only his own post not others
#        # UserPassesTestMixin thats why we write this
#        ContractNotice = self.get_object()
#        if self.request.user == product.author:
#            return True
#        return False


class ContractNoticeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ContractNotice
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserContractNoticeListView(ListView):  # when we click on title tis executed
    model = ContractNotice
    template_name = 'track/user_products.html'  #
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # noinspection PyUnresolvedReferences
        return ContractNotice.objects.filter(author=user).order_by('-date_posted')


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
    return render(request, 'users/register.html', myform)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,

    }

    return render(request, 'users/profile.html', context)


class ContractNoticeList(APIView):
    def get(self, request, format=None):
        # noinspection PyUnresolvedReferences
        all_notices = ContractNotice.objects.all()
        serializers = ContractNoticeSerializer(all_notices, many=True)
        return Response(serializers.data)


class ProfileList(APIView):
    def get(self, request, format=None):
        # noinspection PyUnresolvedReferences
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)


# connect scrapyd service
# noinspection PyRedeclaration
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

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        task = scrapyd.schedule('default', 'icrawler',
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
