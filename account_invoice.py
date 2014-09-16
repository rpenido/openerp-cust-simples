# encoding: utf-8
from openerp.osv import fields, osv

class account_invoice(osv.osv):
	_inherit = 'account.invoice'
	_columns = {
		'partner_legal_name': fields.related('partner_id', 'legal_name', type='string', string="Razão Social"),
	}

