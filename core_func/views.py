from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Community, Coordinate, Plant
from authentication.models import User
from datetime import date, timedelta, datetime
from .serializers import PlantSerializer
from django.core.files.storage import FileSystemStorage
from .helper import is_plant, create_static_map, add_border_radius
from django.http import HttpResponse

# Create your models here.

class CommunityImageAPI(APIView):
    def get(self, request):
        curr_user = request.data["curr_user_email"]
        curr_long = request.data["long"]
        curr_lan = request.data["lat"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")

        output_path = "./temp/" + str(curr_user.email_core) + "_" + str(date_str) + "_" + str(time_str) + ".png"
    

        create_static_map(output_path=output_path, lat=float(curr_lan), lon=float(curr_long))
        add_border_radius(input_path=output_path, output_path=output_path)

        with open(output_path, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type='image/jpeg')

class PlantAPI(APIView):
    #GET: All the plants/coins in a community in the past week.
    def get(self, request):
        curr_user = request.data["curr_user_email"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)
        
        start_date = date.today() - timedelta(days=7)

        # Define end date as start date plus 6 days
        end_date = start_date + timedelta(days=7)

        plants_in_last_week = Plant.objects.filter(date_added__gte=start_date, date_added__lte=end_date, is_a_plant=1)
        num_of_coins = len(plants_in_last_week) * 3

        serialized_plants = PlantSerializer(plants_in_last_week, many=True)

        return Response({"message": "Success!", "plants": serialized_plants.data, "coins": num_of_coins}, 200)

    #POST: Add a plant
    def post(self, request):
        curr_user = request.data["curr_user_email"]
        coordinates = request.data["coordinates"]
        plant_img = request.FILES["image"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)
        
        #Check if coordinates are part of a community
        found_flag = 0

        j, k = eval(coordinates)
        all_communities = Community.objects.all()

        for i in all_communities:
            if((j >= i.x_min and j <= i.x_max) and (k >= i.y_min and k <= i.y_max)):
                if(curr_user.community_name == i.comm_name):
                    found_flag = 1
                    community = i
                    break
                else:
                    return Response({"message": "This plant was planted outside of your community."}, 200)
        
        if(found_flag == 0):
            return Response({"message": "This plant was planted outside of a community."}, 200)

        """plant_img_split = plant_img.name.split(".")
        plant_img_ext = plant_img_split[(len(plant_img_split) - 1)]"""
        comm_first = community.comm_name.split(" ")[0]


        new_img_name = str(curr_user.email_core) + "_" + str(comm_first) + "_" + str(date.today().strftime("%m-%d-%Y")) + "_" + str(plant_img.name)
        storage = FileSystemStorage()
        saved_path = storage.save(new_img_name, plant_img)

        plant_obj = Plant(plant_lat = k, plant_long = j, image=saved_path, image_name=plant_img.name, community=community, is_a_plant=0, user=curr_user)
        plant_obj.save()

        post_processing_dir = new_img_name

        data_point = is_plant(post_processing_dir)
        plant_obj.is_a_plant = data_point
        plant_obj.save()

        return Response({"message": "Success!"}, 200)

class CommunityAPI(APIView):
    #Check if coordinates are an existing community
    def get(self, request):
        #input data
        curr_user = request.data["curr_user_email"]
        coordinates = request.data["coordinates"]

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)

        print(coordinates)
        j, k = coordinates
        all_communities = Community.objects.all()

        for i in all_communities:
            if((j >= i.x_min and j <= i.x_max) and (k >= i.y_min and k <= i.y_max)):
                msg = "Looks like the mapped out coordinates interfere with another community: {comm}".format(comm=i.comm_name)
                return Response({"message": msg, "community": i.comm_name}, 200)
            
        return Response({"message": "This user is not in any community."}, 200)
    
    #Create a new community
    def post(self, request):
        #input data
        curr_user = request.data["curr_user_email"]
        coordinates = request.data["coordinates"]
        community_name = request.data["community_name"]

        #Pre Processing Coordinates
        if(type(coordinates) is not list):
            return Response({"message": "There was an error! Please input coordinates as a list."}, 200)
        if(len(coordinates) < 3):
            return Response({"message": "Not enough coordinates to process."}, 200)

        #Check if user is authenticated
        users = User.objects.filter(email=curr_user)
        if(len(users) == 0):
            return Response({"message": "This user doesn't exist. Please authenticate."}, 200)
        curr_user = users[0]
        if not curr_user.is_authenticated:
            return Response({"message": "This user isn't authenticated. Please authenticate."}, 200)
        

        #Check if coordinates interfere with another community
        all_communities = Community.objects.all()

        for i in all_communities:
            for j, k in coordinates:
                if((j >= i.x_min and j <= i.x_max) and (k >= i.y_min and k <= i.y_max)):
                    msg = "Looks like the mapped out coordinates interfere with another community: {comm}".format(comm=i.comm_name)
                    return Response({"message": msg}, 200)
        
        #Process given coordinates:
        x_min = 999999999999999
        x_max = -999999999999999
        y_min = 999999999999999
        y_max = -999999999999999
        for i, j in coordinates:
            if(i > x_max):
                x_max = i
            if(i < x_min):
                x_min = i
            if(j > y_max):
                y_max = j
            if(j < y_min):
                y_min = j

        if(x_max == -999999999999999 or x_min == -999999999999999 or y_max == -999999999999999 or y_min == -999999999999999):
            print(x_max, x_min, y_max, y_min)
            return Response({"message": "Something went wrong! Please try again later."}, 200)
        
        #Create community
        new_comm = Community(comm_name=community_name, num_of_coordinates=len(coordinates), x_max=x_max, x_min=x_min, y_max=y_max, y_min=y_min, added_by=curr_user, plants_life=0)
        new_comm.save()

        for i, j in coordinates:
            new_coordinate = Coordinate(latitude=j, longitude=i, community=new_comm)
            new_coordinate.save()

        curr_user.community = community_name
        curr_user.save()
        
        return Response({"message": "Success! Community added!"}, 200)
