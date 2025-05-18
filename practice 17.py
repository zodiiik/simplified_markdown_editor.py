import requests
import json

class CurrencyExchange:
    def __init__(self):
        self.cache = {}
        self.base_currency = None

    def stage_1(self):
        """Етап 1: Проста конвертація mycoin в долари"""
        try:
            mycoins = float(input("Please, enter the number of mycoins you have: "))
            rate = float(input("Please, enter the exchange rate: "))
            dollars = mycoins * rate
            print(f"The total amount of dollars: {dollars:.2f}")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

    def stage_2(self):
        """Етап 2: Конвертація mycoin в інші валюти"""
        try:
            mycoins = float(input("Please, enter the number of mycoins you have: "))
            
            # Задані курси валют
            rates = {
                'ARS': 0.82,  # Аргентинське песо
                'HNL': 0.17,  # Гондураська лемпіра
                'AUD': 1.9622,  # Австралійський долар
                'MAD': 0.208   # Марокканський дирхам
            }
            
            for currency, rate in rates.items():
                amount = mycoins * rate
                print(f"I will get {amount:.2f} {currency} from the sale of {mycoins} mycoins.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")

    def stage_3(self):
        """Етап 3: Отримання актуальних курсів з FloatRates"""
        currency_code = input("Please, enter the currency code (e.g., AUD): ").upper().strip()
        url = f"http://www.floatrates.com/daily/{currency_code}.json"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print("Failed to fetch currency rates.")
                return
                
            data = response.json()
            
            # Виводимо курси для USD і EUR
            print(f"Exchange rates for {currency_code}:")
            if 'usd' in data:
                print(f"USD: {data['usd']['rate']:.4f}")
            if 'eur' in data:
                print(f"EUR: {data['eur']['rate']:.4f}")
                
        except requests.exceptions.RequestException:
            print("Error fetching currency rates.")

    def stage_4(self):
        """Етап 4: Обмін валют з кешуванням"""
        self.base_currency = input("Enter your currency code: ").lower().strip()
        
        # Завантажуємо курси для USD і EUR за замовчуванням
        self._fetch_and_cache('usd')
        self._fetch_and_cache('eur')
        
        while True:
            target_currency = input("Enter target currency code (or leave empty to exit): ").lower().strip()
            if not target_currency:
                break
                
            try:
                amount = float(input("Enter amount to exchange: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
                
            self._exchange_currency(target_currency, amount)

    def _fetch_and_cache(self, currency_code):
        """Отримує курс валюти і зберігає у кеш"""
        if currency_code in self.cache or currency_code == self.base_currency:
            return
            
        url = f"http://www.floatrates.com/daily/{self.base_currency}.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if currency_code in data:
                    self.cache[currency_code] = data[currency_code]['rate']
        except requests.exceptions.RequestException:
            pass

    def _exchange_currency(self, target_currency, amount):
        """Виконує обмін валюти з перевіркою кешу"""
        print("Checking the cache...")
        
        if target_currency == self.base_currency:
            print("It is in the cache!")
            print(f"You received {amount:.2f} {target_currency.upper()}.")
            return
            
        if target_currency in self.cache:
            print("It is in the cache!")
            rate = self.cache[target_currency]
        else:
            print("Sorry, but it is not in the cache!")
            url = f"http://www.floatrates.com/daily/{self.base_currency}.json"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if target_currency in data:
                        rate = data[target_currency]['rate']
                        self.cache[target_currency] = rate
                    else:
                        print(f"Currency {target_currency.upper()} not found.")
                        return
                else:
                    print("Failed to fetch currency rate.")
                    return
            except requests.exceptions.RequestException:
                print("Error fetching currency rate.")
                return
                
        converted_amount = amount * rate
        print(f"You received {converted_amount:.2f} {target_currency.upper()}.")

def main():
    print("Практична робота №17 'Обмін валют'")
    print("Оберіть етап для виконання:")
    print("1 - Проста конвертація mycoin в долари")
    print("2 - Конвертація mycoin в інші валюти")
    print("3 - Отримання актуальних курсів з FloatRates")
    print("4 - Обмін валют з кешуванням")
    
    exchange = CurrencyExchange()
    
    choice = input("Ваш вибір (1-4): ")
    {
        '1': exchange.stage_1,
        '2': exchange.stage_2,
        '3': exchange.stage_3,
        '4': exchange.stage_4
    }.get(choice, lambda: print("Невірний вибір"))()

if __name__ == "__main__":
    main()