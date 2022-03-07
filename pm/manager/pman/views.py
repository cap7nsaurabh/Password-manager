from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
	return render(request,'pman/index.html')
def about(request):
	return HttpResponse('pman/aboutus.html')
def contact(request):
	return HttpResponse('pman/contacts.html',{'team':('Sajag','Saurabh','Rohit')})
def services(request):
	return HttpResponse('pman/services.html')

