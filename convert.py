from forex_python.converter import CurrencyRates, CurrencyCodes

currency = CurrencyRates()
symbol = CurrencyCodes()


class Conversion():

    def __init__(self, convertFrom='', convertTo='', amount=0):
        self.convertFrom = convertFrom.upper()
        self.convertTo = convertTo.upper()
        self.amount = amount

    def checkCurrency(self):
        """Check currency if valid or invalid"""
        if not (len(self.convertFrom) == 3):
            return 'Invalid from'
        if not(len(self.convertTo) == 3):
            return 'Invalid to'
        # Check currency if available in the API
        try:
            currency.get_rates(self.convertFrom)
        except:
            return 'Invalid from'

        # Check currency if available in the API
        try:
            currency.get_rates(self.convertTo)
        except:
            return 'Invalid to'

        # Check if amount is integer
        try:
            float(self.amount)
        except:
            return 'Invalid amount'

        return "Valid"

    def convertCurrency(self):
        """Converts the currency"""
        sym = self.getSymbol()
        amt = float(self.amount)
        val = currency.convert(
            self.convertFrom, self.convertTo, amt)
        return (f"The result is {sym} {val:,.2f}.")

    def getSymbol(self):
        """Get the symbol of the to currency"""
        return symbol.get_symbol(self.convertTo)
