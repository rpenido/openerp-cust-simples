from openerp.osv import fields, osv
import datetime

class res_partner(osv.osv):
	_inherit = "res.partner"
	_order = "visit_order"
	
	def payment_term_func(self, cr, uid, ids, field_name, field_value, arg, context=None):
		records = self.browse(cr, uid, ids)
		result = {}
		for r in records:
			result[r.id] = r.property_payment_term.name
		return result
	
	def last_visit_today(self, cr, uid, ids, field_name, field_value, arg, context=None):
		today = datetime.date.today()
		records = self.browse(cr, uid, ids)
	        result = {}
        	for r in records:
            		result[r.id] =  r.last_visit > today.isoformat()

	        return result

	def total_orders_today(self, cr, uid, ids, field_name, field_value, arg, context=None):
		today = datetime.date.today()
		records = self.browse(cr, uid, ids)
		result = {}
		for r in records:
			orders_ids = self.pool.get('sale.order').search(cr, uid, [('partner_id', '=', r.id), ('date_order', '>=', today.isoformat())], context=context)
			result[r.id] = 0;
			order_list = self.pool.get('sale.order').browse(cr, uid, orders_ids)
			for so in order_list:
				result[r.id] += so.amount_total;
		return result;

	def total_orders_last_week(self, cr, uid, ids, field_name, field_value, args, context=None):
		ref_date = datetime.date.today() - datetime.timedelta(days=6);
		records = self.browse(cr, uid, ids)
		result = {}
		for r in records:
			orders_ids = self.pool.get('sale.order').search(cr, uid, [('partner_id', '=', r.id), ('date_order', '>=', ref_date.isoformat())], context=context)
			result[r.id] = 0;
			order_list = self.pool.get('sale.order').browse(cr, uid, orders_ids)
			for so in order_list:
				result[r.id] += so.amount_total;
		return result;	

	_columns = {
		'code': fields.char('Codigo', size=10),
		'orders_last_week': fields.function( total_orders_last_week, type='float', method=True, string="Pedidos semana"),
		'visit_order': fields.integer('Ordem'),
		'history': fields.text('Historico'),
		'paym_term': fields.function( payment_term_func, type='char', method=True, string="Metod. de Pagto")
		
	}

res_partner()