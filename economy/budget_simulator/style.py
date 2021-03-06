#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <wins@kasonnara.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Style constants of the budget simulator application
"""


import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

HEADER_STYLE = {
    "background-color": "#f8f9fa",
    "padding": "1rem",
    }

SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    }

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    }

LABEL_SETTING_BOOTSTRAP_COL = {
    "int": (7, 4),
    "bool": (10, 1),
    "default": (6, 6),
    }

TOOLTIPS_STYLE = {
    'max-width': "90%",
    'text-align': "left",
    }

"""Constants used by the build_parameter_selector function to set bootstrap columns grid widths of the label and 
the interactive component for each possible UI parameter type"""
