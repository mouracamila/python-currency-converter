# Python Currency Converter


This application has CLI and API.
The exchange rates are obtained through the European Central Bank every day.

Here's the list of currency codes we this app support https://www.exchangerate-api.com/docs/supported-currencies

Here's more about the web API utilizad https://www.exchangerate-api.com/


Requirements
-
 - Python =< 3
 - click
 - flask
 - flask-restful
 - json

Parameters
-
- `amount` - amount to convert - Support to float numbers
- `input_currency` - input currency - Currency Code or Currency Symbol
- `output_currency` - requested/output currency - Currency Code or Currency Symbol

Obs: When the exit currency is not declared, it is converted to the entire known currency.

# Output
- json struture:

```
{
    "input": {
        "amount": <float>,
        "currency": <Currency Code>
    }
    "output": {
        <Currency Code>: <float>
    }
}
```
# Exemples
CLI
-
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36,
    }
}
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{
    "input": {
        "amount": 0.9,
        "currency": "JPY"
    },
    "output": {
        "AUD": 0.01
    }
}
```
```
./currency_converter.py --amount 10.92 --input_currency £
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": [
        {
            "AUD": 20.24,
            "BGN": 24.4,
            "BRL": 56.53,
            .
            .
        }
    ]
}
```
 API
-
```
GET /currency_converter?amount=0.9&input_currency=au$&output_currency=brl HTTP/1.1
{
    "input": {
        "amount": 0.9,
        "currency": "AUD"
    },
    "output": {
        "BRL": 2.51
    }
}
```
```
GET /currency_converter?amount=0.9&input_currency=CA$&output_currency= HTTP/1.1
{
    "input": {
        "amount": 0.9,
        "currency": "CAD"
    },
    "output": [
        {
            "AUD": 0.97,
            "BGN": 1.17,
            "BRL": 2.71,
            .
            .
            .
        }
    }
}
```
