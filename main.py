import re
from datetime import datetime, timedelta
from random import sample, random

from phone_codes import phone_list


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    name = input("Як вас звати?")
    print(f'Привіт, {name}\n')
    choose = int(input('Напишіть номер завдання, яке хочете перевірити'))
    if choose == 1:
        date_str = input(f'Ви обрали перше завдання, яке розраховує різницю між двома датами\n'
                         f'Введіть дату у форматі "РРРР-ММ-ДД"')
        get_days_from_today(date_str)
    elif choose == 2:
        mini = int(input(f'Ви обрали друге завдання, яка генерує набір унікальних випадкових чисел для лотерей\n'
                         f'Введіть мінімальне можливе число у наборі(не менше 1)'))
        maxi = int(input(f'Введіть максимальне можливе число у наборі (не більше 1000)'))
        quantity = int(input(f'Введіть кількість чисел, які потрібно вибрати (значення між min і max)'))
        print(get_numbers_ticket(mini, maxi, quantity))
    elif choose == 3:
        while True:
            phone_number = input(f'Ви обрали третє завдання, '
                                 f'яке автоматично нормалізує номери телефонів до потрібного формату, '
                                 f'видаляючи всі зайві символи та додаючи міжнародний код країни, якщо потрібно\n'
                                 f'Введіть номер телефону, який треба нормалізувати. '
                                 f'Функція трохи підпиляна для номерів України')
            # normalize_phone(phone_number)
            raw_numbers = [
                "067\\t123 4567",
                "(095) 234-5678\\n",
                "+380 44 123 4567",
                "380501234567",
                "    +38(050)123-32-34",
                "     0503451234",
                "(050)8889900",
                "38050-111-22-22",
                "38050 111 22 11   ",
            ]

            normalize_phone(phone_number)
            # normalize_phone(phone_number)
    elif choose == 4:
        print(f'Ви обрали четверте завдання, яке допоможе вам визначати, кого з колег потрібно привітати\n'
              f'З вводом щось не вийшло, '
              f'тому просто прикріпив інформацію про колег (список словників), дану в завданні')
        get_upcoming_birthdays(users)


# __________________________________________________ Перше завдання __________________________________________________ #

def get_days_from_today(date_str):
    try:
        # Перетворення рядка дати в об'єкт datetime
        date_provided = datetime.strptime(date_str, '%Y-%m-%d').date()
        # Отримання поточної дати
        current_date = datetime.today().date()
        # current_date = datetime(2021, 5, 5)
        # Розрахунок різниці у днях
        difference = (current_date - date_provided).days
        print("Різниця складає - ")
        print(difference)
        return difference
    except ValueError:
        print("Ви ввели неправильну дату. Або такого дня в місяці не існує або не по шаблону")


# ___________________________________________________Друге завдання___________________________________________________ #


def get_numbers_ticket(mini, maxi, quantity):
    if mini < 1 or maxi > 1000 or quantity < 1 or quantity > (maxi - mini + 1):
        return []
    return sorted(sample(range(mini, maxi + 1), quantity))


# __________________________________________________ Третє завдання __________________________________________________ #

def san_numb(raw_numbers):
    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)


def normalize_phone(phone_number):
    print(phone_number)
    # Видалення всіх символів, крім цифр і '+'
    sanitized = re.sub(r'[^\d]', '', phone_number).strip()
    # Перевірка наявності міжнародного коду і корекція
    if len(sanitized) > 12 or len(sanitized) < 10:
        p, p_name = find_country_by_phone(sanitized)
        if p:
            return f'This phone belongs to {p_name}'
        else:
            print('Invalid phone number')
            return 'Invalid phone number'
    else:
        if not sanitized.startswith('+'):
            print(1)
            if sanitized.startswith('380'):
                print(2)
                sanitized = '+' + sanitized
            else:
                if len(sanitized) != 10:
                    p, p_name = find_country_by_phone(sanitized)
                    if p:
                        return f'This phone belongs to {p_name}'
                    else:
                        print('Invalid phone number')
                        return 'Invalid phone number'


                else:
                    sanitized = '+38' + sanitized
                    print(3)
        print(sanitized)
        return sanitized


def find_country_by_phone(phone_number):
    # phone_number = "+" + re.sub(r'\D', '', phone_number).strip()
    phone_number = '+' + phone_number
    print(phone_number)
    for country in phone_list:
        if phone_number.startswith(country["dial_code"]):
            country_name = country['name']
            print(f"The phone number belongs to {country_name}")


            return country, country_name
    return None


# ________________________________________________ Четверте завдання ________________________________________________ #

users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]


def get_upcoming_birthdays(users):
    today = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        print(user["birthday"])
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_until_birthday = (birthday_this_year - today).days

        if 0 <= days_until_birthday <= 7:
            # Adjust for weekends
            if birthday_this_year.weekday() >= 5:  # Saturday or Sunday
                days_to_add = 7 - birthday_this_year.weekday()
                birthday_this_year += timedelta(days=days_to_add)

            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays


if __name__ == '__main__':
    # get_days_from_today("2021-10-09")
    # p = get_numbers_ticket(min_val, max_val, quantity)
    #    sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
    #    print("Нормалізовані номери телефонів для SMS-розсилки:", sanitized_numbers)
    #    print(sanitized_numbers)
    # upcoming_birthdays = get_upcoming_birthdays(users)
    # print("Список привітань на цьому тижні:", upcoming_birthdays)
    print_hi()
