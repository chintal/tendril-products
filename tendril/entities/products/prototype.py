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

from tendril.utils import log
from tendril.costing.breakup import HierachicalCostingBreakup
from tendril.entities.prototypebase import PrototypeBase

from tendril.utils.versions import FeatureUnavailable

from tendril.schema.products import ProductDefinition

try:
    from tendril.boms.outputbase import CompositeOutputBom
except ImportError:
    CompositeOutputBom = None

try:
    from tendril.entityhub.modules import get_prototype_lib
except ImportError:
    get_prototype_lib = None

from .warranty import WarrantyMixin

logger = log.get_logger(__name__, log.INFO)


class ProductPrototype(PrototypeBase, WarrantyMixin):
    def __init__(self, fpath):
        super(ProductPrototype, self).__init__()
        self._cards = None
        self._cables = None
        self._boms = None
        self._obom = None
        self._sourcing_errors = None
        self._indicative_cost_hierarchical_breakup = None
        self._load_product_info(fpath)

    def _load_product_info(self, fpath):
        self._definition = ProductDefinition(fpath)
        self._definition.validate()
        self._validation_errors.add(self._definition.validation_errors)

    _definition_elements = (
        'name',
        'core',
        'calibformat',
        'line',
        'info',
        'card_listing',
        'cable_listing',
        'pricing'
    )

    _pricing_elements = (
        'base_price',
        'apply_discount',
        'discounts',
        'effective_price',
        'iqty',
        'extended_price',
        'tax',
        'taxes',
        'total_price',
        'included_addons',
    )

    def __getattr__(self, item):
        if item in self._definition_elements:
            return getattr(self._definition, item)
        elif item in self._pricing_elements:
            return getattr(self.pricing, item)
        else:
            raise AttributeError("{1} does not have attribute {0}"
                                 "".format(item, self.__class__))

    @property
    def ident(self):
        return self._definition.ident

    @property
    def desc(self):
        return self._definition.info.desc

    def _get_status(self):
        return self._definition.info.status

    @property
    def labels(self):
        return self._definition.labels.content

    def labelinfo(self, sno):
        return self.info.labelinfo(sno)

    # @property
    # def calibformat(self):
    #     # TODO Get the calibformat object instead
    #     return self._calibformat

    @property
    def module_listing(self):
        return {k: v for k, v in (self.card_listing + self.cable_listing)}

    # Libraries
    @staticmethod
    def _get_modules(parsed_listing):
        if get_prototype_lib is None:
            raise FeatureUnavailable('Product Structure',
                                     'get_prototype_lib')
        rval = []
        pl = get_prototype_lib()
        for cname in parsed_listing:
            rval.append((pl[cname[0]], cname[1]))
        return rval

    @property
    def cards(self):
        if self._cards is None:
            self._cards = self._get_modules(self.card_listing)
        return self._cards

    @property
    def cables(self):
        if self._cables is None:
            self._cables = self._get_modules(self.cable_listing)
        return self._cables

    # BOMs
    def _construct_components(self):
        components = []
        for card, qty in self.cards:
            for i in range(qty):
                components.append(card)
        for cable, qty in self.cables:
            for i in range(qty):
                components.append(cable)
        return components

    def _construct_bom(self):
        if CompositeOutputBom is None:
            raise FeatureUnavailable('Product BOMs',
                                     'CompositeOutputBOM')
        self._boms = [x.obom for x in self._construct_components()]
        self._obom = CompositeOutputBom(self._boms, name=self.ident)
        self._obom.collapse_wires()

    @property
    def boms(self):
        if self._boms is None:
            self._construct_bom()
        return self._boms

    @property
    def obom(self):
        if self._obom is None:
            self._construct_bom()
        return self._obom

    # @property
    # def bom(self):
    #     # TODO Check if this is actually necessary.
    #            COBOM (obom) might be enough?
    #     raise NotImplementedError

    # Costing
    @property
    def indicative_cost(self):
        return self.obom.indicative_cost

    @property
    def sourcing_errors(self):
        if self._sourcing_errors is None:
            self._sourcing_errors = self.obom.sourcing_errors
        return self._sourcing_errors

    @property
    def indicative_cost_breakup(self):
        return self.obom.indicative_cost_breakup

    @property
    def indicative_cost_hierarchical_breakup(self):
        if self._indicative_cost_hierarchical_breakup is None:
            breakups = [x.indicative_cost_hierarchical_breakup
                        for x in self._construct_components()]
            if len(breakups) == 1:
                return breakups[0]
            rval = HierachicalCostingBreakup(self.ident)
            for breakup in breakups:
                rval.insert(breakup.name, breakup)
            self._indicative_cost_hierarchical_breakup = rval
        return self._indicative_cost_hierarchical_breakup

    # Instantiation
    # def get_component_snos(self):
    #     pass

    # Housekeeping
    @property
    def _changelogpath(self):
        raise NotImplementedError

    def _reload(self):
        raise NotImplementedError

    def _register_for_changes(self):
        raise NotImplementedError

    def _validate(self):
        pass

    def reset(self):
        self.pricing.reset()

    def __repr__(self):
        return "<ProductPrototype {0}>".format(self.ident)
