from osv import fields, osv
import tools

class nf_series_report(osv.osv):
  _name = "nf_series.report"
  _auto = False
  _columns = {
    'serie': fields.char('Serie', size=128, readonly=True),
    'codigo': fields.char('Codigo', size=128, readonly=True),
    'produto': fields.char('Produto', size=128, readonly=True),
    'quantidade': fields.float('Quantidade', readonly=True),
  }

  def init(self,cr):
    tools.sql.drop_view_if_exists(cr, 'nf_series_report')
    cr.execute("""CREATE VIEW nf_series_report AS(
	select
		ROW_NUMBER() OVER (ORDER BY serie) as id,
		serie,
		codigo,
		produto,
		sum(qtd) as quantidade
	from
		(select
			se.code as serie,
			pp.default_code as codigo,
			pp.name_template as produto,
			-il.quantity as qtd
		from
			account_invoice i,
			account_invoice_line il,
			product_product pp,
			l10n_br_account_document_serie se
		where
			i.id = il.invoice_id
			and pp.id = il.product_id
			and se.id = i.document_serie_id
			and i.state in ('sefaz_export', 'paid')
		
		union
		
		select
			po.serie as serie,
			pp.default_code as codigo,
			pp.name_template as produto,
			product_qty as qtd
		from
			purchase_order po,
			stock_picking sp,
			stock_move sm,
			product_product pp
		where
			po.id = sp.purchase_id
			and sp.id = sm.picking_id
			and sm.product_id = pp.id
			and sp.state = 'done'
		) foo
	group by
		serie,
		codigo,
		produto
  )""")

nf_series_report()
