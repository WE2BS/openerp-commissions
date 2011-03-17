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

class SaleOrderLine(osv.osv):

    """
    We override this model to add a commission and supplier fields. 
    """

    def get_suppliers(self, cursor, user_id, ids, field_name, arg, context=None):

        """
        Returns the suppliers associated to the product.
        """

        products = [line.product_id for line in self.browse(cursor, user_id, ids, context=context) if line.product_id.id]
        result = {}

        for product in products:
            result[product.id] = [supplierinfo.name.id for supplierinfo in product.seller_ids]

        return result

    def get_supplier_and_commission(self, cursor, user_id, product_id, supplier_id=None):

        """
        Returns a 2-Tuple of the default supplier and its commission for the specified product_id.
        """

        product = self.pool.get('product.product').browse(cursor, user_id, product_id)
        commission = 0

        if supplier_id is None: # Use the default supplier if none specified
            supplier_id = product.seller_id.id

        for supplier_info in product.seller_ids:
            if supplier_id == supplier_info.name.id:
                commission = supplier_info.commission
                return (supplier_id, commission)

        return (False, 0)

    def product_id_change(self, cursor, user_id, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):

        """
        Overrided method. When the product change, we update the domain of 'suppliers_ids', and set a default supplier.
        """
        
        result = super(SaleOrderLine, self).product_id_change(cursor, user_id, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag)
        suppliers = []
        default_supplier = False
        commission = 0
        
        if product:
            product_object = self.pool.get('product.product').browse(cursor, user_id, product)
            product_suppliers = [info.name for info in product_object.seller_ids]
            suppliers = [supplier.id for supplier in product_suppliers]
            default_supplier, commission = self.get_supplier_and_commission(cursor, user_id, product)

        result['value'].update( {'supplier_id': default_supplier, 'commission' : commission} )
        result['domain'].update({
            'supplier_id' : [('id', 'in', suppliers)],
        })

        return result

    def supplier_id_change(self, cursor, user_id, ids, product_id, supplier_id):

        """
        When the supplier change, we update the commission on the product based on the supplier.
        """

        result = {}

        if product_id and supplier_id:
            supplier_id, commission = self.get_supplier_and_commission(cursor, user_id, product_id, supplier_id)
            result['value'] = {'commission' : commission}
        return result

    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    _columns = {
        'commission' : fields.float(_('Commission (%)')),
        'supplier_id' : fields.many2one('res.partner', _('Supplier'),
            help=_('Specify the supplier you want to use. This will change the commission value.')),
    }

SaleOrderLine()