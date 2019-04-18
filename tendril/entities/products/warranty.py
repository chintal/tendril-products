# Copyright (C) 2019 Chintalagiri Shashank
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


import six
from numbers import Number
from tendril.utils.types.time import DateSpan
from tendril.schema.base import NakedSchemaObject


class WarrantyTerms(NakedSchemaObject):
    def elements(self):
        e = super(WarrantyTerms, self).elements()
        e.update({
            'std': self._p('std',  parser=DateSpan),
            '_ext': self._p('ext', parser=DateSpan, required=False, default='0yr'),
            '_amc': self._p('amc', parser=DateSpan, required=False, default='0yr')
        })
        return e

    @property
    def ext_max(self):
        return self._ext

    @property
    def amc_max(self):
        return self._amc

    def __repr__(self):
        return "<{0}>\n Standard: {1}\n Optional (Max): " \
               "\n   Extended Warranty: {2} \n   AMC: {3}" \
               "".format(self.__class__.__name__,
                         self.std, self.ext_max, self.amc_max)


class WarrantyMixin(object):
    def _warranty_apply(self, wtype, years, **kwargs):
        if self.pricing.get_included_addon(wtype):
            raise ValueError(
                "Warranty of type {0} already added to this product. Remove it "
                "before trying to add it again".format(wtype.upper())
            )
        if isinstance(years, six.string_types):
            years = DateSpan(years)
        elif isinstance(years, Number):
            years = DateSpan('{0} years'.format(years))

        w_max = getattr(self.warranty_terms, "{0}_max".format(wtype))
        if years > w_max:
            raise ValueError(
                "Maximum warranty of type {0} allowed for this product is {1}."
                "".format(wtype.upper(), w_max)
            )

        self.pricing.include_addon(wtype, unit=DateSpan('1yr'), qty=years, **kwargs)

    def add_extended_warranty(self, years, **kwargs):
        self._warranty_apply('ext', years, **kwargs)

    def add_amc(self, years, **kwargs):
        self._warranty_apply('amc', years, **kwargs)

    @property
    def warranty_terms(self):
        return self.info.warranty
