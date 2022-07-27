from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Todo, User
from .serializer import Todoserializer, Todo_Update, SignupSerializer ,UserLoginSerializer,UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate



class SignupModelViewSet(viewsets.ModelViewSet):


    """
    API for SignUp user.

    #First User Create Account
    # Sample Data
        {
            "user_email": "test@gmail.com",
            "password":"test@123"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "Register Successfully",
            "payload": {
                "id": 2,
                "email": "test@gmail.com",
                "token": "43e3fd07636ca485b5afd45052d5ec8c5cc6e4c2"
            }
        }
    """


    # queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method_names = ["post"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data["user_email"]
        password = serializer.data["password"]
        user = User.objects.create(user_email=serializer.data["user_email"])
        user.set_password(password)
        user.save()
        # print("AAA")
        # print(user)
        # print(user.user_id)
        token = Token.objects.get(user_id=user.id)
        # print(token)
        if token :
            
            return Response(
                {
                    "success": True,
                    "message": "Register Successfully",
                    "payload": {"email": user_email, "Token": token.key},
                },
                status=status.HTTP_200_CREATED,
            )
        else:

            return Response(
            {
                "success": False,
                "message": "You Enter Email Is Exist.Plese Enter Different Email To Signup",
                "payload": {"email": user_email},
            },
            status=status.HTTP_404_NOT_FOUND,
            )

