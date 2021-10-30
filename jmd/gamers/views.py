from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime
from gamers.models import Contact,Game,Question,Matchpt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse
import math, random ,json,requests
ggid=''
ggname=''
name0='ram'
ri={}
# Create your views here.
def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")


def about(request):
    return render (request,'about.html')
    #return HttpResponse("This is about page")
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, 'Your feedback has been sent.')
    return render (request,'contact.html')
    #return HttpResponse("This is contact page")
def services(request):
    return render (request,'services.html')
    #return HttpResponse("This is services page")

def pubg(request):
    return render (request,'pubg.html')
def home(request):
    
    request.session.clear()
    r={}
    r['games']=Game.get_all_games()
    print(r)
    gid=request.GET.get('game')
    print(gid)
    global ggid
    ggid=gid
    
    #print(gamename)
    if gid:
      gamename=Game.get_game(gid)
      #print(gamename('waiting_list'))
      print(gamename[0])
      global ggname
      ggname=gamename[0]
      context={
          'gg':gamename[0]
      }

      return render(request,'findmatch.html',context)
    else:
      return render(request,'home.html',r)

def matchpt(request):
    if request.method=='GET':
         print('this is get')
         if request.session.get('acc') is not None:
          print(request.session.get('wl'))
          if request.session.get('wl') == 0:
           messages.info(request, 'We will inform you when a match is found.')
           return render (request,'findmatch.html')
          else:
           print(request.session.get('data'))
           context1={
             'dictionary':request.session.get('data')
            }
           return render(request,'matches.html',context1)
         else:
            return HttpResponse('404')
        
         
    if request.method=="POST":
        print('this is post')
        name=request.POST.get('name')
        gameid=request.POST.get('gameid')
        email=request.POST.get('email')
        #opt11=request.POST.get('opt11')
        global name0
        name0=name
        print(name)
        option=int(request.POST.get('opt1'))+int(request.POST.get('opt2'))+int(request.POST.get('opt3'))*(2**8)+int(request.POST.get('opt4'))*(2**9)+int(request.POST.get('opt5'))*(2**10)+int(request.POST.get('opt6'))*(2**11)+int(request.POST.get('opt7'))*(2**12)+int(request.POST.get('opt8'))*(2**13)+int(request.POST.get('opt9'))*(2**14)+int(request.POST.get('opt10'))*(2**15)+int(request.POST.get('opt11'))*(2**16)
        matchpt=Matchpt(name=name,gameid=gameid,email=email,option=option,game=ggname)
        

        
        waiting=Game.get_wl((ggid))
        request.session['wl']=waiting
        print(request.session.get('wl'),'wl')

        if request.session.get('acc') is not None:
         print(request.session.get('data'),'hi')
         if request.session.get('wl') == 1:
          messages.info(request, 'We will inform you when a match is found.')
          return render (request,'findmatch.html')
         else:
          context1={
             'dictionary':request.session.get('data')
          }
          return render(request,'matches.html',context1) 
        elif Matchpt.return_acc(name) !=False:
          messages.warning(request, 'Your form already exist.')
          return render (request,'findmatch.html')
        elif waiting == 0:
           obj=Game.objects.get(id=ggid)
           obj.waiting_list=1
           obj.save()
           request.session['acc']=name
           #session
           matchpt.save()
           messages.info(request, 'We will inform you when a match is found.')
           return render (request,'findmatch.html')
        else:
            request.session['acc']=name
            
            global ri
            ri={}
            n=Matchpt.objects.filter(game=ggid).count()
            print(n)
            b=Matchpt.objects.filter(game=ggid)[n-1].option
            #ri={'users':[],'pers':[]}
            #ri['users']=Matchpt.objects.filter(game=ggid)
            print(ri)
            arr=[]
            for i in range(0,n):
                a=Matchpt.objects.filter(game=ggid)[i].option
                a=a&b
                r=0
                while(a>0):
                    a=(a&(a-1))
                    r=r+1
                arr.append(r+i/1000)
            #print(Matchpt.objects.all()[x])
            arr.sort(reverse = True)
            ar=['A']*n
            br=[0]*n
            for i in range(0,n):
                #print(round(arr[i]*1000)%1000)
                ar[i]=Matchpt.objects.filter(game=ggid)[round(arr[i]*1000)%1000].name
                br[i]='%.2f'%((int(arr[i])/11.0)*100)
                ri.update({ar[i]:br[i]})
                #cr[i]=Matchpt.objects.filter(game=ggid)[round(arr[i]*1000)%1000].id
            for i in range(0,n):
                print(ar[i])
                print(br[i])
                print(' ')
                #ri['users']=ar
                #ri['pers']=br
            matchpt.save()
            print(ri)
            duplicate_ri=ri
            obj=Game.objects.get(id=ggid)
            obj.waiting_list=obj.waiting_list+1
            obj.save()
            context={
                'dictionary':duplicate_ri
            }
            request.session['data']=duplicate_ri
            
            #return render(request,'matches.html',ri)
            return render(request,'matches.html',context) 

    return render (request,'findmatch.html')

