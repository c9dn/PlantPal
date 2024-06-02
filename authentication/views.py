from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from core_func.models import Community
from .helper import gen_auth_code, send_msg, validate_email, split_email
import datetime
import pytz

# Create your views here.

class AssociateUser_API(APIView):
    def post(self, request):
        curr_user_email = request.data["email"]
        community_name = request.data["community"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user_email)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)
        time_delta = datetime.timedelta(hours=2)
        timezone = pytz.timezone('America/New_York')
        aware_datetime = timezone.localize(curr_user.authenticated_datetime)
        if(aware_datetime < datetime.datetime.now() - time_delta):
            curr_user.is_authenticated = 0
            curr_user.save()
            return Response({"message": "The user's authentication status has been removed. Please reauthenticate."}, 200)
        
        #Check if community exists
        community = Community.objects.get(comm_name=community_name)
        
        curr_user.community_name = community.comm_name

        curr_user.save()
        return Response({"message": "Successfully associated user with community."}, 200)

class IsAuth_API(APIView):
    def get(self, request):
        curr_user_email = request.data["email_add"]

        #Check if user exists
        user_check = User.objects.get(email=curr_user_email)
        
        return Response({"message": "User found", "response": user_check.is_authenticated, "comm": user_check.community_name}, status=200)

class EmailAuth_API(APIView):
    def post(self, request):
        try:
            curr_user_email = request.data["email_add"]

            if(validate_email(curr_user_email) == False):
                return Response({"message": "Invalid Email"}, status=200)

            #Check if user exists
            users = User.objects.filter(email=curr_user_email)
            
            user_check = None
            if(len(users) == 1):
                user_check = users[0]
            if(user_check):
                if user_check.is_banned:
                    return Response({"message": "User has been banned"}, status=200)
                """
                if(user_check.is_authenticated):
                    time_delta = datetime.timedelta(hours=2)
                    timezone = pytz.timezone('America/New_York').localize(datetime.datetime.now())
                    aware_datetime = timezone.localize(user_check.authenticated_datetime)
                    #aware_datetime = user_check.authenticated_datetime.replace(tzinfo=pytz.utc).astimezone(timezone)

                    #aware_datetime = timezone.localize(user_check.authenticated_datetime)
                    if(user_check.authenticated_datetime < datetime.datetime.now() - time_delta):
                        print("HH")
                        auth_code = gen_auth_code()
                        user_check.curr_auth_code = auth_code
                        user_check.requested_auth = 1
                        user_check.is_authenticated = 0
                        user_check.save()
                        email_core = user_check.email_core
                        url = "http://127.0.0.1:8000/hack_bronx_api/v0/authentication/authenticate/{email_core}/{verif_code}/".format(email_core=email_core, verif_code=auth_code)
                        send_msg(curr_user_email, url)
                        return Response({"message": "The user's authentication status has been removed. Please reauthenticate.", "email": curr_user_email, "verif_code": auth_code}, 200)
                    return Response({"message": "User found", "response": user_check.is_authenticated}, status=200)
                """
                if(user_check.requested_auth):
                    auth_code = user_check.curr_auth_code
                    email_core = user_check.email_core
                    url = "http://127.0.0.1:8000/hack_bronx_api/v0/authentication/authenticate/{email_core}/{verif_code}/".format(email_core=email_core, verif_code=auth_code)
                    send_msg(curr_user_email, url)
                    return Response({"message": "Authenticating", "email": curr_user_email, "verif_code": auth_code}, status=200)
                else:
                    auth_code = gen_auth_code()
                    user_check.curr_auth_code = auth_code
                    user_check.requested_auth = 1
                    user_check.is_authenticated = 0
                    user_check.save()
                    email_core = user_check.email_core
                    url = "http://127.0.0.1/hack_bronx_api/v0/authentication/authenticate/{email_core}/{verif_code}/".format(phone_number=email_core, verif_code=auth_code)

                    #Send Msg
                    send_msg(curr_user_email, url)

                    return Response({"message": "Authenticating", "email": curr_user_email, "verif_code": auth_code}, status=200)

            #Add new user
            auth_code = gen_auth_code()

            email_split = split_email(curr_user_email)

            new_user = User(email=curr_user_email, email_core=email_split[0], email_provider=email_split[1], is_banned=0, is_authenticated=0, curr_auth_code=auth_code, requested_auth=1)
            new_user.save()

            url = "http://127.0.0.1:8000/hack_bronx_api/v0/authentication/authenticate/{email_core}/{verif_code}/".format(email_core=email_split[0], verif_code=auth_code)

            #Send Msg
            send_msg(curr_user_email, url)

            return Response({"message": "Authenticating", "email": curr_user_email, "verif_code": auth_code}, status=200)
        except Exception as e:
            print("Error: ", e)
            return Response({"message": "Internal Server Error"}, status=500)

class AuthenticateUser_API(APIView):
    def get(self, request, email_core, verification_code):
        #print(f"Email Core: {email_core}, Verification Code: {verification_code}")
        #Check if user exists
        users = User.objects.filter(email_core=email_core)

        if(len(users) == 0):
            return Response({"message": "No User with this email. Please try again!"}, status=200)
        user_check = users[0]

        if(user_check.is_authenticated == 1):
            return Response({"message": "User Authenticated", "response": user_check.is_authenticated}, status=200)
        else:
            if(user_check.requested_auth == 0):
                return Response({"message": "User has not requested authentication. Please try again!"}, status=200)
            if(user_check.curr_auth_code != verification_code):
                return Response({"message": "This is the wrong URL."}, status=200)
            
            user_check.requested_auth = 0
            user_check.is_authenticated = 1
            user_check.authenticated_datetime = datetime.datetime.now()
            user_check.save()
            return Response({"message": "User successfully authenticated!"}, status=200)