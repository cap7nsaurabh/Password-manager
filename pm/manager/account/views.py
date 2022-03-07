from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponse
from django.contrib import messages
from account.forms import CustomUserCreationForm,take_cards,EntryForm,meetingform
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from account.models import cards,Entry,Meetings
from Crypto.Cipher import AES
import random
from django.contrib.auth.models import User
# Create your views here.
#sign up form and handles sign up request
def signup_view(request):
	if request.user.is_authenticated:
		return redirect('account:dashboard')
	if request.method=='POST':
		form=CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('account:login')
		else:
			return render(request,'account/signup.html',{'form':form})
	else:
		form=CustomUserCreationForm()
		return render(request,'account/signup.html',{'form':form})

#handles login request
def login_view(request):
	if request.user.is_authenticated:
		return redirect('/account/dashboard')
	if request.method=='POST':
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			user=form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return  redirect(request.POST.get('next'))
			return redirect('account:dashboard')
		else:
			return render(request,'account/login.html',{'form':form})

	else:
		form=AuthenticationForm()
		return render(request,'account/login.html',{'form':form})
	
#handles logout request
def logout_view(request):
	if request.method=='POST':
		logout(request)
		return redirect('home')

#serves dashboardand redirects to login if not authenticated
@login_required(login_url='/account/login')
def dashboard(request):

	us1=User.objects.get(username=request.user)
	print(us1.email)
	ccou=cards.objects.filter(owner=request.user).count()
	pcou = Entry.objects.filter(owner=request.user).count()
	mcou = Meetings.objects.filter(owner=request.user).count()
	return render(request,'account/index2.html',{'username':us1,'fname':us1.first_name,'ccount':ccou,'pcount':pcou,'mcount':mcou})


#serves card list
@login_required(login_url='/account/login')
def card_view(request):
	all_cards=cards.objects.all().filter(owner=request.user)
	return render(request,'account/dis_card.html',{'cards':all_cards})

#serves card form
@login_required(login_url='/account/login')
def cardform(request):
	if request.method=='POST':
		us1=request.user
		new_card=cards(owner=us1)
		form=take_cards(data=request.POST,instance=new_card)
		if form.is_valid():
			form.save()
			return redirect('account:view_cards')
		else:
			return HttpResponse('validation error, re-add card')
	form=take_cards()
	return render(request,'account/cardfill.html',{'form':form})

#serves card view
@login_required(login_url='/account/login')
def card_detail_view(request,slug):
	card=cards.objects.get(slug=slug,owner=request.user)
	return render(request,'account/card_detail.html',{'data':card})

#handles password entry
@login_required(login_url='/account/login')
def add_entry(request):
	key = request.user.password[10:26].encode('cp855')
	cipher = AES.new(key, AES.MODE_EAX)
	nonce = cipher.nonce
	if request.method=='POST':
		form=EntryForm(data=request.POST)
		if form.is_valid():
			ent=form.save(commit=False)
			encrypted,tag=cipher.encrypt_and_digest(form.cleaned_data['password'].encode('cp855'))
			print(encrypted)
			print(type(encrypted))
			ent.password=encrypted.decode('cp855')
			ent.nonce=nonce.decode('cp855')
			ent.owner=request.user
			ent.save()
			return redirect('account:list_pass')
		else:
			return render(request,'account/passentry.html',{'form':form})

	form=EntryForm()
	return render(request,'account/passentry.html',{'form':form})

#list passwords
@login_required(login_url='/account/login')
def list_viewp(request):
	all_pass=Entry.objects.all().filter(owner=request.user)
	return render(request,'account/listp.html',{'pass':all_pass})

#servves password detail view
@login_required(login_url='/account/login')
def detailp_view(request,slug):
	ent=Entry.objects.get(slug=slug,owner=request.user)
	enc_pass=ent.password.encode('cp855')
	enc_nonce=ent.nonce.encode('cp855')
	key = request.user.password[10:26].encode('cp855')
	decipher=AES.new(key, AES.MODE_EAX,nonce=enc_nonce)
	decrypted=decipher.decrypt(enc_pass).decode('cp855')
	cypher="abcdefghijklmnopqrstuvwxyz"
	inc=random.randint(1,255)%26
	newstring=""
	for i in range(0,len(decrypted)):
		if decrypted[i] not in cypher:
			newstring+=decrypted[i]
			continue
		pos=cypher.find(decrypted[i])
		newpos=(pos+inc)%26
		newstring+=cypher[newpos]
	return render(request,'account/pass_detail.html',{'entry':ent,'pass':newstring,'inc':inc})

@login_required(login_url='/account/login')
def meeting_fill(request):
	if request.method=='POST':
		us1=request.user
		new_meeting=Meetings(owner=us1)
		form=meetingform(data=request.POST,instance=new_meeting)
		if form.is_valid():
			form.save()
			return redirect('account:list_meet')
		else:
			return HttpResponse('validation error, re-add meeting')
	form=meetingform()
	return render(request,'account/meetingfill.html',{'form':form})

@login_required(login_url='/account/login')
def listmeet(request):
	all_meet=Meetings.objects.all().filter(owner=request.user)
	return render(request,'account/listmeet.html',{'meets':all_meet})



@login_required(login_url='/account/login')
def meetdetail(request,slug):
	meet = Meetings.objects.get(slug=slug, owner=request.user)
	return render(request, 'account/meet_detail.html', {'data': meet})

@login_required(login_url='/account/login')
def delc(request,slug):
	card=cards.objects.filter(slug=slug,owner=request.user).delete()
	return render(request,'account/dis_card.html',{"message":"Card deleted successfully"})
@login_required(login_url='/account/login')
def delp(request,slug):
	ent=Entry.objects.filter(slug=slug,owner=request.user).delete()
	return render(request,'account/listp.html',{"message":"Password deleted successfully"})
@login_required(login_url='/account/login')
def delm(request,slug):
	meet=Meetings.objects.filter(slug=slug,owner=request.user).delete()
	return render(request,'account/listmeet.html',{"message":"Meeting detail deleted successfully"})
