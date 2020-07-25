# eShopOnline
Create Customers Order, Get Shipment Details with multple Order and items, Insert Products using Django Rest Frame work with JWT

# pip requirements
pip install -r pip requirements.txt

Django==2.1.7
django-cors-headers==3.1.1
djangorestframework==3.10.3
djangorestframework-simplejwt==4.3.0
psycopg2==2.7.5
psycopg2-binary==2.8.4
gunicorn
supervisor

-------------------------------

# python manage.py makemigrations sales
  python manage.py migrate

----------------------------------------

# Insert Products & Shipment
  python manage.py test_data_insert

----------------------------------------------------

# Run App server
supervisord -c supervisord.conf 
supervisorctl restart all
supervisorctl shutdown



----------------------------------------------------

#Register

http://localhost:8001/customer/register

{
                    "first_name":"customer3",
                    "last_name" :"c3",
                    "username" : "customer3",
                    "email" : "customer3@demo.com",
                    "password" : "customer#123"
                    }


{
    "success": true,
    "errors": {},
    "data": {
        "message": "Customer A/c Registered successfully"
    }
}


-----------------------------------------------------

# Login

http://localhost:8001/customer/login

{
                   
                    "username" : "customer3",
                    "password" : "customer#123"
                    }



{
    "success": true,
    "errors": {},
    "data": {
        "email": "customer3@demo.com",
        "customer_id": 3,
        "username": "customer3",
        "first_name": "customer3",
        "last_name": "c3",
        "message": "Customer Loggged In successfully"
    }
}


----------------------------------------------------


# Create Order
http://localhost:8001/customer/order/create
{
    "customer_id":1,
    "amount" :"20",
    "items" : [{"item_id" : 13, "price" : 10},{"item_id" : 14, "price" : 10}]
    }


------------------------------------------------------

# Shipment Details
http://localhost:8001/shipment/details
{
	
	"shipmentId" : 2
	
}


{
    "errors": {},
    "data": {
        "shipmentId": 2,
        "shipmentDate": "2020-07-25T09:50:26.593150Z",
        "ordersList": [
            {
                "amount": 100,
                "orderItemsList": [
                    {
                        "orderItemId": 1,
                        "title": "item_0",
                        "price": 10
                    }
                ],
                "orderId": 3
            },
            {
                "amount": 100,
                "orderItemsList": [
                    {
                        "orderItemId": 2,
                        "title": "item_0",
                        "price": 10
                    },
                    {
                        "orderItemId": 3,
                        "title": "item_1",
                        "price": 10
                    }
                ],
                "orderId": 4
            },
            {
                "amount": 20,
                "orderItemsList": [
                    {
                        "orderItemId": 4,
                        "title": "item_0",
                        "price": 10
                    },
                    {
                        "orderItemId": 5,
                        "title": "item_1",
                        "price": 10
                    }
                ],
                "orderId": 5
            },
            {
                "amount": 20,
                "orderItemsList": [
                    {
                        "orderItemId": 6,
                        "title": "item_0",
                        "price": 10
                    },
                    {
                        "orderItemId": 7,
                        "title": "item_1",
                        "price": 10
                    }
                ],
                "orderId": 6
            }
        ]
    },
    "success": true
}

---------------------------------------------------------
# JWT TOken Example

http post http://127.0.0.1:8001/api/token/ username=test password=123

{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQ1MjI0MjU5LCJqdGkiOiIyYmQ1NjI3MmIzYjI0YjNmOGI1MjJlNThjMzdjMTdlMSIsInVzZXJfaWQiOjF9.D92tTuVi_YcNkJtiLGHtcn6tBcxLCBxz9FKD3qzhUg8",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0NTMxMDM1OSwianRpIjoiMjk2ZDc1ZDA3Nzc2NDE0ZjkxYjhiOTY4MzI4NGRmOTUiLCJ1c2VyX2lkIjoxfQ.rA-mnGRg71NEW_ga0sJoaMODS5ABjE5HnxJDb0F8xAo"
}



