# -*- encoding: utf-8 -*-
#
# OpenERP Commission - Manages sales agents' commissions
# Copyright (C) 2010-Today Thibaut DIRLIK <thibaut.dirlik@gmail.com>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from osv import osv, fields
from tools.translate import _

class ProductSupplierInfo(osv.osv):

    """
    We override the supplier info model to add the commission per supplier.
    """

    _inherit = 'product.supplierinfo'
    _columns = {
        'commission' : fields.float(_('Commission (%)'), required=True,
                                    help=_('Defines the commissions earned by the salesman.')),
    }
    _defaults = {
        'commission' : 0.0,
    }

ProductSupplierInfo()