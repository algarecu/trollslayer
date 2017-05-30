#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2017
# Álvaro García-Recuero, algarecu@gmail.com
#
# This file is part of the Trollslayer framework
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses>.

"""
Utils

Created on'17/06/15'
__author__='algarecu'
__email__='algarecu@gmail.com'

"""

#Taken from https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class bcolors:
    RED='\033['
    OKGREEN='\033[92m'
    WARNING='\033[93m'
    BGGREEN='\033[42m'      #backgroundtogreen
    BGWHITE='\033[47m'      #backgroundtowhite
    FGBLACK='\033[30m'      #foregroundtoblack
    FGRED='\033[31m'        #foregroundtored
    BGBLACK='\033[40m'      #backgroundtoblack
    FGGREEN='\033[32m'      #foregroundtogreen
    BGWHITEFGBLUE='\033[91m'  #backgroundtowhite&foregroundtoblue
    HEADER='\033[95m'       #backgroundtowhite&fgtomagenta
    BGYELLOW='\033[43m'     #backgroundtoyellow
    FGBLUE='\033[34m'       #foregroundtoblue
    FGMAGENTA='\033[35m'    #foregroundtomagenta
    FGCYAN='\033[36m'       #foregroundtocyan
    BGBLUE='\033[44m'       #backgroundtoblue
    BGRED='\033[41m'        #backgroundtored
    FGWHITE='\033[37m'      #foregroundtowhite
    BGCYAN='\033[45m'       #backgroundtocyan
    BLINK='\033[5m'         #terminaltoblink
    NORMAL='\033[m'         #terminaltonormal
    UNDERLINE='\033[4m'     #terminaltounderline
    NOUNDERLINE='\033[24m'  #terminaltocancelunderline
    REVERSE='\033[7m'       #terminaltoreversevideo
    BGMAGENTA='\033[45m'    #backgroundtomagenta
    BOLD='\033[1m'          #bold
    ENDC='\033[0m'
