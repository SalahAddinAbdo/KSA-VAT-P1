import frappe
from frappe.utils import get_url_to_list
from frappe import _
frappe.init(site="dev.erpgulf.com")
frappe.connect()


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

print(frappe.session.user)

company = "My Company"
company_currency = frappe.get_cached_value("Company", company, "default_currency")
print(company_currency)

if frappe.db.exists("KSA VAT Setting", company) is None:
		url = get_url_to_list("KSA VAT Setting")
		# frappe.msgprint(_('Create <a href="{}">KSA VAT Setting</a> for this company').format(url))
		print("insidata")
print("reached")

data = []
# company = filters.get("company")
company_currency = frappe.get_cached_value("Company", company, "default_currency")

append_data(data, "VAT on Sales", "", "", "", "SAR")
append_data(data, "VAT on Sales", "100", "1000", "10000", "SAR")
append_data(data, "VAT on Sales", "110", "1100", "11000", "SAR")

print(data)