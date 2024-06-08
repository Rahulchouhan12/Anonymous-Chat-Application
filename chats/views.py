from django.shortcuts import render, redirect
from django.contrib import admin
from chats.models import SignUp,ChattingDb,Blocks
from django.http import HttpResponse, JsonResponse,HttpRequest
import datetime


admin.site.register(SignUp)
admin.site.register(ChattingDb)
admin.site.register(Blocks)

def Home(request):
	return render(request,"Index.html")

def login(request):
	if request.method=="POST":
		email= request.POST['User_email']
		password=request.POST['pswd']
		email=email.upper()
		data=SignUp.objects.all()

		for i in data:
			if email==i.email:
				if password==i.password:
					key=i.id
					print("Hello ", i.name)
					#msg="<h1> "+"Hello " + i.name +"</h1>"
					msg="Welcome "+i.name
					#return render(request,"chat.html",{"Msg":msg})

					return Globalchat(request,key);
					
				else:
					msg="Incorrect Password"
					print(msg)
					return render(request,"login.html",{"Msg":msg})

		msg="User Not Found"
		print(msg)
		return render(request,"login.html",{"Msg":msg})
	return render(request,"login.html")


def Globalchat(request,key):
	data=SignUp.objects.get(id=key)
	Username=data.name
	Chats= ChattingDb.objects.filter(reciever="All")
	#users=ChattingDb.objects.values_list("sender","yop").distinct()
	#users=ChattingDb.objects.filter(reciever=data.enroll).values_list('sender','yop','id').distinct()
	block_contacts=[]
	block_contacts_detail= Blocks.objects.filter(user=data.id)
	allchats=[]
	AllUser=[]
	Temp_alluser=[]
	RecentChats= ChattingDb.objects.filter(reciever=data.enroll)|ChattingDb.objects.filter(sender=data.enroll)
	RecentChats=RecentChats.exclude(reciever="All")
	for i in block_contacts_detail:
		block_contacts.append(i.blocked)

	for i in Chats:
		if i.sender not in block_contacts:
			allchats.append(i)
	for i in RecentChats:
		if(i.sender==data.enroll):
			temp=SignUp.objects.get(enroll=i.reciever)
		else:
			temp=SignUp.objects.get(enroll=i.sender)

		if temp not in Temp_alluser:
			for i in RecentChats:
				unseen_msg=0
				if i.msgseen==False:
					unseen_msg+=1
			Temp_alluser.append(temp)
			AllUser.append([temp,unseen_msg])	
	AllUser=AllUser[::-1]
	#for i in RecentChats:
		#print(i.reciever)

	if request.method=="POST" and 'messageChat' in request.POST:
		msg=request.POST['messageChat']
		entry=ChattingDb(sender=data.enroll,msg=msg,reciever='All',yop=data.YOP,time=datetime.datetime.now())
		entry.save()
		return redirect('Globalchat',key=key)
	return render(request,"chat.html",{"Username":Username,"KEY":key,"Chats":allchats,"mydata":data,"users":AllUser,"blocks":block_contacts})

