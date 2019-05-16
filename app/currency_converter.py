#!/usr/bin/python3

import click
import requests
import json
from api import currency_converter

@click.command()
@click.option('--amount', nargs=1, type=float)
@click.option('--input-currency', nargs=1)
@click.option('--output-currency')
def main(amount, input_currency, output_currency):
    resp = currency_converter(amount,input_currency, output_currency)
    print(json.dumps(resp if isinstance(resp, dict) else resp[0], indent=4))


if __name__ == "__main__":
    main()