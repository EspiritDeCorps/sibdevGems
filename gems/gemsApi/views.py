from rest_framework import status
from .models import HistoryDeals
from rest_framework.views import APIView
from rest_framework.response import Response
from io import StringIO
import json
import csv
import datetime

"""
Метод Get возвращает в формате JSON 5 покупателей с наибольшим количеством
потраченных денег за весь период, список из названий камней, которые купили как
минимум двое
Метод POST принимает CSV файлы  
"""

class gemsView(APIView):
    def get(self, request):
        customers = {}
        for deal in HistoryDeals.objects.all():
            customers.setdefault(deal.customer, [0, set()])
            customers[deal.customer][0] += deal.total
            customers[deal.customer][1].add(deal.item)

        listCustomers = list(customers.items())
        listCustomers.sort(key=lambda total: total[1][0], reverse=True)
        listCustomers = listCustomers[:5]

        jsonCustomers = ""
        for customer, items in listCustomers:
            spentMoney, gems = items
            temp = gems.copy()
            gems.clear()
            for secondCustomer in listCustomers:
                gems.update(temp & secondCustomer[1][1])

            jsonCustomers += json.dumps(
                {"username": customer, "spent_money": spentMoney, "gems": list(gems)})


        return Response(jsonCustomers)

    def post(self, request, format=None):

        try:
            csvStr = request.read().decode("utf-8")
            csvFile = StringIO(csvStr)
            csvReader = csv.reader(csvFile)
        except:
            return Response("Это не CSV файл", status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if next(csvReader) != ['customer', 'item', 'total', 'quantity', 'date']:
            return Response("Неверные поля в CSV файле",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        listDeals = []
        for row in csvReader:
            try:
                customer = row[0]
                item = row[1]
                total = int(row[2])
                quantity = int(row[3])
                date = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')
            except:
                return Response("Ошибка ковертации значений CSV файла",status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            listDeals.append(HistoryDeals(customer=customer, item=item, total=total, quantity=quantity, date=date))
        for deal in listDeals:
            deal.save()

        return Response(status=status.HTTP_101_SWITCHING_PROTOCOLS)
