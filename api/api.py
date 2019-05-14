import requests
from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api

# Create the application instance
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('amount')
parser.add_argument('input_currency')
parser.add_argument('output_currency')


class CurrencyConverter(Resource):
    def get(self):

        args = parser.parse_args()

        amount = args.get('amount')
        input_currency = args.get('input_currency')
        output_currency = args.get('output_currency')

        # Fails
        if not input_currency:
            return {"error": "input_currency required"}
         
        if not amount:
            return {"error": "amount required"}
        
        amount = float(amount)

        if amount <= 0:
            return {"error": "amount invalid"}

        # Get data currency  
        url = "https://api.exchangerate-api.com/v4/latest/{}".format(input_currency)
        resp = requests.get(url)

        if resp.status_code != 200:
            
            return {"error": "API error"}
        
        # Convert 
        data = resp.json()

        if output_currency:
            return {
                "input": {
                    "amount": amount,
                    "currency": input_currency,
                },

                "output": {
                    output_currency: round(data['rates'][output_currency] * amount, 2),
                }
            }

        else:

            currencies = data['rates']

            if input_currency in currencies:
                del currencies[input_currency]

            for output_currency in currencies:
                new_currencies = [{i: round(v * amount, 2) for i, v in currencies.items()}]

            return {
                "input": {
                    "amount": amount,
                    "currency": input_currency,
                },
                "output": new_currencies
            }

api.add_resource(CurrencyConverter, '/currency_converter')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
