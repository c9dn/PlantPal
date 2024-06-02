from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from core_func.models import Community, Coordinate, Plant
from authentication.models import User
from datetime import date, timedelta, datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

# Create your views here.

class LeaderboardAPI(APIView):
    def get(self, request):
        curr_user = request.data["curr_user_email"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)

        community = curr_user.community_name

        communities_and_count = dict()

        start_date = date.today() - timedelta(days=7)

        # Define end date as start date plus 6 days
        end_date = start_date + timedelta(days=7)

        plants_in_last_week = Plant.objects.filter(date_added__gte=start_date, date_added__lte=end_date, is_a_plant=1)
        for i in plants_in_last_week:
            if(i.community.comm_name in communities_and_count):
                communities_and_count[i.community.comm_name] += 1
            else:
                communities_and_count[i.community.comm_name] = 1
        
        sorted_dict = dict(sorted(communities_and_count.items(), key=lambda item: item[1]))

        res = dict(reversed(list(sorted_dict.items())))

        first_10_dict = dict(list(res.items())[:10])

        """
        f_index = list(res.keys()).index(community)

        if f_index > 0:
            before_f = res[list(res.keys())[f_index - 1]]  # Key before "f" (if it exists)
        else:
            before_f = None

        if f_index < len(res) - 1:
            after_f = res[list(res.keys())[f_index + 1]]  # Key after "f" (if it exists)
        else:
            after_f = None
        """

        return Response({"message": "Success!", "leaderboard": first_10_dict}, status=200)

