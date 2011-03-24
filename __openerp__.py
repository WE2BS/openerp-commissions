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

{
    "name": "Commission",
    "version": "0.1",
    "author": "UIDE/WE2BS",
    "category": "Generic Modules/Sales & Purchases",
    "website": "https://github.com/thibautd/openerp-commision",
    "description":
        """
        This module let you manage commisions of your salesman.
        """,
    "depends": ["base", "account", "sale"],
    "init_xml": [],
    "demo_xml": [],
    "update_xml": ['security/groups.xml', 'views/product.xml', 'views/sale.xml', 'workflow/sale.xml',
                   'views/commissions.xml', 'wizards/commissions_invoice.xml'],
    "active": False,
    "test": [],
    "installable": True
}
