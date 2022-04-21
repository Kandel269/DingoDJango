from uuid import uuid4

from django.core.exceptions import BadRequest
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView

from books.models import BookAuthor, Category, Book


class AuthorListBaseView(View):
    template_name = "author_list.html"
    queryset = BookAuthor.objects.all()  # type: ignore

    def get(self,request: WSGIRequest,*args,**kwargs):
        context = {'authors': self.queryset}
        return render(request, template_name= self.template_name, context= context)

class CategoryListTemplateView(TemplateView):
    template_name = "category_list.html"
    extra_context = {"categories" : Category.objects.all()}   # type: ignore

class BooksListView(ListView):
    template_name = "books_list.html"
    model = Book
    paginate_by = 10

class BooksDetails(DetailView):
    template_name = "book_detail.html"
    model = Book

    def get_object(self, **kwargs):
        return get_object_or_404(Book, id=self.kwargs.get("pk"))


def get_hello(request: WSGIRequest) -> HttpResponse:
    hello = "hello world"
    return render(request, template_name= "hello_world.html", context={"hello_var": hello} )


def get_uuids_a(request: WSGIRequest) -> HttpResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return render(request, template_name= "uuidsaa.html", context={"elements": uuids})
    # return HttpResponse(f"uuids={uuids}")

def get_uuids_b(request: WSGIRequest) -> JsonResponse:
    uuids = [f"{uuid4()}" for _ in range(10)]
    return JsonResponse({"uuids": uuids})

def get_argument_from_path(request: WSGIRequest, x: int, y: str, z: str) -> HttpResponse:
    return HttpResponse(f"x = {x}, y = {y}, z = {z}")

def get_argument_from_query(request: WSGIRequest) -> HttpResponse:
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    print(type(a))
    return HttpResponse(f"a = {a},b = {b},c = {c}")

@csrf_exempt
def check_http_query_type(request: WSGIRequest) -> HttpResponse:
    return render(request, template_name="methods.html", context={})
    # query_type = "Unknown"
    # if request.method == "GET":
    #     query_type = "this is get"
    # elif request.method == "POST":
    #     query_type = "this is post"
    # elif request.method == "PUT":
    #     query_type = "this is put"
    # elif request.method == "DELETE":
    #     query_type = "this is delete"
    # return HttpResponse(query_type)

def get_headers(request: WSGIRequest) -> JsonResponse:
    our_headers = request.headers
    return JsonResponse({"headers": dict(our_headers)})

@csrf_exempt
def raise_error_for_fun(request: WSGIRequest) -> HttpResponse:
    if not request.method == "GET":
        raise BadRequest("method not allowed Dzbanie!")
    return HttpResponse("jest GIT")

