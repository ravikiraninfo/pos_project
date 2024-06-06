# -*- coding: utf-8 -*-
###############################################################################
#
#   Cybrosys Technologies Pvt. Ltd.
#
#   Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#   Author: Aslam A K( odoo@cybrosys.com )
#
#   You can modify it under the terms of the GNU AFFERO
#   GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#   You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#   (AGPL v3) along with this program.
#   If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import models, fields


class AccountPayment(models.Model):
    """
    This class inherits from the 'account.payment' model to add specific
    features and behavior related to printing checks and handling payment
    information. It overrides the 'print_checks' method to provide a custom
    wizard view for selecting and formatting cheque printing options.
    """
    _inherit = 'account.payment'

    def print_checks(self):
        """
        Overriding print_checks button to generate a wizard view to print
        cheque by selecting a cheque print format.
        """
        # if self.payment_method_line_id.payment_method_id.name == 'Checks':
        #     cheque_date = self.date
        # elif self.payment_method_line_id.payment_method_id.name == 'PDC':
        #     cheque_date = self.effective_date

        return {
            'name': "Cheque Format",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cheque.types',
            'target': 'new',
            'context': {
                'default_partner_id': self[0].partner_id.id,
                'default_cheque_amount_in_words': self[0].currency_id.amount_to_text(sum(self.mapped("amount"))),
                'default_cheque_date': fields.Datetime.now(),
                'default_cheque_amount': sum(self.mapped("amount")),
                'default_check_number': self[0].check_number,
                'default_payment_id': len(self) == 1 and self.id or False,
            }
        }