def addme(request):
    if request.method=="POST":
      name1=request.POST.get('addme')
      if request.session.get('sent_to')!=name1:
        email=Matchpt.objects.filter(name=name1)[0].email
        otp=str(Matchpt.objects.filter(name=name0)[0].id)
        print(name1)
        print(email)
        context={
            'dictionary':ri,
            'var':name1
        }
        print(ri)
        send_mail(
            'Find Gamers:New friend request',
            'hi ' +name1 +'   '+name0 +' sent you a friend request with '+ri[name1]+'% match. Connection otp is '+otp,
            'findgamersrequest@gmail.com',
            [email],
            #fail_silently=False,
        )
        del ri[name1]
        request.session['data']=ri
        request.session['sent_to']=name1
        messages.success(request, 'Friend request sent to ')
        return render(request,'matches.html',context)
      else:
          context1={
              'dictionary':request.session.get('data')
          }
          return render(request,'matches.html',context1)


def acceptr(request):
    if request.method=="POST":
        myname=request.POST.get('myname')
        hisname=request.POST.get('hisname')
        otp=int(request.POST.get('otp'))
        if Matchpt.objects.filter(name=myname).exists() and Matchpt.objects.filter(name=hisname).exists():
            if otp==Matchpt.objects.filter(name=hisname)[0].id:
                hisid=Matchpt.objects.filter(name=hisname)[0].gameid
                myid=Matchpt.objects.filter(name=myname)[0].gameid
                email=Matchpt.objects.filter(name=hisname)[0].email
                send_mail(
                    'Find Gamers:Friend request accepted',
                    myname +' accepted your friend request.His Game ID is '+myid,
                    'findgamersrequest@gmail.com',
                    [email],
                    #fail_silently=False,
                )
                context={
                    'name':hisname,
                    'gameid':hisid
                }
                ggid=Matchpt.objects.filter(name=myname)[0].game.id
                obj=Game.objects.get(id=ggid)
                obj.waiting_list=obj.waiting_list-2
                obj.save()
                entry= Matchpt.objects.get(name=hisname)
                entry.delete()
                entry= Matchpt.objects.get(name=myname)
                entry.delete()
                messages.success(request,' Game ID is ')
                return render(request,'acceptr.html',context)
            else:
                messages.error(request, 'Invalid OTP')
                return render(request,'acceptr.html')
        else:
            messages.error(request, 'Invalid name')
            return render(request,'acceptr.html')
    return render(request,'acceptr.html')
       


def search(request):
    query=request.GET['query']
    if len(query)>78:
        games=Game.objects.none()
    else:
        games=Game.objects.filter(gname__icontains=query)
    if games.count() == 0:
        messages.warning(request,'No results found. Please try a different search.')
    par={'games':games , 'query':query}
    return render(request,'search.html',par)


def autosuggest(request):
    print(request.GET)
    query=request.GET.get('term')
    queryset=Game.objects.filter(gname__icontains=query)
    mylist=[]
    mylist += [x.gname for x in queryset]
    return JsonResponse(mylist,safe=False)


def deleteid(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        if Matchpt.objects.filter(name=name).exists():
            if email==Matchpt.objects.filter(name=name)[0].email:
                string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                otp = ""
                length = len(string) 
                for i in range(6) : 
                    otp += string[math.floor(random.random() * length)]
                request.session['OTP']=otp
                request.session['delname']=name
                print(request.session.get('OTP'))
                send_mail(
                    'Find Gamers:OTP to delete ID',
                    'Hi '+name+'your OTP to delete your ID is: '+otp,
                    'findgamersrequest@gmail.com',
                    [email],
                    #fail_silently=False,
                )
                return render(request,'delotp.html')
            else:
                messages.error(request, 'Invalid Name or Email')
                return render(request,'deleteid.html')
        else:
            messages.error(request, 'Invalid Name or Email')
            return render(request,'deleteid.html')
    return render(request,'deleteid.html')


def delotp(request):
    if request.method=="POST":
        otp=request.POST.get('otp')
        if request.session.get('OTP')==otp:
            name=request.session.get('delname')
            ggid=Matchpt.objects.filter(name=name)[0].game.id
            obj=Game.objects.get(id=ggid)
            obj.waiting_list=obj.waiting_list-1
            obj.save()
            entry= Matchpt.objects.get(name=name)
            entry.delete()
            messages.success(request,"Your ID has been deleted successfully!")
            return render(request,'deleteid.html')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request,'delotp.html')
    return render(request,'delotp.html')


def addgame(request):
    if request.method =='POST':
        gamename=str(request.POST.get('word'))
        zi=request.session.get('ngame')
        print(zi)
        if  gamename in zi:
            gi=request.session.get('gameimg')
            gameimage=gi[gamename]
            print(gameimage)
            addgame=Game(gname=gamename,image=gameimage)
            addgame.save()
            context0={'var1':gamename}
            messages.success(request," added successfully!")
            return render(request,'add_newgame.html',context0)
        else:
            messages.warning(request,"Please select from the list")
            return render(request,'add_newgame.html')
    else:
        return render(request,'add_newgame.html')

def gnameautosuggest(request):
    print(request.GET)
    gquery=request.GET.get('term')
    headers={
        'User-Agent':'Rishabh Sidana'
    }
    payload={'search':gquery}
    url="https://api.rawg.io/api/games"
    r=requests.get(url,headers=headers,params=payload)
    data=json.loads(r.text)
    li={}
    li['games']=[]
    for gam in data['results']:
        li['games'].append(gam['name'])
    ki={}
    for gam in data['results']:
        ki.update({gam['name']:gam['background_image']})
    request.session['gameimg']=ki
    mylist=[]
    mylist=li['games']
    #print(li)
    print(mylist)
    request.session['ngame'] = mylist

    #mylist += [x.games for x in zi]
    return JsonResponse(mylist,safe=False)