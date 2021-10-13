from datetime import date  # todo зачем создавать папку внутри которой один файл с тем же названием? Если в будущем нужно будет разделять на модули создашь новую папку, пока это оверхед
import re  # todo неверно поставлены импорты

from django.core.validators import BaseValidator


class BirthdayValidatorPhone(BaseValidator):
    message = 'Действует ограничение по возрасту - 18+'

    def compare(self, age, valid_age):
        birthday = age
        today = date.today()
        data = today.year - birthday.year - (
                (today.month, today.day) < (birthday.month, birthday.day))
        return data < valid_age


class RegexValidatorPhone(BaseValidator):
    message = 'Некорректный номер телефона'

    def compare(self, phone, valid_phone):
        return not re.match(valid_phone, phone)


birthday_validator = BirthdayValidatorPhone(limit_value=18)
phone_validator = RegexValidatorPhone(limit_value=r'^(\+(7|1)|8)[0-9]{9}')
