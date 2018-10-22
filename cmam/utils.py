# -*- coding: utf-8 -*-


def date_handler(obj):
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    else:
        raise TypeError
