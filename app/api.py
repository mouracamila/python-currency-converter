import requests
from flask import Flask
from flask_restful import Resource, reqparse, Api

# Create the application instance
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

    # if input currency code:
    if not input_currency:
        return {"error": "Input Currency Required"}, 400

    # if input_currency symbol
    currency_mapping = {
        '$': 'USD', 'R$': 'BRL', '€': 'EUR', '£': 'GBP',
        '¥': 'JPY', 'CA$': 'CAD', 'Kč': 'CZK', 'AU$': 'AUD',
        'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', 'zł': 'PLN',
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

    # Get data currency
    url = "https://api.exchangerate-api.com/v4/latest/{}".format(
        input_currency)
    resp = requests.get(url)

    data = resp.json()

    if resp.status_code != 200:
        return {"error": "Remote API Server Error"}, resp.status_code

    if output_currency and output_currency not in data['rates']:

        return {"error": "Invalid Output Currency"}, 400
    # Convert
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

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=False)
