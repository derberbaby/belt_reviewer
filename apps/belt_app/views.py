from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import User, UserManager, Book, Author, Review, ReviewManager
# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Book.objects.all().delete()
    # Author.objects.all().delete()
    # Review.objects.all().delete()
    return render(request, 'belt_app/index.html')

def register(request):
    post_data = request.POST.copy()
    result = User.objects.register(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user'] = result
    return redirect(reverse('main'))

def login(request):
    post_data = request.POST.copy()
    result = User.objects.login(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user'] = result
    return redirect(reverse('main'))

def main(request):
    user = User.objects.get(id=request.session['user'])
    reviews = Review.objects.all().order_by('-created_at')[:3]
    exclude = reviews.values('book')
    books = Book.objects.exclude(id__in=exclude)
    context = {
        'user': user,
        'reviews': reviews,
        'books': books
    }
    return render(request, 'belt_app/books.html', context)

def create(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'belt_app/add.html', context)

def add(request):
    post_data = request.POST.copy()
    result = Review.objects.add(post_data, request.session['user'])
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('create'))
    else:
        book = Book.objects.get(id=result)
        return redirect('/books/'+str(book.id))

def book(request, book_id):
    user = User.objects.get(id=request.session['user'])
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    authors = Author.objects.filter(books__id=book_id)
    faves = Book.objects.filter(favorited_by__id=user.id)
    context = {
        'user': user,
        'book': book,
        'reviews': reviews,
        'authors': authors,
        'faves': faves,
    }
    return render(request, 'belt_app/book.html', context)

def review_book(request, book_id):
    post_data = request.POST.copy()
    result = Review.objects.review_book(post_data, request.session['user'], book_id)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect('/books/'+str(book_id))
    else:
        return redirect('/books/'+str(book_id))

def fave(request, book_id):
    user = User.objects.get(id=request.session['user'])
    book = Book.objects.get(id=book_id)
    add_fave_book = book.favorited_by.add(user)

    origin = request.META['HTTP_REFERER']
    page = origin.replace('http://'+request.META['HTTP_HOST'], '')
    return redirect(page)

def user(request, user_id):
    me = User.objects.get(id=request.session['user'])
    user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(user = user)
    friends = User.objects.filter(friend=user)
    faves = Book.objects.filter(favorited_by=user.id)
    context = {
        'user': user,
        'reviews': reviews,
        'friends': friends,
        'me': me,
        'faves': faves
    }
    return render(request, 'belt_app/user.html', context)

def add_friend(request, friend_id):
    user = User.objects.get(id=request.session['user'])
    new_friend = User.objects.get(id=friend_id)
    friendship = user.friend.add(new_friend)

    origin = request.META['HTTP_REFERER']
    page = origin.replace('http://'+request.META['HTTP_HOST'], '')
    return redirect(page)

def author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(book_authors=author)
    context = {
        'author': author,
        'books': books
    }
    return render(request, 'belt_app/author.html', context)

def delete(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()

    origin = request.META['HTTP_REFERER']
    page = origin.replace('http://'+request.META['HTTP_HOST'], '')
    return redirect(page)

# def del_auth(request, book_id, author_id):
#     book = Book.objects.get(id=book_id)
#     bye_author = Author.objects.get(id=author_id)
#     book.author.remove(bye_author)
#
#     origin = request.META['HTTP_REFERER']
#     page = origin.replace('http://'+request.META['HTTP_HOST'], '')
#     return redirect(page)

def del_friend(request, friend_id):
    me = User.objects.get(id=request.session['user'])
    bye_friend = User.objects.get(id=friend_id)
    me.friend.remove(bye_friend)

    origin = request.META['HTTP_REFERER']
    page = origin.replace('http://'+request.META['HTTP_HOST'], '')
    return redirect(page)

def home(request):
    return redirect(reverse('main'))

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))
