from django import http
from django.shortcuts import render
from .wallet import (create_wallet, 
                     load_wallet, 
                     get_balance, 
                     fund_account, 
                     send_sol)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *

from .serializers import *


@api_view(['POST'])
def create_wallet_view(request):
    """
    Create a new wallet
    """
    if request.method == 'POST':
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet_address = create_wallet(request.user.id)
            print(wallet_address)
            serializer.save(public_key=wallet_address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def load_wallet_view(request):
    """
    Given a username, load the wallet associated with that username
    
    :param request: The HTTP request that triggered this view function
    :param username: The username of the user whose wallet you want to load
    :return: The serialized data of the wallet.
    """
    if request.method == 'GET':
        wallet = load_wallet(request.user.username)
        if wallet is not None:
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_wallet_balance_view(request):
    """
    This function is used to get the balance of a wallet
    
    :param request: The HTTP request that triggered this view function
    :param username: The username of the user
    :return: The serialized data of the wallet balance.
    """
    if request.method == 'GET':
        wallet = load_wallet(request.user.name)
        if wallet is not None:
            balance = get_balance(wallet['public_key'])
            if balance is not None:
                serializer = WalletSerializer(balance)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)



class WalletCreateView(CreateAPIView):
    # get the user's username (email), create a wallet via a post request, and return the wallet's public key
    serializer_class = WalletCreationSerializer
    http_method_names= ['post']
    
    
    def perform_create(self, serializer):
        # get the user's username, create a wallet via a post request, and return the wallet's public key
        serializer = self.serializer_class(data=self.request.data)
        
        if serializer.is_valid():
            user = self.request.user
            # print(user.id)
            wallet_address = create_wallet(str(user.id))
            
            serializer.save(user=user, public_key=wallet_address)
            
            message = {
                'userId': user.id,
                'publicKey': wallet_address,
                'balance': serializer.data['balance'],
                'creation_date': serializer.data['creation_date'],
            }
            print(message)
            return Response(message, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    
    # def get(self, request, format=None):
    #     # get the user's username (email), load the wallet associated with that username, and return the wallet's public key
        
    #     user = request.user
    #     wallet = load_wallet(user.id)
    #     if wallet is not None:
    #         serializer = WalletSerializer(wallet)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_404_NOT_FOUND)