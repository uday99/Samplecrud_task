# Samplecrud_task

Firslty
1. Install the packages using
  pip install -r requirements.txt


2. create a local database in postgres

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'syoftdb',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}









3. Then makemigrations and migrate to create the table

    python manage.py makemigrations
    python manage.py migrate

4. After table creation enter the data in role table manaually

   
    id    role_name
========================== 

    1	    "A"
    2	    "M"
    3	    "S" 




1. Registering a User

  method=POST

   http://localhost:8000/register/user/


   

  
  payload_data


    role_id

     1 for admin
     2 for Manger
     3 for staff 

   {
    "username":"sharanya",
    "password":"sharanya123@@",
    "email":"sharanya123@gmail.com",
    "role_id":3
  }





2. Login a user and generate a token
    
   method = POST
    http://localhost:8000/user/login/


   payload-data

      {
    "username":"harish",
    "password":"harish123@@"
     }



3. Create or add products in productMOdel or product table
   

   1. ONly admin can add the data
   

      method =  POST:

      http://localhost:8000/product/add/view/

      payload
      ========
       {
    "title":"garments",
    "description":"ffooooooorehfrfvdfef",
    "inventory_count":15
    
    }
4. TO view the Data from products
   1. Manager  and Admin can only view the data

    method == GET
    
     http://localhost:8000/product/add/view/


5. To UPdate the product model:
    
   Method : PUT
   
    http://localhost:8000/product/update/delete/2/
    

   payload

      {

    "title":"Iphone",
    "description":"Iphone is very costlies mobile in india",
    "inventory_count":20
}


6. To  DELETE the  product
  

   method : DELETE

     http://localhost:8000/product/update/delete/2/


7. Staff cannot perform any crud operations
   
   

    











