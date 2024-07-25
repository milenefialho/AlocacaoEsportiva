from datetime import timedelta
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='replace')
def replace(value, args):
    """ Replace all values of arg[0] with arg[1] in the string """
    old, new = args
    return value.replace(old, new)


@register.filter(name='dataAjuste')
def dataAjuste(value):
    """ Replace all occurrences of old with new in the string """
    # data = timezone.localtime(value)
    return value.strftime('%d/%m/%Y %H:%M:%S')


@register.filter(name='hrsSaida')
def hrsSaida(value, args):
    """ Replace all occurrences of old with new in the string """
    # print('-'*30)
    # print('value = ', value)
    # print('args = ', args)
    # data = timezone.localtime(value)
    novo = args + timedelta(hours=int(value))
    # print('novo = ', novo)
    # print('-'*30)
    return dataAjuste(novo)


@register.filter(name='formatarDataJustInput')
def formatarDataJustInput(value):
    """ Return a formatted date """
    return '' if (value is None) else value.strftime('%Y-%m-%d')

@register.filter(name='formatarDataInput')
def formatarDataInput(value):
    """ Return a formatted date """
    return '' if (value is None) else value.strftime('%Y-%m-%d %H:%M')