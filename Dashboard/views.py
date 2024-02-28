from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "dashboard/home.html")

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST["title"],
                description=request.POST["description"],
            )
            notes.save()

        messages.success(
            request, f"notes added from {request.user.username} sucessfully"
        )
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    return render(request, "dashboard/notes.html", {"notes": notes, "form": form})

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()

    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST["subject"],
                title=request.POST["title"],
                description=request.POST["description"],
                due=request.POST["due"],
                is_finished=finished,
            )
            homeworks.save()
            messages.success(request, f"homework added from {request.user.username}")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    return render(
        request,
        "dashboard/homework.html",
        {"homework": homework, "homework_done": homework_done, "form": form},
    )

@login_required
def update_homework(request, pk=1):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False

    else:
        homework.is_finished = True

    homework.save()
    return redirect(request, "homework")

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    if request.method == "POST":
        form = Dashboardform(request.POST)
        text = request.POST["text"]
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()["result"]:
            result_dict = {
                "input": text,
                "title": i["title"],
                "duration": i["duration"],
                "thumbnails": i["thumbnails"][0]["url"],
                "channel": i["channel"]["name"],
                "link": i["link"],
                "viewCount": i["viewCount"]["short"],
                "published": i["publishedTime"],
            }
            desc = ""
            if i["descriptionSnippet"]:
                for j in i["descriptionSnippet"]:
                    desc += j["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)
        return render(
            request, "dashboard/youtube.html", {"form": form, "results": result_list}
        )

    else:

        form = Dashboardform()
    return render(request, "dashboard/youtube.html", {"form": form})

@login_required
def todo(request):
    if request.method == "POST":
        form = Todoform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            todo = Todo(
                user=request.user, title=request.POST["title"], is_finished=finished
            )
            todo.save()
            messages.success(request, f"Todo Added from {request.user.username}")
    else:
        form = Todoform
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    return render(
        request,
        "dashboard/todo.html",
        {"todos": todos, "todos_done": todos_done, "form": form},
    )

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True

    todo.save()
    return redirect("todo")

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = Dashboardform(request.POST)
        text = request.POST["text"]
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                "title": answer["items"][i]["volumeInfo"]["title"],
                "subtitle": answer["items"][i]["volumeInfo"].get('subtitle'),
                "description": answer["items"][i]["volumeInfo"].get('description'),
                "count": answer["items"][i]["volumeInfo"].get('pageCount'),
                "categories": answer["items"][i]["volumeInfo"].get('categories'),
                "rating": answer["items"][i]["volumeInfo"].get('pageRating'),
                "thumbnail": answer["items"][i]["volumeInfo"].get('imageLinks').get('thumbnail'),
                "preview": answer["items"][i]["volumeInfo"].get('previewLink')
            }
            result_list.append(result_dict)
        return render(
            request, "dashboard/books.html", {"form": form, "results": result_list}
        )

    else:

        form = Dashboardform()
    return render(request, "dashboard/books.html", {"form": form})






def dictionary(request):
    if request.method=='POST':
        form=Dashboardform(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
        except:
            form=Dashboardform()
        return render(request,'dashboard/dictionary.html',{'form':form,'input':text ,'phonetics':phonetics,'audio':audio,'definition':definition,'example':example, 'synonyms':synonyms
                                                       })
    
    else:
     form=Dashboardform()
    return render(request,'dashboard/dictionary.html',{'form':form})                                                



def wiki(request):
    if request.method=='POST':
        text=request.POST['text']
        form=Dashboardform(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
     form=Dashboardform()
     context={
        'form':form
    }
    return render(request,'dashboard/wiki.html',context)



def register(request):
    if request.method=='POST':
        form=UserRegisterationForm(request.POST)
        if form .is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"account created for {username}!!")
            return redirect("login")
    else:

            form=UserRegisterationForm()
    context={
        'form':form
    }
    return render(request,'dashboard/register.html',context)


@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done= True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done= True
    else:
        todos_done=False
    context={
        'homeworks':homeworks,
         'todos':todos,
         'homework_done':homework_done,
         'todos_done':todos_done
    }
    return render(request,'dashboard/profile.html',context)




