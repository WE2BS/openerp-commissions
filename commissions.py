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
from tools.tranlate import _

STATES = (
    ('waiting', 'Waiting'),
    ('invoiced', 'Invoiced'),
)

class Commission(osv.osv):

    """
    Represents the commission associated with a sale.order.line. 
    """

    _name = 'commission.commission'
    _columns = {
        'line_id' : fields.many2one('sale.order.line', _('Sale Order Line'), required=True),
        'order_id' : fields.related('line_id', 'order_id', relation='sale.order', type='many2one', string=_('Sale Order')),
        'commission' : fields.related('line_id', 'commission', type='float', string=_('Commission (%)')),
        'commission_amount' : fields.related('line_id', 'commission_amount', type='float', string=_('Commission')),
        'supplier' : fields.related('line_id', 'supplier_id', relation='res.partner', type='many2one', string=_('Supplier')),
        'state' : fields.selection(STATES, _('State')),
        'invoice_id' : fields.related('invoice_line_id', 'invoice_id', relation='account.invoice', string=_('Invoice')),
        'invoice_line_id' : fields.many2one('account.invoice.line', _('Invoice Line')),
    }

Commission()
