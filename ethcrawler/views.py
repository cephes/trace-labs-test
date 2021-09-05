import requests
from django.http import HttpResponse
from django.shortcuts import render

import time
import datetime

from django.template import loader


def check_balance(request):
    addr = request.GET['address2']
    t = request.GET['date']
    ts = int(time.mktime(datetime.datetime.strptime(t, "%Y-%m-%d").timetuple()))

    r = requests.get("https://api.etherscan.io/api"
                     "?module=block"
                     "&action=getblocknobytime"
                     "&timestamp=" + str(ts) +
                     "&closest=before"
                     "&apikey=W9FZQXURBZSTXATJTIUGK7QJZPFYRW12N5",
                     headers={"Content-Type": "application/json"}, )
    blockno = r.json()['result']

    r = requests.get("https://api.etherscan.io/api?module=account"
                     "&action=txlist"
                     "&address=" + addr +
                     "&startblock=" + blockno +
                     "&endblock=99999999"
                     "&page=1"
                     "&offset=10"
                     "&sort=asc"
                     "&apikey=W9FZQXURBZSTXATJTIUGK7QJZPFYRW12N5",
                     headers={"Content-Type": "application/json"}, )
    normal_transactions = r.json()['result']

    balance = 0
    for element in normal_transactions:

        if element['from'] == addr:
            balance += int(element['value']) / 1000000000000000000 + (int(element['gasPrice']) / 1000000000000000000) * int(element['gasUsed'])
        elif element['to'] == addr:
            balance -= int(element['value']) / 1000000000000000000 + (int(element['gasPrice']) / 1000000000000000000) * int(element['gasUsed'])

    r = requests.get("https://api.etherscan.io/api"
                     "?module=account"
                     "&action=tokentx"                     
                     "&address="+addr +
                     "&page=1"
                     "&offset=100"
                     "&sort=asc"
                     "&apikey=W9FZQXURBZSTXATJTIUGK7QJZPFYRW12N5",
                     headers={"Content-Type": "application/json"}, )

    ftresponse = r.json()['result']

    r = requests.get("https://api.etherscan.io/api"
                     "?module=account"
                     "&action=tokennfttx"                     
                     "&address="+addr +
                     "&page=1"
                     "&offset=100"
                     "&sort=asc"
                     "&apikey=W9FZQXURBZSTXATJTIUGK7QJZPFYRW12N5",
                     headers={"Content-Type": "application/json"}, )

    nftresponse = r.json()['result']
    #import pdb;pdb.set_trace()
    context = {'balance': balance, 'fttokens': ftresponse, 'nfttokens': nftresponse}
    return render(request, 'ethcrawler/balance.html', context)


def check_by_block(request):
    addr = request.GET['address1']
    blockno = request.GET['block']
    r = requests.get("https://api.etherscan.io/api?module=account"
                     "&action=txlist"
                     "&address=" + addr +
                     "&startblock=" + blockno +
                     "&endblock=99999999"
                     "&page=1"
                     "&offset=10"
                     "&sort=asc"
                     "&apikey=W9FZQXURBZSTXATJTIUGK7QJZPFYRW12N5",
                     headers={"Content-Type": "application/json"}, )
    response = r.json()

    context = {'results': response['result']}
    return render(request, 'ethcrawler/history.html', context)


def home(request):
    return render(request, 'ethcrawler/home.html')