from xml.dom import ValidationErr
from django.shortcuts import render, redirect

from library.settings import MEDIA_ROOT
from .models import StudentDetails, LibrarianDetails, BookDetails, BookLendings
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from django.template import loader

from django.core.paginator import Paginator

from datetime import datetime, timedelta

# Create your views here.

def index(request):
    return render(request, 'base/index.html')

def studentSignup(request):
    return render(request, 'base/student_signup.html')

def addStudentDetails(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    rollno = request.POST['rollno']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    flag = False

    if password == confirm_password:
        studentObjects_list = list()
        for stdnt in StudentDetails.objects():
            studentObjects_list.append(stdnt.to_json())


        for stdnt in studentObjects_list:
            if stdnt['rollno'] == rollno:
                error_message = "Roll No Already Exist"
                flag = True
                break
            if stdnt['email_id'] == email:
                error_message = "Email Id '" + email + "' Already Exist"
                flag = True
                break
    else:
        error_message = "Password did not match"
        flag = True
    
    if flag:
        return render(request, "base/student_signup.html", {"error_message" : error_message})

    studentDetails = StudentDetails(firstname = firstname, lastname = lastname, rollno = rollno, email = email, username = username, password = password, confirm_password = confirm_password)
    studentDetails.save() 
    return render(request, 'base/student_login.html')

def studentLogin(request):
    return render(request, "base/student_login.html")

def studentLoginValidation(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        student = StudentDetails.objects.get(email = email, password = password)
        student = student.to_json()
        rollno = student['rollno']
        return redirect('/studenthome/' + str(rollno) + '/')
    except:
        return render(request, "base/student_login.html", {"error_message" : "Incorrect Username or Password"})



def librarianSignup(request):
    return render(request, 'base/librarian_signup.html')

def addLibrarianDetails(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    empid = request.POST['empid']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    flag = False

    if password == confirm_password:
        librarianObjects_list = list()
        for emp in LibrarianDetails.objects():
            librarianObjects_list.append(emp.to_json())


        for emp in librarianObjects_list:
            if emp['empid'] == empid:
                error_message = "Roll No Already Exist"
                flag = True
                break
            if emp['email_id'] == email:
                error_message = "Email Id '" + email + "' Already Exist"
                flag = True
                break
    else:
        error_message = "Password did not match"
        flag = True
    
    if flag:
        return render(request, "base/librarian_signup.html", {"error_message" : error_message})

    librarianDetails = LibrarianDetails(firstname = firstname, lastname = lastname, empid = empid, email = email, username = username, password = password, confirm_password = confirm_password)
    librarianDetails.save() 
    return render(request, 'base/librarian_login.html')


def librarianLogin(request):
    return render(request, "base/librarian_login.html")
    

def librarianLoginValidation(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        librarian = LibrarianDetails.objects.get(email = email, password = password)
        librarian = librarian.to_json()
        bookObjects_list = list()
    
        for book in BookDetails.objects():
            bookObjects_list.append(book.to_json())
        return render(request, "base/librarian_home.html", {"bookObjects_list" : bookObjects_list})
    except:
        return render(request, "base/librarian_login.html", {"error_message" : "Incorrect Username or Password"})
    

def logout(request):
    return render(request, "base/index.html")


def librarianHome(request):
    return render(request, "base/librarian_home.html")

def studentHome(request):
    return render(request, "base/student_home.html")

# @login_required(login_url='student-home/')
def studentHomeList(request, rollno):
    search = request.POST.get('search')
    booklendings_list = list()

    for book in BookLendings.objects():
        books = book.to_json()
        if books['rollno'] == int(rollno) and (books['pending'] == 1 or books['approved'] == 1):
            booklendings_list.append(books['bookid'])

    if search and len(search) > 0:
        flag = False
        booksObjects_list = list()
        for book in BookDetails.objects():
            book = book.to_json()
            if book['bookid'] in booklendings_list:
                continue
            if search.lower() in book['bookname'].lower():
                booksObjects_list.append(book)
                flag = True
                
            elif search.lower() in book['author'].lower():
                booksObjects_list.append(book)
                flag = True
    
        if flag:
            return render(request, "base/student_home.html", {"bookObjects_list" : booksObjects_list, "rollno":rollno})
        else:
            return render(request, "base/student_home.html", {"error_message" : "There is no such book", "rollno" : rollno})
    bookObjects_list = list()
    for book in BookDetails.objects().order_by('bookname'):
        book = book.to_json()
        if book['bookid'] in booklendings_list or book['noofcopies'] == 0:
                continue
        bookObjects_list.append(book)
    
    p = Paginator(bookObjects_list, 3)
    page = request.GET.get('page')
    home = p.get_page(page)
    nums = "a" * home.paginator.num_pages
    return render(request, "base/student_home.html", {"bookObjects_list" : bookObjects_list, "rollno":rollno, "home" : home, "nums" : nums})

def books(request, bookid, rollno):
    try:
        book = BookLendings.objects.get(bookid = bookid, rollno = rollno, pending = 1).to_json()
        book = BookDetails.objects.get(bookid = bookid).to_json()
        bookname = book['bookname']
        author = book['author']
        summary = book['summary']
        bookimage = book['bookimage']
        return render(request, "base/bookinfo.html", {"bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno, "visited" : True})
    except:
        book = BookDetails.objects.get(bookid = bookid).to_json()
        bookname = book['bookname']
        author = book['author']
        summary = book['summary']
        bookimage = book['bookimage']
        return render(request, "base/bookinfo.html", {"bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno})

def requestBook(request, bookid, rollno):
    book = BookDetails.objects.get(bookid = bookid)
    if book.noofcopies == 0:
        bookid = book.bookid
        bookname = book.bookname
        author = book.author
        summary = book.summary
        bookimage = book.bookimage
        return render(request, "base/bookinfo.html", {"flag" : True, "bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno})
    
    current_date = datetime.now()
    today = str(current_date.day) + "-" + str(current_date.month) + "-" + str(current_date.year)
    date1 = datetime.strptime(today, "%d-%m-%Y").date()
    books = BookLendings.objects.filter(bookid = bookid, rollno = rollno, pending = 0, approved = 0)
    if len(books) != 0:
        bks = None
        for b in books:
            bks = b
        date2 = bks.requesteddate
        date2 = datetime.strptime(date2, "%d-%m-%Y").date()
        diff = date1 - date2
        diff = diff.days
        bookid = book.bookid
        bookname = book.bookname
        author = book.author
        summary = book.summary
        bookimage = book.bookimage
        if diff == 0:
            return render(request, "base/bookinfo.html", {"temp" : True, "bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno})
    

    pending_list = list()
    approved_list = list()
    for cnt in BookLendings.objects():
        cnt = cnt.to_json()
        if cnt['rollno'] == int(rollno):
            if cnt['pending'] == 1:
                pending_list.append(cnt)
            if cnt['approved'] == 1:
                approved_list.append(cnt)
    if len(pending_list) + len(approved_list) >= 3:
        bookid = book.bookid
        bookname = book.bookname
        author = book.author
        summary = book.summary
        bookimage = book.bookimage
        return render(request, "base/bookinfo.html", {"limit" : True, "bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno})

    current_date = datetime.now()
    today = str(current_date.day) + "-" + str(current_date.month) + "-" + str(current_date.year)
    booklendings = BookLendings(bookid = bookid, rollno = rollno, pending = 1, approved = 0, requesteddate = today)
    booklendings.save()
    book.noofcopies -= 1
    book.save()

    bookid = book.bookid
    bookname = book.bookname
    author = book.author
    summary = book.summary
    bookimage = book.bookimage

    return render(request, "base/bookinfo.html", {"bookid" : bookid, "bookname" : bookname, "author" : author, "summary" : summary, "bookimage" : bookimage, "rollno" : rollno, "visited" : True})

def requestPage(request, rollno):
    return render(request, "base/student_request.html", {"rollno": rollno})

def bookLendings(request, rollno):
    bookrequests = list()
    status = ""
    for book in BookLendings.objects.filter(rollno = rollno):
        books = book.to_json()
        bookid = books['bookid']
        requesteddate = books['requesteddate']
        status = "Rejected"

        if books['pending'] == 1:
            status = "Pending"
        elif books['approved'] == 1:
            status = "Approved"
        book = BookDetails.objects.get(bookid = bookid).to_json()
        bookname = book['bookname']
        author = book['author']
        bookrequests.append({'bookname' : bookname, 'author' : author, "requesteddate" : requesteddate, "status" : status})
    return render(request, 'base/student_request.html', {"bookrequests" : bookrequests, "status" : status, 'rollno' : rollno})

def duesPage(request, rollno):
    return render(request, "base/student_dues.html", {"rollno": rollno})

def bookDues(request, rollno):
    bookdues = list()
    for book in BookLendings.objects.filter(rollno = rollno):
        books = book.to_json()
        bookid = books['bookid']
        if books['approved'] == 1:
            date1 = books['requesteddate']
            date1 = datetime.strptime(date1, "%d-%m-%Y").date()
            duedate = date1 + timedelta(days=7)
            duedate = duedate.strftime("%d-%m-%Y")
            bookDetails = BookDetails.objects.get(bookid = bookid).to_json()
            bookname = bookDetails['bookname']
            bookdues.append({'bookname' : bookname, 'duedate' : duedate})
    return render(request, 'base/student_dues.html', {"bookdues" : bookdues, "rollno" : rollno})




def bookList(request):
    search = request.POST.get('search')
    if search and len(search) > 0:
        flag = False
        booksObjects_list = list()
        for book in BookDetails.objects():
            book = book.to_json()
            if str(book['bookid']) == search:
                booksObjects_list.append(book)
                flag = True
                
            elif search.lower() in book['bookname'].lower():
                booksObjects_list.append(book)
                flag = True
                
            elif search.lower() in book['author'].lower():
                booksObjects_list.append(book)
                flag = True
    
        if flag:
            return render(request, "base/librarian_home.html", {"bookObjects_list" : booksObjects_list})
        
    bookObjects_list = list()
    for book in BookDetails.objects():
        bookObjects_list.append(book.to_json())

    p = Paginator(bookObjects_list, 3)
    page = request.GET.get('page')
    home = p.get_page(page)
    nums = "a" * home.paginator.num_pages
    return render(request, "base/librarian_home.html", {"bookObjects_list" : bookObjects_list, "home" : home, "nums" : nums})

def addBooks(request):
    return render(request, "base/addbooks.html")

def addBookInfo(request):

    bookid = request.POST['bookid']
    bookname = request.POST['bookName']
    author = request.POST['author']
    summary = request.POST['summary']
    bookimage = request.POST['bookimage']
    noofcopies = request.POST['noofcopies']

    bookimage =  "images/" + bookimage 

    error_message = "Book Added Successfully"

    flag = False
    bookObjects_list = list()
    
    for book in BookDetails.objects():
        bookObjects_list.append(book.to_json())
    
    for book in bookObjects_list:
        if book['bookid'] == bookid or book['bookname'] == bookname:
            error_message = "Book Already Exist"
            flag = True
            break
    
    if flag:
        return render(request, "base/addbooks.html", {"error_message" : error_message})
    
    bookDetails = BookDetails(bookid = bookid, bookname = bookname, author = author, summary = summary, bookimage = bookimage, noofcopies = noofcopies)
    bookDetails.save() 
    return render(request, "base/librarian_home.html")

def updateBooksPage(request):
    return render(request, "base/updatebooks.html")

def checkBook(request):
    bookid = request.POST['bookid']
    flag = False
    book_id = ""
    for books in BookDetails.objects():
        if str(books['bookid']) == bookid:
            book_id = books
            flag = True
            break 
    if not flag:
        return render(request, "base/updatebooks.html", {"error_message" : "There is no such book"})
    return render(request, "base/updatebooks.html", {"bookid" : book_id['bookid'], "bookname" : book_id['bookname'], "author" : book_id['author'], "summary": book_id['summary'], "bookimage" : book_id['bookimage'], "noofcopies" : book_id['noofcopies']})

def updateBook(request):
    bookid = request.POST['book_id']
    bookname = request.POST['bookName']
    author = request.POST['author']
    summary = request.POST['summary']
    bookimage = request.POST['bookimage']
    noofcopies = request.POST['noofcopies']
    book = BookDetails.objects.get(bookid = bookid)
    book.bookname = bookname
    book.author = author
    book.summary = summary
    book.noofcopies = noofcopies
    if len(bookimage) > 0:
        book.bookimage = "images/" + bookimage
    book.save()
    return render(request, "base/updatebooks.html", {"success" : "Data Successfully Updated"})

def librarianViewRequestPage(request):
    return render(request, 'base/librarian_request.html')

def displayRequests(request):
    booklending_list = list()
    for student in StudentDetails.objects():
        students = student.to_json()
        rollno = students['rollno']
        firstname = students['firstname']
        lastname = students['lastname']
        name = firstname + " " + lastname
        for lending in BookLendings.objects.filter(rollno = rollno):
            lendings = lending.to_json()
            if lendings['pending'] == 1:
                bookid = lendings['bookid']
                book = BookDetails.objects.get(bookid = bookid)
                books = book.to_json()
                bookname = books['bookname']
                author = books['author']
                booklending_list.append({'rollno' : rollno, 'name' : name, 'bookname' : bookname, 'author' : author, 'bookid' : bookid})
    if len(booklending_list) != 0:
        return render(request, 'base/librarian_request.html', {'booklending_list' : booklending_list})
    return render(request, 'base/librarian_request.html', {'error_message' : "No Requests"})

def updateRequest(request,rollno,bookid,status):
    booklendings = BookLendings.objects.get(rollno = rollno, bookid = bookid, pending = 1)
    booklendings.pending = 0
    booklendings.approved = 1
    current_date = datetime.now()
    today = str(current_date.day) + "-" + str(current_date.month) + "-" + str(current_date.year)
    if int(status) == 0:
        booklendings.approved = 0
        book = BookDetails.objects.get(bookid = bookid)
        book.noofcopies += 1
        book.save()
    booklendings.requesteddate = today 
    booklendings.save()
    return displayRequests(request) 
            
