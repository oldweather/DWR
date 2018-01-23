# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
"""
Functions for DWR station names.
"""

custom_names={'SUMBURGHHEAD'  : 'Sumburgh Head',
              'FORTWILLIAM'   : 'Fort William',
              'MALINHEAD'     : 'Malin Head',
              'BLACKSODPOINT' : 'Blacksod Point',
              'SPURNHEAD'     : 'Spurn Head',
              'THEHELDER'     : 'Den Helder',
              'ROCHESPOINT'   : 'Roches Point',
              'CAPGRISNEZ'    : 'Cap Gris-Nez',
              'PORTLANDBILL'  : 'Portland Bill',
              'PORTADELGADA'  : 'Ponta Delgada'}

def pretty_name(name):
    name=name.upper()
    if name in custom_names:
        return custom_names[name]
    return name.capitalize()
