from django.shortcuts import render
from adrf.decorators import api_view
import json
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .models import UserModel
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from media.models import MediaModel
from django.core.paginator import Paginator


def registerUser(user_data):
    try:
        user = UserModel.objects.get(username=user_data['username'])
        print('User already exists')
    except UserModel.DoesNotExist:
        user = UserModel.objects.create(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        user.save()
        return user

def handleImg(img, user):
    imgins = MediaModel.objects.create(pic=img)
    user.profile_pic = imgins
    user.save()

@api_view(['POST'])
async def register(request):
    obj = request.POST
    img = request.FILES.get('profilepic')
    # user_details = await sync_to_async(json.loads)(obj)
    # profile_pic = user_details.pop('profile_pic', None)
    user = await sync_to_async(registerUser)(obj)
    if img: 
        await sync_to_async(handleImg)(img, user)
    res = Response({
        'success': 'true'
    })
    return res

def fetch_users(page):
    users = UserModel.objects.prefetch_related('profile_pic').values('id', 'username', 'first_name', 'last_name', 'email', 'profile_pic__pic').exclude(is_superuser=True)
    paginator = Paginator(users, 10)
    res = paginator.get_page(page)
    has_next = res.has_next()
    for user in res:
        if user['profile_pic__pic']:
            user['profile_pic__pic'] = user['profile_pic__pic']
    obj = {
        "data": list(res), 
        'has_next': res.has_next()
    }
    return obj

@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def get_users(request, page):
    try:
        obj = await sync_to_async(fetch_users)(page)
        res = {
            "success": True, 
            "message": "users fetched successfully", 
            "data": obj['data'], 
            "has_next": obj['has_next']
        }
        return Response(res)
    except Exception as e:
        return Response({
            "success": False, 
            "message": "something went wrong", 
            "error": str(e)
        })
    
def fetch_user(username):
    try:
        user = UserModel.objects.get(username=username)
        return({
            'success': True, 
            'message': "User fetched successfully", 
            'user': user
        })
    except Exception as e:
        return({
            'success': False, 
            'message': "something went wrong", 
            'error': e
        })

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def getUser(request, username):
    if username is None:
        return Response({
            'success': False, 
            'msg': 'username is needed'
        })
    else:
        return await sync_to_async(fetch_user)(username)
    
def getChannelNameHelper(username):
    try:
        cn = UserModel.objects.values('channel_name').get(username=username)
        obj = {
            'success': True, 
            "cn": cn
        }
        return obj
    except Exception as e:
        return {
            'success': False, 
            'error': str(e)
        }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def getChannelName(request, username):
    if username is not None:
        try:
            res = await sync_to_async(getChannelNameHelper)(username)
            return Response(res)
        except Exception as e:
            return Response({
                'success': False,
                'message': "error in fetching user's channel name" ,
                'error': str(e)
            })

    else: 
        return Response({
            'success': False, 
            "message": "username should not be empty"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def filterUsers(request, pattern=""):
    if pattern is not None:
        try:
            users = await sync_to_async(list)(
                UserModel.objects.filter(username__icontains=pattern).prefetch_related('profile_pic').values('id', 'username', 'first_name', 'last_name', 'email', 'profile_pic__pic').exclude(is_superuser=True)[:10]
            )
            return Response({
                "success": True, 
                "users": users
            })
        except Exception as e:
            print(str(e))
            return Response({
                "success": False, 
                'error': str(e)
            })
    else:
        print('pattern not found')
        res = {
            "success": False, 
            "msg": "pattern needed!"
        }
        return Response(res)
    

def fetch_user(username): 
    return UserModel.objects.prefetch_related('profile_pic').values('id', 'username', 'first_name', 'last_name', 'email', 'profile_pic__pic').get(username=username)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
async def getUser(request, username):
    if username is not None:
        try:
            user = await sync_to_async(fetch_user)(username)
            res = {
                'success': True, 
                'message': "user found", 
                'user': user
            }
            return Response(res)
        except UserModel.DoesNotExist:
            res = {
                'success': False, 
                'message': "user not found!"
            }
            return Response(res)
    else:
        res = {
            'success': False, 
            "message": "username required!"
        }
        return Response(res)
    
def userUpdateHelper(request, username):
    try:
        user_data = request.POST
        pic = request.FILES.get('profile_pic')
        user = UserModel.objects.get(username=username)

        for key, value in user_data.items():
            if key != 'profile_pic':
                setattr(user, key, value)

        user.save()
        if user.profile_pic:
            user.profile_pic.delete()
        if pic: 
            newpic = MediaModel.objects.create(pic=pic)
            user.profile_pic = newpic
        user.save()
        return {
            "success": True,
        }
    except Exception as e:
        return {
            "success": False, 
            "msg": str(e)
        }
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
async def updateUserDetails(request, username):
    if username is not None:
        try:
            res = await sync_to_async(userUpdateHelper)(request=request, username=username)
            if res:
                return Response({
                    "success": True, 
                    "msg": "Profile updated successfully"
                })
            else:
                return Response(res)
        except UserModel.DoesNotExist:
            res = {
                "success": False,
                "msg": "user not found!"
            }
            return Response(res)
    else:
        res = {
                "success": False,
                "msg": "username is required!"
        }
        return Response(res)