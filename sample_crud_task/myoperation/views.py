from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from rest_framework import status
#from rest_framework.authentication import  BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
import psycopg2
from rest_framework_jwt.settings import api_settings


# Create your views here.

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]




@api_view(['POST'])
def register_user(request):
    if request.method == "POST":
        data=request.data
        username=data['username']
        password=data['password']
        email=data['email']
        role_id=data['role_id']
        isactive=True

        with connection.cursor() as cursor:
            cursor.execute('''
                    INSERT into 
                    myoperation_register(username,password,email,is_active,role_id) VALUES(%s,%s,%s,%s,%s)
            ''',(username,password,email,isactive,role_id))
            content={'message': "User is added successfully"}

            return Response(content,status=status.HTTP_201_CREATED)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# payload = jwt_payload_handler(user)
# token = jwt_encode_handler(payload)





@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_products_inventory(request):
    if request.method =='GET':
        username=request.user.username
        with connection.cursor() as cursor:
            cursor.execute(''' 
                                select username from 
                                myoperation_register 
                                where username=%s and (role_id=1 or role_id=2 )''',(username,))
            userdata=dictfetchall(cursor)
            if len(userdata)!=0:
                cursor.execute('''
                    select * from myoperation_productmodel
                    order by id asc
                    
                ''')
                product_data=dictfetchall(cursor)
                return  Response(product_data,status=status.HTTP_200_OK)
            else:
                content={'msg':"invalid User"}
                return  Response(content,status=status.HTTP_401_UNAUTHORIZED)




    elif request.method == 'POST':
        user=request.user
        print(user,'USer')
        role_id=1
        data=request.data
        title=data['title']
        description=data['description']
        inv_count=data['inventory_count']

        username=request.user.username
        print(username,'USSERNASM')

        with connection.cursor() as cursor:

            cursor.execute('''

            select username from myoperation_register where username=%s and role_id=1


            ''',(username,))
            user_data=dictfetchall(cursor)

            if len(user_data)!=0:
                cursor.execute('''
                Insert into myoperation_productmodel(title,description,inventory_count) VALUES (%s,%s,%s) Returning id
                ''',(title,description,inv_count))
                product_data=cursor.fetchone()
                product_id=product_data[0]

                cursor.execute('''
                Select * from myoperation_productmodel where id=%s

                ''',(product_id,))
                product_info=dictfetchall(cursor)

                return Response(product_info,status=status.HTTP_201_CREATED)
            else:
                content={'msg':"Invalid User"}
                return Response(content,status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login_gettoken(request):
    # if request.method=='GET':
    #     pass
    if request.method == 'POST':
        data=request.data
        username=data['username']
        password=data['password']

        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT id,username,role_id from myoperation_register where username=%s and password=%s
            
            ''',(username,password))

            user_data=dictfetchall(cursor)
            print(user_data,'USER DATA')
            if len(user_data)!=0:
                user=user_data[0]
                print(user,'YTYYYYY')
                payload = user
                token = jwt_encode_handler(payload)
                content={'msg':'user is logged in','token':token}
                return Response(content,status=status.HTTP_200_OK)
            else:
                content={'msg':'invalid username and password'}
                return Response(content,status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT','DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def product_update_delete(request,id):

    if request.method == 'PUT':
        username=request.user.username
        prd_id=id
        data=request.data
        title=data['title']
        description=data['description']
        inventory_count=data['inventory_count']
        with connection.cursor() as cursor:
            cursor.execute(''' 
                                select username from 
                                myoperation_register 
                                where username=%s and (role_id=1 or role_id=2 )''', (username,))
            userdata = dictfetchall(cursor)

            if len(userdata)!=0:
                cursor.execute('''
                
                Update myoperation_productmodel set (title,description,inventory_count)=(%s,%s,%s)
                Where id=%s
                
                
                ''',(title,description,inventory_count,prd_id))

                cursor.execute('''
                select * from myoperation_productmodel where id=%s
                
                ''',(prd_id,))

                update_data=dictfetchall(cursor)
                return Response(update_data,status=status.HTTP_201_CREATED)
            else:
                content = {'msg': "Invalid User"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)



    elif request.method == 'DELETE':
        prd_id=id
        username=request.user.username
        with connection.cursor() as cursor:
            cursor.execute('''

                        select username from myoperation_register where username=%s and role_id=1


                        ''', (username,))
            user_data = dictfetchall(cursor)

            if len(user_data)!=0:
                cursor.execute('''
                SELECT * from myoperation_productmodel where id=%s
                ''',(prd_id,))
                prd=dictfetchall(cursor)
                if len(prd)!=0:
                    cursor.execute('''
                    DELETE  from myoperation_productmodel where id=%s
                    ''',(prd_id,))
                    content={'msg':'ITem Deleted Successfully'}
                    return Response(content,status=status.HTTP_200_OK)
                else:
                    content={'msg':'Item not found'}
                    return Response(content,status=status.HTTP_404_NOT_FOUND)

            else:
                content = {'msg': "Invalid User"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)




