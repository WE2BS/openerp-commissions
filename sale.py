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

class SaleOrder(osv.osv):

    """
    We override the sale.order model to remove / add some things :
        - Remove the 'Generate invoice' button
        - Add a 'generate commission invoice' button
        - Add a 'Total commission' field
        - Total price will take commission into account
    """

    def get_total_commissions(self, cursor, user_id, ids, field_name, arg, context=None):

        """
        Compute the total amount of commissions on this sale order.
        """

        orders = self.browse(cursor, user_id, ids, context=context)
        result = {}
        
        for order in orders:
            total_commission = 0
            for line in order.order_line:
                total_commission += line.commission_amount
            result[order.id] = total_commission

        return result

    def get_default_logistic(self, cursor, user_id, context=None):

        if context is None:
            return False

        return context.get('only_commissions', False)

    def are_commissions_created(self, cursor, user_id, ids, field_name, arg, context=None):

        """
        A boolean functional field which contains TRUE if all commissions have been generated.
        """

        orders = self.browse(cursor, user_id, ids, context=context)
        result = {}

        for order in orders:
            valid_lines_ids = self.pool.get('sale.order.line').search(cursor, user_id,
                [('order_id', '=', order.id), ('commission_amount', '>', 0), ('supplier_id', '!=', False)])
            result[order.id] = len(valid_lines_ids) == len(order.commissions)

        return result

    def action_make_commissions(self, cursor, user_id, ids, context=None):

        """
        Generate the commissions associated to this order.
        """

        order = self.browse(cursor, user_id, ids[0], context=context)
        lines = order.order_line

        for line in lines:
            if line.commission_amount <= 0:
                continue
            if not line.supplier_id.id:
                continue
            exists = False # TODO: May have a better way to check this
            for commission in order.commissions:
                if commission.order_line_id.id == line.id:
                    exists = True
            if exists:
                continue
            self.pool.get('commissions.commission').create(cursor, user_id, {
                'order_line_id' : line.id,
                'order_id' : order.id,
            })

        return True

    def action_done(self, cursor, user_id, ids, context=None):

        """
        In the case of a 'No logistic' order, we mark all the order lines as being invoiced when the order is done.
        """

        orders = self.browse(cursor, user_id, ids, context=context)

        for order in orders:
            if order.disable_logistic:
                self.pool.get('sale.order.line').write(
                    cursor, user_id, [line.id for line in order.order_line], {'invoiced' : True}, context=context)

        self.write(cursor, user_id, ids, {'state' : 'done'}, context=context)
        
        return True

    def action_show_commissions(self, cursor, user_id, ids, context=None):

        """
        Show the generated commissions object.
        """

        search_view_id = self.pool.get('ir.ui.view').search(cursor, user_id,
            [('model', '=', 'commissions.commission'),('type','=','search')])[0]

        return {
            'name' : _('Commissions'),
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'res_model' : 'commissions.commission',
            'search_view_id' : search_view_id,
            'context' : {'search_default_order_id' : ids[0]},
            'nodestroy' : True, # See https://bugs.launchpad.net/openobject-client/+bug/651784
        }

    _inherit = 'sale.order'
    _name = 'sale.order'

    _columns = {
        'disable_logistic' : fields.boolean(_('No logistic'), help=_(
            'Check this if you are a Sale Agent who does\'t need picking/invoicing/etc')),
        'commissions' : fields.one2many('commissions.commission', 'order_id', _('Commissions')),
        'total_commissions' : fields.function(get_total_commissions, method=True, type='float', string=_('Total commissions')),
        'are_commissions_created' : fields.function(are_commissions_created, method=True, type='boolean'),
    }

    _defaults = {
        'disable_logistic' : get_default_logistic,
        'are_commissions_created' : False,
    }

SaleOrder()

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

        if not supplier_id: # Use the default supplier if none specified
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

    def get_commission_amount(self, cursor, user_id, ids, field_name, arg, context=None):

        """
        Returns the amount of the commission.
        """

        lines = self.browse(cursor, user_id, ids, context=context)
        result = {}
        for line in lines:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * line.product_uom_qty
            result[line.id] = price * (line.commission / 100.0)
        return result

    def supplier_id_change(self, cursor, user_id, ids, product_id, supplier_id):

        """
        When the supplier change, we update the commission on the product based on the supplier.
        """

        result = {}

        if product_id:
            if supplier_id:
                supplier_id, commission = self.get_supplier_and_commission(cursor, user_id, product_id, supplier_id)
            else:
                commission = 0
            result['value'] = {'commission' : commission}
        return result

    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    _columns = {
        'commission' : fields.float(_('Commission (%)')),
        'commission_amount' : fields.function(get_commission_amount, string= _('Commission amount'), type='float', method=True),
        'supplier_id' : fields.many2one('res.partner', _('Supplier'),
            help=_('Specify the supplier you want to use. This will change the commission value.')),
    }

SaleOrderLine()
