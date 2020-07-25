from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from sales.models import User, Shipments, Products, Orders, OrderProducts, OrderShipments
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

class CustomerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=60)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=100)

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=100)


class CustomerOrderCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = serializers.ListField()
    amount= serializers.DecimalField(6,2)

class ShipmentDetailsSerializer(serializers.Serializer):
    shipmentId = serializers.IntegerField()
    

class CustomAPIResponse():

    def __init__(self, **kwargs):
        self.response = {
            "success": kwargs.get('success'),
            "errors": kwargs.get('errors', {}),
            "data": kwargs.get('data', {}),
        }

class CustomerRegisterViewSet(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        logger.info("*** CustomerRegisterViewSet POST or Update Request Process start ***")
        logger.info(request.data)
        try:
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user_obj = User.objects.get(username=request.data['username'])
                except User.DoesNotExist as e:
                    user_obj = None
                if user_obj is None:
                    user_obj = User.objects.create(
                            username=request.data['username'], 
                            email=request.data['email'], 
                            first_name=request.data['first_name'],
                            last_name=request.data['last_name']
                            )
                    user_obj.set_password(request.data['password'])
                    user_obj.is_active=True
                    user_obj.save()
                    status_code = 201
                    context_data = {"success": True, "data": {"message": "Customer A/c Registered successfully"}}
                else:
                    status_code = 400
                    context_data = {"success": False, "errors": {"message": "Customer A/c Already Exist"}}

            else:
                context_data = {"success": False, "errors": {"message": "Validation Errors", "errors_list": serializer.errors}}
                status_code = 400
        except Exception:
            status_code = 500
            logger.info("*** CustomerRegisterViewSet POST Exception {} ***".format(traceback.format_exc()))
            context_data = {"success": False, "errors": {"message": "Internal Server Error"}}

        response_data = CustomAPIResponse(**context_data).response
        logger.info(response_data)
        logger.info("*** CustomerRegisterViewSet POST Request Process End ***")
        return Response(response_data, status=status_code)


class CustomerLoginViewSet(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        logger.info("*** CustomerLoginViewSet POST or Update Request Process start ***")
        logger.info(request.data)
        try:
            serializer = CustomerLoginSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user_obj = User.objects.get(Q(username=request.data['username']) & Q(is_active=True))
                except User.DoesNotExist as e:
                    user_obj = None
                if user_obj:
                    if user_obj.check_password(request.data['password']):
                        status_code = 200
                        context_data = {"success": True, "data": {
                                                        "message": "Customer Loggged In successfully", 
                                                        "username" : user_obj.username, 
                                                        "first_name" : user_obj.first_name, 
                                                        "last_name" : user_obj.last_name, 
                                                        "email" : user_obj.email, 
                                                        "customer_id" : user_obj.pk  }}
                    else:
                        status_code = 400
                        context_data = {"success": False, "data": {"message": "Invalid Password"}}
                else:
                    status_code = 400
                    context_data = {"success": False, "errors": {"message": "Invalid Login Credentials"}}

            else:
                context_data = {"success": False, "errors": {"message": "Validation Errors", "errors_list": serializer.errors}}
                status_code = 400
        except Exception:
            status_code = 500
            logger.info("*** CustomerLoginViewSet POST Exception {} ***".format(traceback.format_exc()))
            context_data = {"success": False, "errors": {"message": "Internal Server Error"}}

        response_data = CustomAPIResponse(**context_data).response
        logger.info(response_data)
        logger.info("*** CustomerLoginViewSet POST Request Process End ***")
        return Response(response_data, status=status_code)



class CustomeOrderCreateViewSet(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        logger.info("*** CustomeOrderCreateViewSet POST or Update Request Process start ***")
        logger.info(request.data)
        try:
            serializer = CustomerOrderCreateSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    user_obj = User.objects.get(Q(pk=request.data['customer_id']) & Q(is_active=True))
                except User.DoesNotExist as e:
                    user_obj = None
                if user_obj:
                    order_obj = Orders.objects.create(user=user_obj, order_date=datetime.now(), amount=request.data['amount'])
                    for each_item in request.data['items']:
                        product_obj = Products.objects.get(pk=each_item['item_id'])
                        OrderProducts.objects.create(order=order_obj, product=product_obj, price=each_item['price'])
                    shipment_obj = Shipments.objects.all().first()
                    OrderShipments.objects.create(order=order_obj, shipment_date=datetime.now(), shipment=shipment_obj)
                    status_code = 200
                    context_data = {"success": True, "data": {"message": "Order Created successfully", "order_id" : order_obj.pk, "shipment_id" : shipment_obj.pk}}
                else:
                    status_code = 400
                    context_data = {"success": False, "errors": {"message": "Invalid Customer Id"}}

            else:
                context_data = {"success": False, "errors": {"message": "Validation Errors", "errors_list": serializer.errors}}
                status_code = 400
        except Exception:
            status_code = 500
            logger.info("*** CustomeOrderCreateViewSet POST Exception {} ***".format(traceback.format_exc()))
            context_data = {"success": False, "errors": {"message": "Internal Server Error"}}

        response_data = CustomAPIResponse(**context_data).response
        logger.info(response_data)
        logger.info("*** CustomeOrderCreateViewSet POST Request Process End ***")
        return Response(response_data, status=status_code)

class ShipmentDetailsViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        """
        Response
        {
            "shipmentId": 1234,
            "shipmentDate": "12-12-2020",
            "ordersList": [
                {
                    "orderId": 1,
                    "amount": 123,
                    "orderItemsList": [
                        {
                            "orderItemId": 1,
                            "title": "asdf",
                            "price": 12.50
                        },
                        {
                            "orderItemId": 2,
                            "title": "qwer",
                            "price": 23.50
                        },
                    ]
                },
                {
                    "orderId": 2,
                    "amount": 300.00,
                    "orderItemsList": [
                        {
                            "orderItemId": 3,
                            "title": "asdf",
                            "price": 12.50
                        },
                        {
                            "orderItemId": 4,
                            "title": "qwer",
                            "price": 23.50
                        },
                    ]
                }
            ]
        }
        """
        logger.info("*** ShipmentDetailsViewSet POST or Update Request Process start ***")
        logger.info(request.data)
        try:
            serializer = ShipmentDetailsSerializer(data=request.data)
            if serializer.is_valid():
                shipment_order_obj_list = OrderShipments.objects.filter(Q(shipment_id=request.data['shipmentId']))
                if shipment_order_obj_list.count() > 0:
                    orders_list = []
                    shipment_date = None
                    for each_shipment_order_obj  in shipment_order_obj_list:
                        shipment_date = each_shipment_order_obj.shipment_date
                        order_obj = each_shipment_order_obj.order
                        product_obj_list = OrderProducts.objects.filter(order=order_obj)
                        item_list = []
                        for each_item in product_obj_list:
                            item = {
                                    "orderItemId": each_item.pk,
                                    "title": each_item.product.title,
                                    "price": each_item.price
                                }
                            item_list.append(item)
                        order_item_dict = {
                        "orderId" : order_obj.pk,
                        "amount" : order_obj.amount,
                        "orderItemsList" : item_list
                        }
                        orders_list.append(order_item_dict)
                    shipment_dict = {
                        "shipmentId": request.data['shipmentId'],
                        "shipmentDate": shipment_date,
                        "ordersList" : orders_list
                    }
                    context_data = {"success": True, "data": shipment_dict}
                    status_code = 200

                else:
                    status_code = 400
                    context_data = {"success": False, "errors": {"message": "No Orders Exist"}}

            else:
                context_data = {"success": False, "errors": {"message": "Validation Errors", "errors_list": serializer.errors}}
                status_code = 400
        except Exception:
            status_code = 500
            logger.info("*** ShipmentDetailsViewSet POST Exception {} ***".format(traceback.format_exc()))
            context_data = {"success": False, "errors": {"message": "Internal Server Error"}}

        response_data = CustomAPIResponse(**context_data).response
        logger.info(response_data)
        logger.info("*** ShipmentDetailsViewSet POST Request Process End ***")
        return Response(response_data, status=status_code)