from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, decorators
from .models import Content
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AddForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from .serializers import GetContent, GetUser
from django.db.models import Q
from django.contrib.auth.models import User, Group
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'home/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        account = authenticate(request, username=username, password=password)
        if account is None:
            return render(request, 'home/login.html', {'f': "Tài khoản không tồn tại"})
        login(request, account)
        # print(account.user_permissions.all())
        return HttpResponseRedirect('/content/')


class Logout(View):
    def get(self, request):
        pass

    def post(self, request):
        logout(request)
        return render(request, 'home/login.html')


class ContentClass(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        data_list = Content.objects.all()
        paginator = Paginator(data_list, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/content.html', {"page_obj": page_obj})


class AddContent(PermissionRequiredMixin, View):
    permission_required = 'home.add_content'

    def get(self, request):
        f = AddForm()
        return render(request, 'home/add.html', {'f': f})

    def post(self, request):
        data = AddForm(request.POST)
        if data.is_valid():
            data.save()
        return HttpResponseRedirect('/content/')


class ContentDetailClass(PermissionRequiredMixin, View):
    permission_required = 'home.change_content'

    def get(self, request, id):
        data = Content.objects.get(id=id)
        return render(request, 'home/change.html', {'data': data})

    def post(self, request, id):
        old_data = Content.objects.get(id=id)
        new_data = AddForm(request.POST, instance=old_data)
        new_data.save()
        return HttpResponseRedirect('/content/')


class DeleteContent(PermissionRequiredMixin, View):
    permission_required = 'home.delete_content'
    def get(self, request, id):
        q = Content.objects.get(id=id)
        q.delete()
        return HttpResponseRedirect('/content/')

# API
class GetContent1(APIView):
    def get(self, request):
        list_content = Content.objects.all()
        # list_content = Content.objects.filter(Q(total_mac__gte=5000) | Q(number_of_pop_tail__gte=30))
        mydata = GetContent(list_content, many=True)
        return Response(mydata.data, status=status.HTTP_200_OK)

    def post(self, request):
        new_data = request.data['data']
        data = AddForm(new_data)
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class GetContent2(APIView):
    def get(self, request, value1, value2):
        list_content2 = Content.objects.filter(total_mac=value1, number_of_pop_tail=value2)
        mydata2 = GetContent(list_content2, many=True)
        return Response(mydata2.data, status=status.HTTP_200_OK)


class GetUserInfo(APIView):
    def get(self, request):
        list_user = User.objects.all()
        mydata = GetUser(list_user, many=True)
        return Response(mydata.data, status=status.HTTP_200_OK)

    def post(self, request):
        # print(request.data)
        username = request.data['username']
        password = request.data['password']
        account = authenticate(request, username=username, password=password)
        if account is None:
            return Response({'auth': 'false'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # login(request, account)
        user = User.objects.get(username=username)
        group = user.groups.all()[0]
        permission = user.get_all_permissions()
        return Response((username, str(group), permission), status=status.HTTP_200_OK)


class DeleteContentAPI(APIView):
    def post(self, request):
        id_del = request.data['data']
        del_data = Content.objects.get(id=id_del)
        del_data.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateContentAPI(APIView):

    def post(self, request):
        update_data = request.data['data']
        old_data = Content.objects.get(id=update_data['id'])
        new_data = AddForm(update_data, instance=old_data)
        new_data.save()
        return Response(status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    def post(self, request):
        print(request.data)
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        group_name = request.data['group']
        user = User.objects.create_user(username=username, password=password, email=email)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        user.save()
        permission = user.get_all_permissions()
        return Response(permission, status=status.HTTP_200_OK)


class SortContentAPI(APIView):
    def post(self, request):
        titleSort = request.data['titleSort']
        typeSort = request.data['typeSort']
        if typeSort == 'up':
            sorted_content = Content.objects.all().order_by(titleSort)
        else:
            sorted_content = Content.objects.all().order_by(titleSort).reverse()
        mydata = GetContent(sorted_content, many=True)
        return Response(mydata.data, status=status.HTTP_200_OK)

class SearchContentAPI(APIView):
    def post(self, request):
        dataSearch = request.data['dataSearch']
        dataSearchType = request.data['dataSearchType']
        search_content = Content.objects.filter(('%s__startswith' % dataSearchType, dataSearch))
        mydata = GetContent(search_content, many=True)
        return Response(mydata.data, status=status.HTTP_200_OK)


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = GetContent
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = '__all__'
    search_fields = ['__all__']
    ordering_fields = '__all__'