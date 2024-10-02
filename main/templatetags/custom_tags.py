from django import template

register = template.Library()

@register.filter
def split_first_word(value):
    """Split the first word and return a tuple (first_word, rest_of_the_string)"""
    words = value.split(' ', 1)  # Split on the first space
    if len(words) == 1:
        return words[0], ''  # If there's only one word, return it and an empty string
    return words[0], words[1]
