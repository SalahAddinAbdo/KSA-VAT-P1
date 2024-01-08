import frappe
from frappe.utils import get_url_to_list
from frappe import _
import json
frappe.init(site="hoda-dev.erpgulf.com")
frappe.connect()
from frappe.utils.data import  get_time

def get_tax_amount(item_code, account_head, doctype, parent, net_amount):
	if doctype == "Sales Invoice":
		tax_doctype = "Sales Taxes and Charges"

	elif doctype == "Purchase Invoice":
		tax_doctype = "Purchase Taxes and Charges"

	item_wise_tax_detail = frappe.get_value(
		tax_doctype,
		{"docstatus": 1, "parent": parent, "account_head": account_head},
		"item_wise_tax_detail",
	)
	
	tax_amount = 0
	if item_wise_tax_detail and len(item_wise_tax_detail) > 0:
		item_wise_tax_detail = json.loads(item_wise_tax_detail)
		tax_percentage=item_wise_tax_detail.get(item_code,[0,0])[0]
		for key, value in item_wise_tax_detail.items():
			# print(tax_percentage)
			if key == item_code:
				tax_amount = net_amount*tax_percentage/100
				break
	print(tax_amount)
	return tax_amount


def get_tax_data_for_each_vat_setting(vat_setting, doctype):
	"""
	(KSA, {filters}, 'Sales Invoice') => 500, 153, 10 \n
	calculates and returns \n
	total_taxable_amount, total_taxable_adjustment_amount, total_tax"""
	# from_date = filters.get("from_date")
	# to_date = filters.get("to_date")

	from_date = "2020/02/02"
	to_date = "2025/02/02"

	# Initiate variables
	total_taxable_amount = 0
	total_taxable_adjustment_amount = 0
	total_tax = 0
	# Fetch All Invoices
	from_date = "2020/02/02"
	to_date = "2025/02/02"
	invoices = frappe.get_all(
		doctype,
		filters={"docstatus": 1, "posting_date": ["between", [from_date, to_date]]},
		fields=["name", "is_return"],
	)
	for invoice in invoices:
		invoice_items = frappe.get_all(
			f"{doctype} Item",
			filters={
				"docstatus": 1,
				"parent": invoice.name,
				"item_tax_template": vat_setting.item_tax_template,
			},
			fields=["item_code", "net_amount"],
		)

		for item in invoice_items:
			# Summing up total taxable amount
			if invoice.is_return == 0:
				total_taxable_amount += item.net_amount

			if invoice.is_return == 1:
				total_taxable_adjustment_amount += item.net_amount

			# Summing up total tax
			total_tax += get_tax_amount(item.item_code, vat_setting.account, doctype, invoice.name, item.net_amount)

	return total_taxable_amount, total_taxable_adjustment_amount, total_tax


def append_data(data, title, amount, adjustment_amount, vat_amount, company_currency):
	"""Returns data with appended value."""
	data.append(
		{
			"title": _(title),
			"amount": amount,
			"adjustment_amount": adjustment_amount,
			"vat_amount": vat_amount,
			"currency": company_currency,
		}
	)

# print(frappe.session.user)

company = "AHMED A ALHASHIM SONS CO & PARTNER (ALHODA)"
company_currency = frappe.get_cached_value("Company", company, "default_currency")
# print(company_currency)

if frappe.db.exists("KSA VAT Setting", company) is None:
		url = get_url_to_list("KSA VAT Setting")
		# frappe.msgprint(_('Create <a href="{}">KSA VAT Setting</a> for this company').format(url))
	
data = []

append_data(data, "VAT on Sales", "", "", "", company_currency)

grand_total_taxable_amount = 0
grand_total_taxable_adjustment_amount = 0
grand_total_tax = 0

ksa_vat_setting = frappe.get_doc("KSA VAT Setting", "AHMED A ALHASHIM SONS CO & PARTNER (ALHODA)")
for vat_setting in ksa_vat_setting.ksa_vat_sales_accounts:
	(
		total_taxable_amount,
		total_taxable_adjustment_amount,
		total_tax,
	) = get_tax_data_for_each_vat_setting(vat_setting, "Sales Invoice")
	# print(vat_setting.parent)
	# Adding results to data
	append_data(
		data,
		vat_setting.title,
		total_taxable_amount,
		total_taxable_adjustment_amount,
		total_tax,
		company_currency,
	)

	grand_total_taxable_amount += total_taxable_amount
	grand_total_taxable_adjustment_amount += total_taxable_adjustment_amount
	grand_total_tax += total_tax


# Sales Grand Total
append_data(
	data,
	"Grand Total",
	grand_total_taxable_amount,
	grand_total_taxable_adjustment_amount,
	grand_total_tax,
	company_currency,
)




print(data)