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

STATES = (
    ('draft', _('Draft')),
    ('invoiced', _('Invoiced')),
)

class Commission(osv.osv_memory):

    """
    Represents a commission. These objects are create when the user clicks on 'Make commissions',
    after the sale order has been confirmed.
    """

    _name = 'commissions.commission'
    _columns = {
        'order_line_id' : fields.many2one('sale.order.line', _('Sale Order Line'), ondelete='CASCADE'),
        'order_id' : fields.related('order_line_id', 'order_id', relation='sale.order', string=_('Sale Order')),
        'product_id' : fields.related('order_line_id', 'product_id', relation='product.product', string=_('Product')),
        'commission' : fields.related('order_line_id', 'commission', string=_('Commission (%)')),
        'commission_amount' : fields.related('order_line_id', 'commission_amount', string=_('Amount')),
        'supplier_id' : fields.related('order_line_id', 'supplier_id', relation='res.partner', string=_('Supplier')),
        'state' : fields.selection(STATES, _('State')),
    }

Commission()
