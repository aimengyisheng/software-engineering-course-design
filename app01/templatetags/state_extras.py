from django import template

register = template.Library()


# 可以成功识别state[obj.id]
@register.filter('f')
def f(h, key):
    return h[key]
