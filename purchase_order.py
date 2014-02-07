# coding=UTF-8
from osv import fields, osv
import tools

class purchase_order(osv.osv):
  _inherit = "purchase.order"
  _columns = {
    'serie': fields.selection((('s1','Série 1'), ('p10','p10')),'Série', required=True)
  }
purchase_order()
