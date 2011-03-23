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
        
        for commission in commissions:
            suppliers_commissions.setdefault(commission.supplier_id, list())
            suppliers_commissions[commission.supplier_id].append(commission)

        for supplier, commissions in suppliers_commissions.iteritems():
            # For each supplier, we generate an invoice with the specified commissions.
            # We also write the the invoice_line_id to commissions objects.
            invoice_id = self.pool.get('account.invoice').create(cursor, user_id, {
                'type' : 'out_invoice',
                'state' : 'draft',
                'date_invoice' : datetime.date.today(),
                'partner_id' : supplier.id,
                'address_invoice_id' : commissions.order_id.partner_invoice_id.id,
                'account_id' : supplier.property_account_receivable.id,
            }, context=context)
            suppliers_invoices[supplier] = invoice_id

        return {
            'name' : 'Commissions Invoices',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'res_model' : 'account.invoice',
            'res_id' : suppliers_invoices.values(),
        }

CreateCommissionsInvoice()
