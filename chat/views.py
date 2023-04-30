from django.shortcuts import render, redirect
 
def chatList(request):
    return render(request, 'chats.html')
 

