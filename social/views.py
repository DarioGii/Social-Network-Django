from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import generics

from social.models import Member, Profile, Message
from social.serializers import MessageSerializer

appname = 'FacesMagazine'

class MessageCollection(generics.ListCreateAPIView):
        
    """ GET individual messages in the database. POST, 
    PUT AND DELETE a message.

    Implemented using generics in rest framework. Queryset gathers list
    of messages orderd by the time posted and they are then serialized by the MessageSerializer"""

    queryset = Message.objects.order_by('time')
    serializer_class = MessageSerializer

class MessageDetail(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):

    """ GET individual messages in the database. POST,
    PUT AND DELETE a message.

    Implemented using generics in rest framework. Queryset gathers list
    of messages orderd by the time posted and they are then serialized by the MessageSerializer"""

    queryset = Message.objects.order_by('time')
    serializer_class = MessageSerializer

def index(request):
    return render(request, 'social/index.html', {
        'appname': appname
        })

def messages(request):

    """ Retrieves all messages related to the current user, 
    whether private or public stored in a Message object
    and sends them to the messages.html template"""

    if 'username' in request.session:
        if request.method == 'POST':
            username = request.session['username']
            member_obj = Member.objects.get(pk=username)

            try:
                recipient = Member.objects.get(pk=request.POST.get('recip', None))
                if 'message' in request.POST:
                    message = request.POST['message']
                    if 'message_type' in request.POST:
                        private = request.POST['message_type'] == '1'
                        message = Message(author=member_obj, recip=recipient, private=private, message=message)
                        message.save()
                    else: #Redirect back to the current page with accompanying error message
                        members = Member.objects.all()
                        messages = Message.objects.filter(author=username, private=True) | Message.objects.filter(recip=username, private=True) | Message.objects.filter(recip=username, private=False) | Message.objects.filter(author=username, private=False).order_by('time')
                        return render(request, 'social/messages.html', {
                            'appname': appname,
                            'username': username,
                            'loggedin': True,
                            'chat_messages': messages,
                            'members': members,
                            'error': "Must select \"Public\" or \"Private\""
                        })
                else: #Redirect back to the current page with accompanying error message
                    members = Member.objects.all()
                    messages = Message.objects.filter(author=username, private=True) | Message.objects.filter(recip=username, private=True) | Message.objects.filter(recip=username, private=False) | Message.objects.filter(author=username, private=False).order_by('time')
                    return render(request, 'social/messages.html', {
                            'appname': appname,
                            'username': username,
                            'loggedin': True,
                            'chat_messages': messages,
                            'members': members,
                            'error': "Cannot send empty message"
                        })
            except Member.DoesNotExist:
                members = Member.objects.all()
                messages = Message.objects.filter(author=username, private=True) | Message.objects.filter(recip=username, private=True) | Message.objects.filter(recip=username, private=False) | Message.objects.filter(author=username, private=False).order_by('time')
                return render(request, 'social/messages.html', {
                    'appname': appname,
                    'username': username,
                    'loggedin': True,
                    'chat_messages': messages,
                    'members': members,
                    'error': "Recipient not specified"
                })
        username = request.session['username']
        members = Member.objects.all()
        messages = Message.objects.filter(author=username, private=True) | Message.objects.filter(recip=username, private=True) | Message.objects.filter(recip=username, private=False) | Message.objects.filter(author=username, private=False).order_by('time')
        return render(request, 'social/messages.html', {
            'appname': appname,
            'username': username,
            'loggedin': True,
            'members': members,
            'chat_messages': messages
            })
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to messages page!"
            })


def signup(request):
    return render(request, 'social/signup.html', {
        'appname': appname
        })

def register(request):
    u = request.POST['user']
    p = request.POST['pass']
    user = Member(username=u, password=p)
    user.save()
    return render(request, 'social/user-registered.html', {
        'appname': appname,
        'username' : u
        })

def login(request):

    """ Redirects back to the current page 
    with an accompanying error message if the user
    has entered an incorrect username or password"""

    if 'username' not in request.POST:
        return render(request, 'social/login.html', {
        'appname': appname
        })
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist: #Redirect back to the current page with accompanying error message
            return render(request, 'social/login.html', {
            'appname': appname,
            'error': "User does not exist"
            })
        if member.password == p:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else: #Redirect back to the current page with accompanying error message
            return render(request, 'social/login.html', {
            'appname': appname,
            'error': "Incorrect username or password"
            })

def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()
        return render(request, 'social/logout.html', {
            'appname': appname,
            'username': u
            })
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in"
            })

def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'social/member.html', {
            'appname': appname,
            'username': username,
            'greeting': greeting,
            'profile': text,
            'loggedin': True
            })
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to member page!"
            })

def friends(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'social/friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to friends page!"
            })

def members(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # follow new friend
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        # unfollow a friend
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        # view user profile
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            # list of all other members
            members = Member.objects.exclude(pk=username)
            # list of people I'm following
            following = member_obj.following.all()
            # list of people that are following me
            followers = Member.objects.filter(following__username=username)
            # render reponse
            return render(request, 'social/members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                )
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to members page!"
            })

def profile(request):
    if 'username' in request.session:
        u = request.session['username']
        member = Member.objects.get(pk=u)

        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'social/profile.html', {
            'appname': appname,
            'username': u,
            'text' : text,
            'loggedin': True}
            )
    else: #Redirect back to index.html with accompanying error message
        return render(request, 'social/index.html', {
            'appname': appname,
            'error': "You are not logged in, no access to profile page!"
            })

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']

        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        else:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")