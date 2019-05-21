# -*- coding: utf-8 -*-

import requests
from flask import Flask
from flask_restful import Resource, reqparse, Api

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('amount')
parser.add_argument('input_currency')
parser.add_argument('output_currency')


def currency_converter(amount, input_currency, output_currency=None):

    input_currency = input_currency.upper().strip()

    if output_currency:
        output_currency = output_currency.upper().strip()

    if not input_currency:
        return {"error": "Input Currency Required"}, 400

    currency_mapping = {
        '$': 'USD', 'R$': 'BRL', u'€': 'EUR', u'£': 'GBP',
        u'¥': 'JPY', 'CA$': 'CAD', u'Kč': 'CZK', 'AU$': 'AUD',
        'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', u'zł': 'PLN',
        }

    if input_currency in currency_mapping:
        input_currency = currency_mapping.get(input_currency)

    if output_currency in currency_mapping:
        output_currency = currency_mapping.get(output_currency)

    if not amount:
        return {"error": "Invalid Amount"}, 400

    amount = float(amount)

    if amount <= 0:
        return {"Bad Request": "Error 400"}

    url = "https://api.exchangerate-api.com/v4/latest/{}".format(
        input_currency)
    resp = requests.get(url)

    data = resp.json()

    if resp.status_code != 200:
        return {"error": "Remote API Server Error"}, resp.status_code

    if output_currency and output_currency not in data['rates']:

        return {"error": "Invalid Output Currency"}, 400

    elif output_currency:

        return {
            "input": {
                "amount": amount,
                "currency": input_currency,
            },

            "output": {
                output_currency: round(data['rates'][
                    output_currency] * amount, 2),
            }
        }

    else:

        currencies = data['rates']

        if input_currency in currencies:
            del currencies[input_currency]

        for output_currency in currencies:
            new_currencies = [{i: round(
                v * amount, 2) for i, v in currencies.items()}]

        return {
            "input": {
                "amount": amount,
                "currency": input_currency,
            },
            "output": new_currencies
        }


class CurrencyConverter(Resource):
    def get(self):

        args = parser.parse_args()

        amount = args.get('amount')
        input_currency = args.get('input_currency')
        output_currency = args.get('output_currency')
        return currency_converter(amount, input_currency, output_currency)


api.add_resource(CurrencyConverter, '/currency_converter')

if __name__ == '__main__':
    app.run(debug=True)
