# FlousFlow Pricelist Packaging Prices

Odoo 20 addon that interprets a fixed pricelist price as the price of the
selected packaging/unit of measure. For example, a fixed price of 50 with
`Dozen` selected remains 50 per dozen instead of being converted from the
product's base unit into 600.

## Behavior

- Rules without a selected packaging/UoM keep standard Odoo behavior.
- Rules with a selected packaging/UoM use that UoM as the price basis.
- The rule still applies only when the sales line uses the selected UoM.
- Explicit sales-line UoM choices are preserved; the addon does not force a
  packaging choice on every order.

## Installation

Install `ff_pricelist_packaging_price` from the Odoo Apps menu or with the Odoo
command line on an Odoo 20 database.

## Compatibility

- Odoo 20.0
- License: LGPL-3
- Dependencies: `product`, `sale`
