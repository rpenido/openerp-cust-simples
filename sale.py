from openerp.osv import fields, osv
import tools

class sales_order(osv.Model):
  _inherit = "sale.order"
  def _prepare_invoice(self, cr, uid, order, lines, context=None):
    res = super(sales_order, self)._prepare_invoice(cr, uid, order, fields, context=context)
    #res['comment'] += 'Teste123'
    return res
sales_order()
