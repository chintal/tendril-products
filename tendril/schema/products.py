#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
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


from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile
from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList
from tendril.schema.prototype import LabelListing
from tendril.pricing.structured import StructuredUnitPrice
from tendril.entities.products import infoclasses
from tendril.entities.products import calibformats

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class SimpleBomLine(NakedSchemaObject):
    _itemtype = None

    def elements(self):
        e = super(SimpleBomLine, self).elements()
        e.update({
            self._itemtype: self._p((self._itemtype,), required=True),
            'qty':          self._p(('qty',),          required=True, parser=int),
        })
        return e

    @property
    def ident(self):
        return getattr(self, self._itemtype)

    def __repr__(self):
        return "<{0} {1}, {2}>".format(self.__class__.__name__,
                                       self.ident, self.qty)


class SimpleBomLineCard(SimpleBomLine):
    _itemtype = 'card'


class SimpleBomLineCable(SimpleBomLine):
    _itemtype = 'cable'


class SimpleBomItemDecl(NakedSchemaObject):
    def elements(self):
        e = super(SimpleBomItemDecl, self).elements()
        e.update({
            '_ident': self._p(None, required=True),
        })
        return e

    @property
    def qty(self):
        return 1

    @property
    def ident(self):
        return self._ident

    def __repr__(self):
        return "<SimpleBomItemDecl {0}, {1}>".format(self.ident, self.qty)


class SimpleBomListing(SchemaObjectList):
    _objtype = None


class SimpleCardListing(SimpleBomListing):
    _objtype = [(dict, SimpleBomLineCard),
                ('default', SimpleBomItemDecl)]


class SimpleCableListing(SimpleBomListing):
    _objtype = [(dict, SimpleBomLineCable),
                ('default', SimpleBomItemDecl)]


class ProductDefinition(SchemaControlledYamlFile):
    supports_schema_name = 'ProductDefinition'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, *args, **kwargs):
        super(ProductDefinition, self).__init__(*args, **kwargs)

    def elements(self):
        e = super(ProductDefinition, self).elements()
        e.update({
            'name':        self._p('name'),
            'core':        self._p('derive_sno_from', required=False),
            'calibformat': self._p('calibformat',     required=False, parser=self._get_calibformat),
            'cards':       self._p('cards',           required=False, parser=SimpleCardListing, default={}),
            'cables':      self._p('cables',          required=False, parser=SimpleCableListing, default={}),
            'labels':      self._p('labels',          required=False, parser=LabelListing, default={}),
            'line':        self._p(('productinfo', 'line',)),
            'info':        self._p('productinfo',     parser=self._get_info_instance),
            'pricing':     self._p('pricing',         required=False, parser=StructuredUnitPrice)
        })
        return e

    def _get_info_instance(self, content):
        return infoclasses.get_product_info_class(
            self.line, content, parent=self, vctx=self._validation_context
        )

    def _get_calibformat(self, content):
        return calibformats.get_calibformat(content)

    def schema_policies(self):
        policies = super(ProductDefinition, self).schema_policies()
        policies.update({})
        return policies

    @property
    def version(self):
        return self.info.version

    @property
    def ident(self):
        if self.info.version:
            return "{0} v{1}".format(self.name, self.info.version)
        else:
            return self.name

    def _parse_listing(self, listing):
        return [(i.ident, i.qty) for i in listing]

    @property
    def card_listing(self):
        return self._parse_listing(self.cards)

    @property
    def cable_listing(self):
        return self._parse_listing(self.cables)

    def __repr__(self):
        return "<ProductDefinition {0}>".format(self.ident)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('ProductDefinition', ProductDefinition,
                        doc="Schema for Tendril Product Definition Files")
