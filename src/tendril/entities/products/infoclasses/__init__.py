#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2018 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import importlib


def get_product_info_class(line, infodict, *args, **kwargs):
    try:
        modname = 'tendril.entities.products.infoclasses.{0}'.format(line)
        mod = importlib.import_module(modname)
        func = getattr(mod, 'get_info_class')
        instance = func(infodict, *args, **kwargs)
    except ImportError:
        from .default import ProductInfo
        instance = ProductInfo(infodict, *args, **kwargs)
    return instance
