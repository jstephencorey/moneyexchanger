import unittest
from unittest.mock import Mock, patch, MagicMock
from MoneyExchanger import MoneyExchanger


class MoneyExchangerUnitTest(unittest.TestCase):

    # # Test that MoneyExchanger can correctly load valid symbols
    def _test_symbols_success_get_api_result(self, api_url):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'symbols': {"USD": "United States Dollars","GBP":"Great British Pounds"}
        }
        return mock_response

    def test_get_valid_symbols_success(self):
        with patch.object(MoneyExchanger, '_get_api_result', self._test_symbols_success_get_api_result):
            exchanger = MoneyExchanger()
            self.assertEqual(exchanger.symbols,['USD','GBP'])

    # # Test that MoneyExchanger will throw an exception if API fails
    def _test_symbols_fail_get_api_result(self, api_url):
        mock_response = MagicMock()
        mock_response.status_code = 400
        return mock_response
        
    def test_get_valid_symbols_fail(self):
        with patch.object(MoneyExchanger, '_get_api_result', self._test_symbols_fail_get_api_result):
            with self.assertRaises(Exception):
                MoneyExchanger()

    # Test that MoneyExchanger.convert_currency will fail if you try to convert something with an invalid currency
    def test_convert_currency_fail_invalid_symbol(self):
        with patch.object(MoneyExchanger, '_get_api_result', self._test_symbols_success_get_api_result):
            with self.assertRaises(Exception):
                exchanger = MoneyExchanger()
                exchanger.convert_currency("USD","ZZZ", 7)

    # Test that MoneyExchanger.convert_currency fails if you don't pass a valid amount type
    def test_convert_currency_fail_invalid_currency_type(self):
        with patch.object(MoneyExchanger, '_get_api_result', self._test_symbols_success_get_api_result):
            with self.assertRaises(Exception):
                exchanger = MoneyExchanger()
                exchanger.convert_currency("USD","GBP","42")
 
    # Test that MoneyExchanger.convert_currency converts money correctly
    def _test_convert_success_get_api_results(self, api_url):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': 42.42,
            'symbols': {"USD": "United States Dollars","GBP":"Great British Pounds"}
        }
        return mock_response

    def test_convert_currency_success(self):
        with patch.object(MoneyExchanger, '_get_api_result', self._test_convert_success_get_api_results):
            exchanger = MoneyExchanger()
            self.assertEqual(exchanger.convert_currency("USD","GBP",42), 42.42)

if __name__ == '__main__':
    unittest.main()
