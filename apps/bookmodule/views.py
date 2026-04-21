from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from .models import Book, Address, Publisher
from django.db.models import Count
from django.db.models import F, ExpressionWrapper, FloatField, Sum


def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    return render(request, "bookmodule/list_books.html")


def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")


def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def links(request):
    return render(request, "books/html5/links.html")

def formatting(request):
    return render(request, "books/html5/formatting.html")

def listing(request):
    return render(request, "books/html5/listing.html")

def tables(request):
    return render(request, "books/html5/tables.html")

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]
def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_task1.html', {'books': books})

def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_task2.html', {'books': books})

def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_task3.html', {'books': books})

def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8_task4.html', {'books': books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/lab8_task5.html', {'stats': stats})

def lab8_task7(request):
    data = Address.objects.annotate(num_students=Count('student'))
    return render(request, 'bookmodule/lab8_task7.html', {'data': data})

def lab9_task1(request):
    from django.db.models import Sum

    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total']

    books = Book.objects.annotate(
        percentage=ExpressionWrapper(
            (F('quantity') * 100.0) / total_quantity,
            output_field=FloatField()
        )
    )

    return render(request, 'bookmodule/lab9_task1.html', {'books': books})

def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})

def lab9_task3(request):
    publishers = Publisher.objects.annotate(oldest_pubdate=Min('book__pubdate'))

    data = []
    for publisher in publishers:
        oldest_book = Book.objects.filter(
            publisher=publisher,
            pubdate=publisher.oldest_pubdate
        ).first()

        data.append({
            'publisher_name': publisher.name,
            'location': publisher.location,
            'oldest_book_title': oldest_book.title if oldest_book else '',
            'oldest_pubdate': publisher.oldest_pubdate
        })

    return render(request, 'bookmodule/lab9_task3.html', {'data': data})

def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})

def lab9_task5(request):
    from django.db.models import Count, Q

    publishers = Publisher.objects.annotate(
        high_rated_books=Count('book', filter=Q(book__rating__gte=4))
    )

    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})

def lab9_task6(request):
    from django.db.models import Count, Q

    publishers = Publisher.objects.annotate(
        filtered_books_count=Count(
            'book',
            filter=Q(book__price__gt=50, book__quantity__lt=5, book__quantity__gte=1)
        )
    )

    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})

