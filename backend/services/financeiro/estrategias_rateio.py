from decimal import Decimal


class RateioAutomatico:
    def calcular(self, total, pessoas, valor_fixo):
        base, sobra = divmod(int(total * 100), pessoas)
        return [Decimal(base + (i < sobra)) / 100 for i in range(pessoas)]


class RateioFixo:
    def calcular(self, total, pessoas, valor_fixo):
        return [Decimal(valor_fixo or 0)] * pessoas


ESTRATEGIAS = {"auto": RateioAutomatico(), "fixo": RateioFixo()}
