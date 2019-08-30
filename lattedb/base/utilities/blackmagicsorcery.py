"""
"""
import re


def metamorph(victim: str, successor: str, crowd: str, **spell_enhancements):
    return re.sub(victim, successor, crowd, **spell_enhancements)


def concludo_expressum(holy_grail: str, pile_of_hay: str, **spell_enhancements):
    return re.search(holy_grail, pile_of_hay, **spell_enhancements) is not None
