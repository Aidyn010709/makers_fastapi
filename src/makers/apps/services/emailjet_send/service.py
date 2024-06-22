from mailjet_rest import Client
from loguru import logger

from makers.config.settings import settings
from makers.apps.commons.constants import CONSTANTS


def send_activation_code(*, activation_code: str, email: str, name: str):
    """
    activation_code: this is activated code
    email: this os email client where send activation code
    name: this is client name
    """
    mailjet = Client(
        auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version="v3.1"
    )
    data = {
        "Messages": [
            {
                "From": {
                    "Email": CONSTANTS.SENDER_EMAIL,
                    "Name": CONSTANTS.SENDER_NAME,
                },
                "To": [{"Email": email, "Name": name}],
                "Subject": "Поздравляем! Вы успешно зарегистрировались!",
                "TextPart": CONSTANTS.MAILJET_GREETING,
                "HTMLPart": f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta http-equiv="X-UA-Compatible"content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Document</title></head><body style="font-family: "Manrope", sans-serif"><divstyle="width: 600px; height: 800px; font-family: "Manrope", sans-serif"><div style="width: 80%; margin: auto"><img width="150px"src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-iu0_prbzA-mit9nCCc1LbSeaVOT1Rw7X6g&usqp=CAU"alt="logo"/><h1 style="margin: 0">Подтвердите вашу почту</h1><p style="font-size:18px">До конца регистрации на сайте <a href="https://online-course.makers.com/" target="_blank">Makers online course</a> осталось совсем чуть-чуть</p><a href="{settings.URL_FRONTEND_ACTIVATION_CODE}/{activation_code}" target="_blank"><button style="width: 30%;height: 40px;background-color: #2b59c3;border: none;outline: none;border-radius: 5px;cursor: pointer;color: #ffffff;">Подтвердить почтовый адрес</button></a><a href="http://localhost:5173/success/{activation_code}" target="_blank"><button style="width: 30%;height: 40px;background-color: #2b59c3;border: none;outline: none;border-radius: 5px;cursor: pointer;color: #ffffff;">Test</button></a></div></div></body></html>',
            }
        ]
    }

    result = mailjet.send.create(data=data)
    logger.info(f"Email sent with result: {result.json()}")


def send_reset_password(*, generate_activation_code: str, email: str, name: str):
    """
    generate_activation_code: this is generated activation code for verified
    email: this is email client where send activation code
    name: this is client name
    """
    mailjet = Client(
        auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version="v3.1"
    )

    data = {
        "Messages": [
            {
                "From": {
                    "Email": CONSTANTS.SENDER_EMAIL,
                    "Name": CONSTANTS.SENDER_NAME,
                },
                "To": [{"Email": email, "Name": name}],
                "Subject": "Сброс пароля Juniors.dev",
                "TextPart": CONSTANTS.MAILJET_GREETING,
                "HTMLPart": f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta http-equiv="X-UA-Compatible"content="IE=edge" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Document</title></head><body style="font-family: "Manrope", sans-serif"><divstyle="width: 600px; height: 800px; font-family: "Manrope", sans-serif"><div style="width: 80%; margin: auto"><img width="150px"src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-iu0_prbzA-mit9nCCc1LbSeaVOT1Rw7X6g&usqp=CAU"alt="logo"/><h1 style="margin: 0">Приветствуем, {name}</h1><p style="font-size:16px">Необходимо восстановить пароль учетной записи.</p><p style="font-size:16px">Нажмите на кнопку ниже, чтобы изменить пароль.</p><a href="{settings.URL_FRONTEND_RESET_PASSWORD}/{generate_activation_code}" target="_blank"><button style="width: 30%;height: 40px;background-color: #2b59c3;border: none;outline: none;border-radius: 5px;cursor: pointer;color: #ffffff;">Изменить пароль</button></a></div></div></body></html>',
            }
        ]
    }

    result = mailjet.send.create(data=data)
    logger.info(f"Email sent with result: {result.json()}")
