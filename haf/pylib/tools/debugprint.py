import os, time, datetime, sys, inspect

def class_debug(origin_func):
    '''
    类方法的调试装饰器
    '''
    def wrapper(self, *args, **kwargs):
        try:
            
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception:
            return 'an Exception raised.'
    return wrapper
 
def debug(origin_func):
    '''
    非类方法的调试装饰器
    '''
    def wrapper(*args, **kwargs):
        try:
            u = origin_func(*args, **kwargs)
            return u
        except Exception:
            return 'an Exception raised.'
    return wrapper