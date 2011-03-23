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

import datetime
import math

from osv import osv, fields
from tools.translate import _

class CreateCommissionsInvoice(osv.osv_memory):

    """
    This wizard generates an invoice for the selected commissions items. 
    """

    _name = 'commissions.invoice.wizard'
    _columns = {
        'supplier_id' : fields.many2one('res.partner', _('Supplier')),
    }

    def execute(self, cursor, user_id, ids, context=None):

        """
        Generare an invoice per supplier for all selected commissions.
        """

        if context is None:
            raise osv.except_osv(_('Error'), _('Invalid context. Try to refresh the view.'))

        commissions = self.pool.get('commissions.commission').browse(
            cursor, user_id, context['active_ids'], context=context)

        suppliers_commissions = {}
        suppliers_invoices = {}

        try:
            product_id = self.pool.get('ir.model.data').read(cursor, user_id,
            self.pool.get('ir.model.data').search(cursor, user_id,
                [('module', '=', 'commissions'),('name', '=', 'commission_product')],context=context
            ), context=context)[0]['res_id']
            product = self.pool.get('product.product').browse(cursor, user_id, product_id, context=context)
        except KeyError, e:
            raise osv.except_osv(_('Error'), _('You removed the Commission product. Update the module.'))
        
        for commission in commissions:
            suppliers_commissions.setdefault(commission.supplier_id, list())
            suppliers_commissions[commission.supplier_id].append(commission)

        for supplier, commissions in suppliers_commissions.iteritems():
            # Generate invoice
            invoice_id = self.pool.get('account.invoice').create(cursor, user_id, {
                'type' : 'out_invoice',
                'state' : 'draft',
                'date_invoice' : datetime.date.today(),
                'partner_id' : supplier.id,
                'address_invoice_id' : commissions[0].order_id.partner_invoice_id.id,
                'account_id' : supplier.property_account_receivable.id,
            }, context=context)
            suppliers_invoices[supplier] = invoice_id

            # Generate invoice line - One customer / line
            invoice_lines = {}
            for commission in commissions:
                invoice_lines.setdefault(commission.order_customer_id, list())
                invoice_lines[commission.order_customer_id].append(commission)
            for customer, commissions in invoice_lines.iteritems():
                self.pool.get('account.invoice.line').create(cursor, user_id, {
                    'name' : customer.name,
                    'invoice_id' : invoice_id,
                    'product_id' : product.id,
                    'account_id' : product.property_account_income.id,
                    'price_unit' : sum([commission.commission_amount for commission in commissions]),
                    'quantity' : 1,
                    'origin' : commission.order_id.name,
                }, context=context)

        view_id = self.pool.get('ir.ui.view').read(cursor, user_id,
            self.pool.get('ir.ui.view').search(
                cursor, user_id, [('name', '=', 'account.invoice.form')] ,context=context),
            context=context)[0]['id']
        view_xmlid = self.pool.get('ir.ui.view').get_xml_id(cursor, user_id, [view_id], context=context)[view_id]

        return {
            'name' : 'Commissions Invoices',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'context' : {'form_view_ref' : view_xmlid},
            'res_model' : 'account.invoice',
            'domain' : [('id', 'in', suppliers_invoices.values())],
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
        }

CreateCommissionsInvoice()
