#!/usr//bin/python3

# import sys
import click
import requests

@click.command()
@click.option('--amount', nargs=1, type=float)
@click.option('--input-currency', nargs=1)
@click.option('--output-currency')

def main(amount, input_currency, output_currency):
    
    # print(amount,output_currency,input_currency)
    
    # report errors args    
    if output_currency:
        output_currency = output_currency.upper().strip()
    
    if not input_currency:
        print({"error": "You must specify the input currency"})
  
    input_currency = input_currency.upper().strip()
    
    if not amount:
        print({"error": "This amount is invalid"})

    amount = float(amount)

    if amount <= 0:
        print({"error": "This amount must be <=0"})

    # Get data currency   
    
    url = "https://api.exchangerate-api.com/v4/latest/{}".format(input_currency)
    resp = requests.get(url)

    data = resp.json()
    
    if resp.status_code != 200:
        print({"error": "Remote API server error, {}".format(resp.status_code)})

    # Convert 

    if output_currency:
        print({
            "input": {
                "amount": amount,
                "currency": input_currency,
            },

            "output": {
                output_currency: round(data['rates'][output_currency] * amount, 2),
            }
        })

    else:
        currencies = data['rates']

        if input_currency in currencies:
            del currencies[input_currency]

        for output_currency in currencies:
            new_currencies = [{i: round(v * amount, 2) for i, v in currencies.items()}]

        print({ 
            "input": {
                "amount": amount,
                "currency": input_currency,
            },
            "output": new_currencies
        })

if __name__ == "__main__":
    main()