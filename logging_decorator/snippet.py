# coding: utf8
# Author: Jakub Krajniak <jkrajniak@gmail.com>
# Licence: LGPL
# Web: https://github.com/MrTheodor/django-snippets
#
# logging_decorator - log all exceptions from e.g. views. Useful when it
# is combined with @transaction.commit_manually decorator. 
#
# Example:
#  
#  @transaction.commit_manually
#  @logging_decorator
#  def foobar(request):
#    ...

import traceback
import logging

def logging_decorator(view_fn):
  
  def inner(*args, **kwargs):
      try:
        return view_fn(*args, **kwargs)
      except Exception as e:
        log = traceback.format_exc()
        logging.exception(log)
        raise e
  
  return inner
