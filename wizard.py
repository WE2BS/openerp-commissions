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

class CreateCommissionsInvoice(osv.osv_memory):

    """
    This wizard generates an invoice for the selected commissions items. 
    """

    _name = 'commissions.invoice.wizard'
    _columns = {
        'supplier_id' : fields.many2one('res.partner', _('Supplier')),
    }

CreateCommissionsInvoice()