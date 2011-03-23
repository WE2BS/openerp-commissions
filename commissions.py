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

class Commission(osv.osv):

    """
    Represents a commission. These objects are create when the user clicks on 'Make commissions',
    after the sale order has been confirmed. The invoice is created with the wizard.
    """

    def is_invoiced(self, cursor, user_id, ids, field_name, arg, context=None):

        """
        Returns True if the commissions has an invoice line.
        """

        commissions = self.browse(cursor, user_id, ids, context=context)
        result = {}

        for commission in commissions:
            result[commission.id] = commission.invoice_line_id.id and True or False

        return result

    _name = 'commissions.commission'
    _columns = {
        'order_line_id' : fields.many2one('sale.order.line', _('Sale Order Line'), required=True, ondelete='RESTRICT'),
        'order_id' : fields.many2one('sale.order', string=_('Order'), required=True),
        'order_customer_id' : fields.related('order_id', 'partner_id', type='many2one', relation="res.partner", string=_('Customer')),
        'vendor_id' : fields.related('order_id', 'user_id', type='many2one', relation='res.users', string=_('Vendor')),
        'product_id' : fields.related('order_line_id', 'product_id', type='many2one', relation='product.product', string=_('Product')),
        'product_uom' : fields.related('order_line_id', 'product_uom', type='many2one', relation='product.uom', string=_('UoM')),
        'product_qty' : fields.related('order_line_id', 'product_uom_qty', type='float', string=_('Quantity')),
        'commission' : fields.related('order_line_id', 'commission', type='float', string=_('Commission (%)')),
        'commission_amount' : fields.related('order_line_id', 'commission_amount', type='float', string=_('Amount')),
        'supplier_id' : fields.related('order_line_id', 'supplier_id', type='many2one', relation='res.partner', string=_('Supplier')),
        'invoice_line_id' : fields.many2one('account.invoice.line', _('Invoice line'), ondelete='SET NULL'),
        'invoice_id' : fields.related('invoice_line_id', 'invoice_id', type="many2one", relation='account.invoice', string= _('Invoice')),
        'invoiced' : fields.function(is_invoiced, type='boolean', method=True, string=_('Invoiced')),
    }

Commission()
