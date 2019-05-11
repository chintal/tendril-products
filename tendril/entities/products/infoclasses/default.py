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
from tendril.entities.products.warranty import WarrantyTerms


class ProductInfo(NakedSchemaObject):
    def __init__(self, *args, **kwargs):
        self._parent = kwargs.pop('parent')
        super(ProductInfo, self).__init__(*args, **kwargs)

    def elements(self):
        e = super(ProductInfo, self).elements()
        e.update({
            'line':           self._p('line'),
            'ptype':          self._p('type',           required=False),
            'desc':           self._p('desc'),
            'version':        self._p('version',        required=False),
            'status':         self._p('status',         required=False, default='Undefined'),  # noqa
            'is_hardware':    self._p('is_hardware',    required=False, default=False),  # noqa
            'is_software':    self._p('is_software',    required=False, default=False),  # noqa
            'is_firmware':    self._p('is_firmware',    required=False, default=False),  # noqa
            'is_third_party': self._p('is_third_party', required=False, default=False),  # noqa
            'is_consumable':  self._p('is_consumable',  required=False, default=False),  # noqa
            'warranty':       self._p('warranty',       required=False, parser=WarrantyTerms)
        })
        return e

    @property
    def ident(self):
        return self._parent.ident

    def labelinfo(self, sno):
        return sno, {}
