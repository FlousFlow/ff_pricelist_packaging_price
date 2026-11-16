from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_price(self, product, quantity, uom, **kwargs):
        """Interpret a fixed price in the rule's selected UoM.

        Odoo's default implementation treats ``fixed_price`` as a price in the
        product's base UoM, even when the rule is restricted to another UoM.
        For packaging rules this makes, for example, 50 per dozen become 600.
        Keep standard behavior for rules without a selected UoM and convert a
        packaging price only when the rule explicitly defines one.
        """
        self and self.ensure_one()
        if self.compute_price == "fixed" and self.uom_id:
            uom = uom or product._get_main_uom()
            price = self.uom_id._compute_price(self.fixed_price, uom)
            if self.applied_on == "0_product_variant":
                extra_price = self.env.context.get("no_variant_attributes_price_extra", 0)
            else:
                extra_price = product._get_attributes_extra_price()
            extra_price = self.uom_id._compute_price(extra_price, uom)
            extra_price = self._convert_price(extra_price, product.currency_id, **kwargs)
            return price + extra_price
        return super()._compute_price(product, quantity, uom, **kwargs)
