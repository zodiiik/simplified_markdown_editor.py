import math
import argparse
from datetime import datetime

class CreditCalculator:
    def __init__(self):
        # Инициализация и парсинг аргументов командной строки
        self.args = self.parse_arguments()
        # Валидация введенных параметров
        self.validate_arguments()
        
    def parse_arguments(self):
        # Создаем парсер аргументов командной строки
        parser = argparse.ArgumentParser(description='Кредитный калькулятор')
        # Добавляем возможные аргументы:
        parser.add_argument('--type', choices=['diff', 'annuity'], help='Тип платежа: дифференцированный или аннуитетный')
        parser.add_argument('--principal', type=float, help='Основная сумма кредита')
        parser.add_argument('--periods', type=int, help='Количество месяцев для погашения')
        parser.add_argument('--interest', type=float, help='Годовая процентная ставка')
        parser.add_argument('--payment', type=float, help='Ежемесячный платеж')
        return parser.parse_args()
    
    def validate_arguments(self):
        args = self.args
        
        # Проверка обязательных параметров
        if not args.type or args.type not in ['diff', 'annuity']:
            self.error("Некорректные параметры")
        
        # Для дифференцированных платежей не должно быть параметра payment
        if args.type == 'diff' and args.payment:
            self.error("Некорректные параметры")
            
        # Процентная ставка обязательна для всех расчетов
        if not args.interest:
            self.error("Некорректные параметры")
            
        # Проверка на отрицательные значения
        for param in [args.principal, args.periods, args.interest, args.payment]:
            if param is not None and param < 0:
                self.error("Некорректные параметры")
                
        # Проверка количества параметров
        if args.type == 'diff':
            # Для дифференцированных платежей нужны: сумма, срок и проценты
            if not all([args.principal, args.periods, args.interest]):
                self.error("Некорректные параметры")
        else:  # Аннуитетные платежи
            # Должно быть известно минимум 2 параметра из 3 (сумма, срок, платеж)
            known_params = sum(1 for param in [args.principal, args.periods, args.payment] if param is not None)
            if known_params < 2:
                self.error("Некорректные параметры")
    
    def error(self, message):
        # Вывод сообщения об ошибке и завершение программы
        print(message)
        exit()
    
    def calculate(self):
        # Выбор типа расчета в зависимости от введенных параметров
        if self.args.type == 'diff':
            self.calculate_diff_payments()
        else:
            self.calculate_annuity()
    
    def calculate_diff_payments(self):
        # Расчет дифференцированных платежей
        principal = self.args.principal
        periods = self.args.periods
        # Перевод годовой ставки в месячную (в долях)
        interest = self.args.interest / (12 * 100)
        
        total_payment = 0
        # Расчет платежа для каждого месяца
        for m in range(1, periods + 1):
            # Формула дифференцированного платежа
            payment = math.ceil(principal / periods + interest * (principal - (principal * (m - 1)) / periods)
            total_payment += payment
            print(f"Месяц {m}: платеж составляет {payment}")
        
        # Расчет переплаты (общая сумма платежей - основная сумма кредита)
        overpayment = total_payment - principal
        print(f"\nПереплата = {overpayment}")
    
    def calculate_annuity(self):
        # Определение, какой параметр нужно рассчитать для аннуитета
        if self.args.payment is None:
            self.calculate_annuity_payment()
        elif self.args.principal is None:
            self.calculate_annuity_principal()
        else:
            self.calculate_annuity_periods()
    
    def calculate_annuity_payment(self):
        # Расчет аннуитетного платежа
        principal = self.args.principal
        periods = self.args.periods
        interest = self.args.interest / (12 * 100)
        
        # Формула аннуитетного платежа
        payment = principal * (interest * (1 + interest)**periods) / ((1 + interest)**periods - 1)
        payment = math.ceil(payment)
        
        # Расчет переплаты
        overpayment = payment * periods - principal
        
        print(f"Ваш аннуитетный платеж = {payment}!")
        print(f"Переплата = {overpayment}")
    
    def calculate_annuity_principal(self):
        # Расчет основной суммы кредита для аннуитета
        payment = self.args.payment
        periods = self.args.periods
        interest = self.args.interest / (12 * 100)
        
        # Формула расчета основной суммы
        principal = payment / ((interest * (1 + interest)**periods) / ((1 + interest)**periods - 1))
        principal = math.floor(principal)
        
        # Расчет переплаты
        overpayment = payment * periods - principal
        
        print(f"Основная сумма кредита = {principal}!")
        print(f"Переплата = {overpayment}")
    
    def calculate_annuity_periods(self):
        # Расчет срока кредита для аннуитета
        principal = self.args.principal
        payment = self.args.payment
        interest = self.args.interest / (12 * 100)
        
        # Формула расчета количества периодов
        periods = math.log(payment / (payment - interest * principal), 1 + interest)
        periods = math.ceil(periods)
        
        # Преобразование месяцев в годы и месяцы
        years = periods // 12
        months = periods % 12
        
        # Форматирование вывода срока
        period_str = ""
        if years > 0:
            period_str += f"{years} год(а/лет) "
        if months > 0:
            period_str += f"и {months} месяц(ев)"
        
        # Расчет переплаты
        overpayment = payment * periods - principal
        
        print(f"Для погашения кредита потребуется {period_str.strip()}!")
        print(f"Переплата = {overpayment}")

if __name__ == "__main__":
    # Создание экземпляра калькулятора и запуск расчетов
    calculator = CreditCalculator()
    calculator.calculate()