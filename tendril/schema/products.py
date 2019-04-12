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
from tendril.entities.products import infoclasses

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class LabelDeclaration(NakedSchemaObject):
    def elements(self):
        e = super(LabelDeclaration, self).elements()
        e.update({
            'desc': self._p(('desc',), required=True),
            'type': self._p(('type',), required=True),
        })
        return e

    def __repr__(self):
        return "<LabelDeclaration {0}, {1}>" \
               "".format(self.desc, self.type)


class LabelListing(SchemaObjectList):
    _objtype = LabelDeclaration


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


class SimpleBomListing(SchemaObjectList):
    _objtype = None


class SimpleCardListing(SimpleBomListing):
    _objtype = SimpleBomLineCard


class SimpleCableListing(SimpleBomListing):
    _objtype = SimpleBomLineCable


class ProductDefinition(SchemaControlledYamlFile):
    supports_schema_name = 'ProductDefinition'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, *args, **kwargs):
        super(ProductDefinition, self).__init__(*args, **kwargs)

    def elements(self):
        e = super(ProductDefinition, self).elements()
        e.update({
            'name':        self._p(('name',),   required=True),
            'core':        self._p(('derive_sno_from',),),
            'calibformat': self._p(('calibformat',),),
            'cards':       self._p(('cards',),  parser=SimpleCardListing),
            'cables':      self._p(('cables',), parser=SimpleCableListing),
            'labels':      self._p(('labels',), parser=LabelListing),
            'line':        self._p(('productinfo', 'line',), required=True),
            'info':        self._p(('productinfo',),         parser=self._get_info_instance),
        })
        return e

    def _get_info_instance(self, content):
        return infoclasses.get_product_info_class(
            self.line, content, parent=self, vctx=self._validation_context
        )

    def schema_policies(self):
        policies = super(ProductDefinition, self).schema_policies()
        policies.update({})
        return policies

    @property
    def ident(self):
        return self.name

    def __repr__(self):
        return "<ProductDefinition {0}>".format(self.ident)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('ProductDefinition', ProductDefinition,
                        doc="Schema for Tendril Product Definition Files")