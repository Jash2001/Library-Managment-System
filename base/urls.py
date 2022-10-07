from unicodedata import name
from django.urls import path
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('', views.logout, name='logout'),
    
    path('student-login/', views.studentLogin, name='student-login'),
    path('student-home/', views.studentLoginValidation, name='login-validation'),
    # path('student/', views.studentHome, name='studenthome'),
    path('studenthome/<rollno>/', views.studentHomeList, name='studenthomelist'),
    path('student-home/book/<bookid>/<rollno>/', views.books, name='bookinfo'),
    path('request-book/<bookid>/<rollno>/', views.requestBook, name = 'request-book' ),
    path('student-home/requests/<rollno>', views.requestPage, name='request-page'),
    path('requests/<rollno>/', views.bookLendings, name = 'view-bookrequests'),
    path('student-home/dues/<rollno>', views.duesPage, name='dues-page'),
    path('dues/<rollno>/', views.bookDues, name = 'view-bookdues'),

    path('student-login/student-signup/', views.studentSignup, name='student-signup'),
    path('student-login/student-signup/add/', views.addStudentDetails, name='signup'),


    path('librarianhome/', views.bookList, name='librarianhome'),
    path('librarian-login/', views.librarianLogin, name='librarian-login'),
    path('librarian-home/', views.librarianLoginValidation, name='librarian-login-validation'),

    path('librarian-login/librarian-signup/', views.librarianSignup, name='librarian-signup'),
    path('librarian-login/librarian-signup/add/', views.addLibrarianDetails, name='signup'),

    path('librarian-home/addbooks/', views.addBooks, name='add-books'),
    path('addbooks/add/', views.addBookInfo, name='add-bookdetails'),
    path('librarian-home/updatebooks/', views.updateBooksPage, name='update-book'),
    path('librarian-home/checkbooks/', views.checkBook, name='check-book'),
    path('updatebooks/updatedetails/', views.updateBook, name='update-book-details'),
    path('viewRequests/', views.displayRequests, name='view-request-page'),
    path('viewRequests/<rollno>/<bookid>/<status>/', views.updateRequest, name='update-request')
]