class LoginModelViewSet(viewsets.ModelViewSet):

    """
    API for Login user.

    # Sample Data
            {
                "email": "test@gmail.com",

                "password":"test@123"
            }
    # Success Sample Response
            {
                "success": true,
                "message": "You login successfully",
                "payload": {
                    "user_email": "test@gmail.com",
                    "password": "pbkdf2_sha256$320000$4bFyAVqmp904nOOID3UXjE$wpfTZ9681RRl0lnu2WUZrmGm4bx3zxldJd4qy2QrfBY=",
                    "token": "de2876005a81314feb2a273bb4b815ea6cc2061b"
            }
            }

        """

    serializer_class = UserLoginSerializer
    http_method_names = ['post']

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["user_email"]
        password = serializer.validated_data["password"]
        msg = False

        if email and password:
            user = authenticate(user_email=email, password=password)
            if user:
                if not user.is_active:
                    msg = ("User account is disabled.")

            else:
                msg = ("Unable to log in with provided credentials.")

        else:
            msg = ('Must include "email" and "password".')

        if not msg:
            user_serializer = UserLoginSerializer(user)
            return Response(
                {
                    "success": True,
                    "message": "You login successfully",
                    "payload": user_serializer.data,

                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": msg, "payload": []},
                status=status.HTTP_200_OK,
            )

class UserProfile(viewsets.ModelViewSet):

    """
    API for Update User Profile.

    
    # Sample Data
        {
        "first_name": "test",
        "last_name": "test1",
        "image": null,
        "user_phone": "1234567890",
        "address": "earth",
        "city": "earth",
        "state": "earth",
        "Pin_Code": 987866
        }
    # Success Sample Response
        {
        "success": true,
        "message": "User Profile Update Successfully",
        "payload": [
        {
        "id": 1,
        "first_name": "test",
        "last_name": "test1",
        "image": null,
        "user_phone": "1234567890",
        "address": "earth",
        "city": "earth",
        "state": "earth",
        "Pin_Code": 987866
        }
        ]
        }
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["patch","get"]


#  def get_queryset(self):
#     return User.objects.filter(id=self.request.user.id)

    def list(self, request):
        queryset = User.objects.filter(id=self.request.user.id)
        serializer = UserSerializer(queryset, many=True)
        return Response(
                {
                    "success": True,
                    "message": "User Get Successfully",
                    "payload": serializer.data,

                },
                status=status.HTTP_200_OK,
            )

    
    def partial_update(self, request,pk=None):
        # print("AAAAA")
        user=User.objects.get(id=self.request.user.id)
        # print(user)
        # print(pk)
        # print("nikunj")
        if user:

            serializer = UserSerializer(user, data=self.request.data, partial=True)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status': True,
                'message': 'sucess update',
                'data': serializer.data
                },
                    status=status.HTTP_200_OK,
                )
            return Response(
            {
            'status': False,
            'message': 'invaild data',
            'data': serializer.errors
            },status=status.HTTP_404_NOT_FOUND,
            )
        else:

            return Response({
                    'status': False,
                    'message': 'plese enter valid id',
                    'data': {}
                },status=status.HTTP_404_NOT_FOUND,)   


class Todo_Update_Retrieve_Destory(viewsets.ModelViewSet):
    """
     
    API for Create, Get ,Update , Delete  Todo.

    # Sample Data For Create Todo
        {
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at ",
        "is_done": false,
        "favourite": true
        }

    

    # Success Sample Response
        {
        "success": true,
        "message": "User Todo Create Successfully",
        "payload": [      
        {
        "id": 1,
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
        "create_at": "2022-07-22T08:35:44.047951Z",
        "is_done": false,
        "favourite": true
        }]
    
    # Sample Data For Delete Todo
       
        Enter id in Box:1

    # Success Sample Response
        {
        'status': True,
        'message': 'Sucessfully Delete',
        },     
        Delete Todo Itself 
    
    # Sample Data For Update Todo
        {
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at ",
        "is_done": false,
        "favourite": true
        }

        Enter id in Box:1

    # Success Sample Response
        {
        "success": true,
        "message": "User Todo Update Successfully",
        "payload": [      
        {
        "id": 1,
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
        "create_at": "2022-07-22T08:35:44.047951Z",
        "is_done": false,
        "favourite": true
        }]
    
    # Sample data For Get Todo
        click Execute 

    # Success Sample Response
        [
        "success": True,
        "message": "Todo Create Sucessfully",
        "payload":
        {
        "id": 1,
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
        "create_at": "2022-07-22T08:35:44.047951Z",
        "is_done": false,
        "favourite": false
        }
        ]
    """
    
  
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Todoserializer
    queryset = Todo.objects.all()
    http_method_names = ["patch", "delete","post","get"]



    def list(self, request):
        queryset = Todo.objects.filter(user=self.request.user)
        serializer = Todoserializer(queryset, many=True)
        return Response(
                {
                    "success": True,
                    "message": "User Todo Get Successfully",
                    "payload": serializer.data,

                },
                status=status.HTTP_200_OK,
            )
    def create(self,request): 
            serializer=Todoserializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(
                        {
                        "success": True,
                        "message": "Todo Create Sucessfully",
                        "payload": serializer.data,

                        },
                        status=status.HTTP_200_OK,
                        )
                return Response(
                        {
                        'status': False,
                        'message': 'invaild data',
                        'data': serializer.errors,
                        },status=status.HTTP_404_NOT_FOUND,
                        )


    def partial_update(self, request,pk=None):
        user=Todo.objects.filter(id=pk)
        if user:

            serializer = Todoserializer(user, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status': True,
                'message': 'sucess update',
                'data': serializer.data
                },
                    status=status.HTTP_200_OK,
                )
                return Response(
                {
                'status': False,
                'message': 'invaild data',
                'data': serializer.errors
                },status=status.HTTP_404_NOT_FOUND,
                )
        else:

            return Response({
                    'status': False,
                    'message': 'plese enter valid id',
                    'data': {}
                },status=status.HTTP_404_NOT_FOUND,)
        
        

    def destroy(self, request,pk=None):
        user=Todo.objects.filter(id=pk)
        if user:
            user.delete()
            print("ok")
            return Response({
                'status': True,
                'message': 'Sucessfully Delete',
                },
                    status=status.HTTP_200_OK,
                )
        
        else:

            return Response({
                'status': False,
                'message': 'plese enter valid id',
                'data': {}
                },status=status.HTTP_404_NOT_FOUND,)
        
        
       



class TodoFavModelViewSet(viewsets.ModelViewSet):

    """
    API for Show User Favourite Todo.

    #Sample data
        Click Execute To Show Favourite Todo

    # Success Sample Response
        [
        {
        "id": 1,
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
        "create_at": "2022-07-22T08:35:44.047951Z",
        "is_done": false,
        "favourite": True
        }
        ]

    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = Todo_Update
    http_method_names = ["get","patch"]
    def list(self, request):
        queryset = Todo.objects.filter(user=self.request.user,favourite=True)
        serializer = Todoserializer(queryset, many=True)
        return Response(
                {
                    "success": True,
                    "message": "User Todo Favourite Display Successfully",
                    "payload": serializer.data,

                },
                status=status.HTTP_200_OK, 
            )
    def partial_update(self, request,pk=None):
        user=Todo.objects.filter(id=pk).update(favourite=True)
        if user:
            return Response({
                'status': True,
                'message': 'sucess ',
                },
                    status=status.HTTP_200_OK,
                )
            
        else:

            return Response({
                    'status': False,
                    'message': 'plese enter valid id',
                    'data': {}
                },status=status.HTTP_404_NOT_FOUND,)

class TodoisdoneModelViewSet(viewsets.ModelViewSet):
    """
    API for Show User Is_Done Todo.

    #Sample data
        Click Execute To Show Is_Done Todo

    # Success Sample Response
        [
        {
        "id": 1,
        "todo_title": "Cricket",
        "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
        "create_at": "2022-07-22T08:35:44.047951Z",
        "is_done": True,
        "favourite": True
        }
        ]

    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = Todoserializer
    http_method_names = ["get","patch"]
    def list(self, request):
        queryset = Todo.objects.filter(user=self.request.user,is_done=True)
        serializer = Todoserializer(queryset, many=True)
        return Response(
                {
                    "success": True,
                    "message": "User Todo Complated Display Successfully",
                    "payload": serializer.data,

                },
                status=status.HTTP_200_OK, 
            )
    def partial_update(self, request,pk=None):
        user=Todo.objects.filter(id=pk).update(is_done=True)
        if user:
            return Response({
                'status': True,
                'message': 'sucess',
                },
                    status=status.HTTP_200_OK,
                )
            
        else:

            return Response({
                    'status': False,
                    'message': 'plese enter valid id',
                    'data': {}
                },status=status.HTTP_404_NOT_FOUND,)



















# class User_isdone_Todo(generics.UpdateAPIView):
#     """
#     API for User Set isdone_Todo.

#     # Sample Data
#         Click Execute To Is_Done Todo
#     # Success Sample Response
#         {
#         "id": 16
#         }

#     """
#     serializer_class = Todo_Update
#     permission_classes = [permissions.IsAuthenticated]
#     http_method_names = ["patch"]

#     def get_queryset(self):
#         user = self.request.user
#         return Todo.objects.filter(user=user)

#     def perform_update(self, serializer):
#         serializer.instance.is_done = not (serializer.instance.is_done)
#         serializer.save()


# class User_fav_Todo(generics.UpdateAPIView):
#     """
#     API for User Set Favourite Todo.

#     # Sample Data
#         Click Execute To Fav_Todo
#     # Success Sample Response
#         {
#         "id": 16
#         }

#     """
#     serializer_class = Todo_Update
#     permission_classes = [permissions.IsAuthenticated]
#     http_method_names = ["patch"]

#     if permission_classes:
#         def get_queryset(self):
#             user = self.request.user
#             return Todo.objects.filter(user=user)

#         def perform_update(self, serializer):
#             serializer.instance.favourite = not (serializer.instance.favourite)
#             serializer.save()






# class TodoModelViewSet(viewsets.ModelViewSet):

#     """
#     API for Show User All Todo .

#     #Sample data
#         click Execute 

#     # Success Sample Response
#         [
#         {
#         "id": 1,
#         "todo_title": "Cricket",
#         "todo_description": "Cricket is a bat-and-ball game played between two teams of eleven players each on a field at",
#         "create_at": "2022-07-22T08:35:44.047951Z",
#         "is_done": false,
#         "favourite": false
#         }
#         ]
#     """
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Todo.objects.all()
#     serializer_class = Todoserializer
#     http_method_names = ["get"]
#     def list(self, request):
#         queryset = Todo.objects.filter(user=self.request.user)
#         # print(queryset)
#         serializer = Todoserializer(queryset, many=True)
#         # return Response(serializer.data)
#         return Response(
#                 {
#                     "success": True,
#                     "message": "User Todo Display Successfully",
#                     "payload": serializer.data,

#                 },
#                 status=status.HTTP_200_OK, #HTTP_202_ACCEPTED
#             )
