from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Movies,Rating

from .serializers import MoviesListRetrieveSerializer , MoviesCreateUpdateSerializer

from .serializers import RatingSerializer

import json

from django.shortcuts import get_object_or_404

from rest_framework import authentication

from rest_framework.permissions import AllowAny

from authentication.permissions import IsAdmin,IsUser

from rest_framework_simplejwt import authentication


from django.db.models import Avg 



# Create your views here.


class MoviesListCreateView(APIView):

    http_method_names=['get','post']
    
    authentication_classes = [authentication.JWTAuthentication]

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # this serializer retrieve and list view

    get_serializer_class = MoviesListRetrieveSerializer

    # this serializer for create/post view or update view

    post_serializer_class = MoviesCreateUpdateSerializer


    def get_permissions(self):

        if self.request.method == 'GET':

            return [AllowAny()]
        
        if self.request.method == 'POST':

            return [IsAdmin()]
        
        return super().get_permissions()

    def get(self,request,*args,**kwargs):

        movies = Movies.objects.filter(active_status=True)

        movie_serializer = self.get_serializer_class(movies,many=True)

        return Response(data= movie_serializer.data ,status=200)


    def post(self, request , *args , **kwargs):

        # print(request.data.get('cast'))

        # print(request.data)

        movie_serializer = self.post_serializer_class(data= request.data)

        if movie_serializer.is_valid():

            movie = movie_serializer.save()

            # thi

            cast_ids = json.loads(request.data.get('cast',[]))

            movie.cast.set(cast_ids)

            return Response(data={'msg': 'Movie created successfully!!'}, status=200)
        
        return Response (data=movie_serializer.errors,status=400)
    
class MovieRetrieveUpdateDestroyView(APIView):

    get_serializer_class = MoviesListRetrieveSerializer

    put_serializer_class = MoviesCreateUpdateSerializer

    def get(self, request, *args ,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        serializer = self.get_serializer_class(movie)

        return Response(data=serializer.data , status=200)
    
    def put(self,request, *args ,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        serializer = self.put_serializer_class(instance=movie,data= request.data,partial =True)

        if serializer.is_valid():

            movie_obj = serializer.save()

            cast = request.data.get('cast')

            if cast:

                cast_ids = json.loads(cast,[])

                movie_obj.cast.set(cast_ids)

            return Response(data={'msg' : 'Movie updated successfully'},status=200)
        
        return Response(data= serializer.errors,status=400)
    
    def delete(self, request, *args , **kwargs):


        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        movie.active_status=False

        movie.save()

        return Response(data= {'msg' : 'movie deleted succesfully'},status=200)
    
class AddRatingview(APIView):

    http_method_names = ['post'] 

    authentication_classes= [authentication.JWTAuthentication]

    permission_classes =[IsUser]

    # serializer_class = RatingSerializer

    def post(self, request , *args , **kwargs):

        user = request.user

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        rating = request.data.get('rating')

        Rating.objects.create(user = user,movie=movie,rating=rating)

        return Response(data={'msg' : 'rating added successfully' })


class Top20MoviesListView(APIView):

    http_method_names = ['get']

    authentication_classes = [authentication.JWTAuthentication]

    permission_classes = [AllowAny]

    serializer_class = MoviesListRetrieveSerializer

    def get(self, request , *args , **kwargs ):

        top_20_movies = Movies.objects.annotate(avg_rating=Avg('rating__rating')).filter(avg_rating__isnull = False)  
                                                            # if we use .exclude() then .exclude(avg_rating__isnull = True)

        serializer = self.serializer_class(top_20_movies,many=True)

        return Response(data= serializer.data, status=200)