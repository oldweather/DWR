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

# Functions for DWR station names.

custom_names={
              'BLACKSODPOINT'    : 'Blacksod Point',
              'BOSCOMBEDOWN'     : 'Boscombe Down',
              'BUTTOFLEWIS'      : 'Butt of Lewis',
              'CAPEWRATH'        : 'Cape Wrath',
              'CAPGRISNEZ'       : 'Cap Gris-Nez',
              'CASTLEARCHDALE'   : 'Castle Archdale',
              'CLACTONONSEA'     : 'Clacton-on-Sea',
              'EASTFORTUNE'      : 'East Fortune',
              'FLAMBOROUGHHEAD'  : 'Flamborough Head',
              'FORTWILLIAM'      : 'Fort William',
              'HARTLANDPOINT'    : 'Hartland Point',
              'HOLMSLEYSOUTH'    : 'Holmsley South',
              'LITTLERISSINGTON' : 'Little Rissington',
              'LOCHRANNOCH'      : 'Loch Rannoch',
              'LOUGHFOYLE'       : 'Lough Foyle',
              'MALINHEAD'        : 'Malin Head',
              'MULLOFGALOWAY'    : 'Mull of Galloway',
              'NORTHWEALD'       : 'North Weald',
              'PEMBROKEDOCK'     : 'Pembroke Dock',
              'POINTAYRE'        : 'Point Ayre',
              'PORTADELGADA'     : 'Ponta Delgada',
              'PORTLANDBILL'     : 'Portland Bill',
              'ROCHESPOINT'      : 'Roches Point',
              'ROSSONWYE'        : 'Ross-on-wye',
              'SPURNHEAD'        : 'Spurn Head',
              'SQUIRESGATE'      : 'Squires Gate',
              'STABBSHEAD'       : 'St. Abb''s Head',
              'STEVAL'           : 'St. Eval',
              'STMAWGAN'         : 'St. Mawgan',
              'SULESKERRY'       : 'Sule Skerry',
              'SULLOMVOE'        : 'Sullom Voe',
              'SUMBURGHHEAD'     : 'Sumburgh Head',
              'THEHELDER'        : 'Den Helder',
              'THELIZARD'        : 'The Lizard',
              'THORNEYISLAND'    : 'Thorney Island',
              'UPPERHEYFORD'     : 'Upper Heyford',
              'WESTFREUGH'       : 'West Freugh',
              'WESTRAYNHAM'      : 'West Raynham'
}

def pretty_name(name):
    """Convert station names from DATAFORMAT to Print Format.

    The station names included in the DWR data files are in all caps and contain no spaces. This function maps them to a readable format - so FORTWILLIAM becomes 'Fort William'. 

    Args:
        name (:obj:`str`): Name as in data file (e.g. 'CAPGRISNEZ')

    Returns:
        :obj:`str`: Name in readable format (e.g. 'Cap Gris-Nez')

    """
    name=name.upper()
    if name in custom_names:
        return custom_names[name]
    return name.capitalize()
