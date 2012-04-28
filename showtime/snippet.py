# coding: utf8
# Author: Jakub Krajniak <jkrajniak@gmail.com>
# Licence: LGPL
# Web: https://github.com/MrTheodor/django-snippets
#
# ShowTime template tag
#
# Usage:
#   1. Define in settings dict TIME_BLOCK with names of block that has to be
#   shown on certain time:
#       TIME_BLOCK = {
#           'block1': {
#               'from_date': datetime.datetime(2012, 04, 28, 13, 48),
#               'to_date': datetime.datetime(2012, 04, 30, 13, 48),
#               'show': True
#           }
#       }
#   
#   2. In template use it in such way:
#       
#       {% showtime block1 %}
#           content that will be displayed between 2012-04-28 13:48 and 2012-04-30
#           13:48
#       {% else %}
#           content that will be displayed before and after that time
#       {% endshowtime %}
#
#  There is also the possibility to do it in the reverse form by using option
#  'show'.


import datetime
from django import template
from django.template import NodeList

from django.conf import settings
register = template.Library()

def do_showtime(parser, token):
    nodelist_true = parser.parse(('else', 'endshowtime', ))
    
    try:
        tag_name, block_name = token.split_contents()
        block_name = block_name.replace('"', '').replace("'", '')
    except:
        tag_name = token.split_contents()
    
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endshowtime', ))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()


    return DisplayShowTime(nodelist_true, nodelist_false, block_name)

class DisplayShowTime(template.Node):
    def __init__(self, true_nodelist, false_nodelist, block_name):
        self.true_nodelist = true_nodelist
        self.false_nodelist = false_nodelist
        self.block_name = block_name

    def render(self, context):
        from_date = None
        to_date = None
        default_show = None

        cmp_only_hour = False
        current_datetime = datetime.datetime.now()

        show = False

        try:
            settings_block = settings.TIME_BLOCK[self.block_name]
            from_date = settings_block['from_date']
            to_date = settings_block['to_date']
            
            if isinstance(from_date, datetime.time):
                current_datetime = current_datetime.time()
                if isinstance(to_date, datetime.datetime):
                    to_date = to_date.time()
            default_show = settings_block.get('show', True) # True/False
        except:
            show = True
        
        if current_datetime >= from_date and current_datetime <= to_date:
            show = default_show
        else:
            show = not default_show
        

        if show:
            output_true = self.true_nodelist.render(context)
            return output_true
        else:
            output_false = self.false_nodelist.render(context)
            return output_false

register.tag('showtime', do_showtime)