def privateChat(request,key,rkey):
	mydata = SignUp.objects.get(id=key)
	second = SignUp.objects.get(enroll=rkey)
	#users=ChattingDb.objects.values_list("sender","yop").distinct()
	#users=ChattingDb.objects.filter(reciever=mydata.enroll).values_list('sender','yop','id').distinct()
	data = ChattingDb.objects.filter(sender=mydata.enroll, reciever=rkey) | ChattingDb.objects.filter(sender=rkey, reciever=mydata.enroll)
	Chats= ChattingDb.objects.filter(reciever=mydata.enroll)|ChattingDb.objects.filter(sender=mydata.enroll)
	Chats=Chats.exclude(reciever="All")
	block_contacts=[]
	block_contacts_detail= Blocks.objects.filter(user=mydata.id)
	allchats=[]
	AllUser=[]
	Temp_alluser=[]


	for i in block_contacts_detail:
		block_contacts.append(i.blocked)

	for i in Chats:
		if(i.sender==mydata.enroll):
			temp=SignUp.objects.get(enroll=i.reciever)
		else:
			temp=SignUp.objects.get(enroll=i.sender)

		if temp not in Temp_alluser:
			for i in data:
				unseen_msg=0
				if i.msgseen==False:
					unseen_msg+=1
					#i.msgseen=True
			Temp_alluser.append(temp)
			AllUser.append([temp,unseen_msg])
	AllUser=AllUser[::-1]

	#for i in AllUser[0]:
	#	print(i.name)

	if request.method == "POST" and 'messageChat' in request.POST:
		msg = request.POST["messageChat"]
		entry = ChattingDb(sender=mydata.enroll, reciever=rkey, msg=msg,yop=mydata.YOP,time=datetime.datetime.now())
		entry.save()
		data = ChattingDb.objects.filter(sender=mydata.enroll, reciever=rkey) | ChattingDb.objects.filter(sender=rkey, reciever=mydata.enroll)
		return redirect('privateChat', key=key, rkey=rkey)
	return render(request, "chatP.html", {"Chats": data, "mydata": mydata, "second": second, "KEY": key,"users":AllUser})


def delete_entry(request, key, msgid):
    mysid = SignUp.objects.get(id=key)
    entry = ChattingDb.objects.get(sender=mysid.enroll, id=msgid)
    entry.delete()
    return redirect('Globalchat', key=key)

def delete_entry2(request, key, rkey, msgid):
    mysid = SignUp.objects.get(id=key)
    entry = ChattingDb.objects.get(sender=mysid.enroll, id=msgid)
    entry.delete()
    return redirect('privateChat', key=key, rkey=rkey)

def Profile(request,key):
	mydata=SignUp.objects.get(id=key)
	chats=ChattingDb.objects.all()
	total=0
	mypost=0
	connect=set()
	block_contacts_detail=Blocks.objects.filter(user=key)
	blockedby=Blocks.objects.filter(blocked=mydata.enroll)


	for i in chats:
		total=total+1;
		if i.sender==mydata.enroll:
			mypost=mypost+1
			last=i.time

		if i.reciever==mydata.enroll:
			connect.add(i.reciever)
	dataofprofile={"mydata":mydata,"KEY":key,"total":total,"mypost":mypost,"connection":len(connect),"last":last,
	"blocks":len(block_contacts_detail),"blockedby":len(blockedby),"listofblocks":block_contacts_detail}
	return render(request,"Profile.html", dataofprofile)


def about(request):
	return render(request,"about.html")


def services(request):
	return render(request,"service.html")


def signup(request):
	if request.method=='POST':
		Username= request.POST['Name']
		email= request.POST['User_email']
		email=email.upper()
		enroll= request.POST['enroll']
		enroll=enroll.upper()
		password= request.POST['pswd']
		yop= request.POST['yop']
		gender= request.POST['gender']
		course= request.POST['course']
		data=SignUp.objects.all()

		for i in data:
			if i.email==email or i.enroll==enroll:
				print("User Already Exist")
				return render(request,"signup.html")

		entry= SignUp(name=Username,email=email,password=password,enroll=enroll, Gender=gender,course=course,YOP=yop)
		entry.save()
		print("Account created Successfully")
		return login(request)


	return render(request,"signup.html")


def block(request,key,rkey):
	reson=request.POST["Reason"]
	mydata=SignUp.objects.get(id=key)
	data=SignUp.objects.get(enroll=rkey)
	if mydata.YOP < data.YOP:
		role = f"({data.id}) Junior Passing in {data.YOP}"
	elif mydata.YOP > data.YOP:
		role = f"({data.id}) Senior Passing in {data.YOP}"
	else:
		role = f"({data.id}) Your Batchmate of passing year {data.YOP}"
	data=Blocks(user=key,blocked=rkey,role=role,Reason=reson)
	data.save()
	return redirect('Globalchat', key=key)


def unblock(request, key, uid):
    mysid = SignUp.objects.get(id=key)
    entry = Blocks.objects.get(id=uid)
    entry.delete()
    return redirect('Profile',key=key )