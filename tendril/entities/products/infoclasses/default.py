# Copyright (C) 2015-2019 Chintalagiri Shashank
#
# This file is part of Tendril.
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
"""
This file is part of tendril
See the COPYING, README, and INSTALL files for more information
"""

from tendril.schema.base import NakedSchemaObject


class ProductInfo(NakedSchemaObject):
    def __init__(self, *args, **kwargs):
        self._parent = kwargs.pop('parent')
        super(ProductInfo, self).__init__(*args, **kwargs)

    @property
    def ident(self):
        return self._parent.ident

    def labelinfo(self, sno):
        return sno, {}

    @property
    def line(self):
        # TODO Setup validation
        return self._raw['line']

    @property
    def ptype(self):
        # TODO Setup validation
        return self._raw['type']

    @property
    def desc(self):
        # TODO Setup validation
        return self._raw['desc']

    @property
    def version(self):
        # TODO Setup validation
        try:
            return self._raw['version']
        except KeyError:
            return None

    @property
    def status(self):
        # TODO Setup validation
        try:
            return self._raw['status']
        except KeyError:
            return 'Undefined'
