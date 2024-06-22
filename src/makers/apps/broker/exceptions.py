class BrokerBaseException(Exception):
    """
    Базовый класс ошибки при работе с Брокером
    """
    default_text = "Проблема с брокером"

    def __init__(self, text: str = None, detail: str = None):
        if text is None:
            text = self.default_text
        self.text = text
        if detail:
            self.detail = detail.lower()
            self.text = f"{self.text}: {self.detail}"

    def __str__(self):
        return self.text
