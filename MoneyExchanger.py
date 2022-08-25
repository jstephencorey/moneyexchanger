from numpy import array
import requests

class MoneyExchanger():
    def __init__(self):
        # self.api = ExchangeApi(self.API_URL, self.API_KEY)
        self.API_URL = "https://api.apilayer.com/fixer/"
        self.API_KEY = "7ToJDm8RU0PCoB87ImaKHA3wugjZEYfQ"
        self.symbols = self._get_valid_symbols()

    def convert_currency(self,currencyFrom, currencyTo, amount):
        if currencyFrom not in self.symbols or currencyTo not in self.symbols:
            raise Exception(f"Not a valid currency, valid currencies are:\n {self.symbols}")
        if not isinstance(amount,float) and not isinstance(amount, int):
            raise Exception("Not a valid amount to convert, please use a valid number")
        else:
            return self._convert(currencyFrom, currencyTo, amount)

    def _convert(self, currencyFrom, currencyTo, amount):
        response = self._get_api_result(self.API_URL + f"convert?to={currencyTo}&from={currencyFrom}&amount={amount}")
        if response.status_code != 200:
            raise Exception("API issue, please try again later")
            # API Documentation: https://apilayer.com/marketplace/fixer-api#documentation-tab
        else:
            converted_amount = response.json()["result"]
            return converted_amount

    def _get_valid_symbols(self):
        response = self._get_api_result(self.API_URL + "symbols")
        if response.status_code != 200:
            raise Exception("API issue, please try again later")
            # API Documentation: https://apilayer.com/marketplace/fixer-api#documentation-tab
        else:
            symbol_dict = response.json()["symbols"]
            symbols = [key for key in symbol_dict.keys()]
        return symbols
    
    # This function makes the class easier to test
    def _get_api_result(self, api_url):
        return requests.get(api_url, headers={'apikey':self.API_KEY})

