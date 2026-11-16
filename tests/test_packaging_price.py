from odoo.tests.common import TransactionCase


class TestPackagingPricelistPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_uom = cls.env.ref("uom.product_uom_unit")
        cls.uom_category = cls.product_uom.category_id
        cls.dozen_uom = cls.env["uom.uom"].create({
            "name": "Test Dozen",
            "category_id": cls.uom_category.id,
            "uom_type": "bigger",
            "factor": 12,
            "rounding": 0.01,
        })
        cls.product_tmpl = cls.env["product.template"].create({
            "name": "Packaging Price Test Product",
            "uom_id": cls.product_uom.id,
            "list_price": 5,
        })
        cls.product = cls.product_tmpl.product_variant_id
        cls.pricelist = cls.env["product.pricelist"].create({"name": "Packaging Test"})
        cls.rule = cls.env["product.pricelist.item"].create({
            "pricelist_id": cls.pricelist.id,
            "product_id": cls.product.id,
            "uom_id": cls.dozen_uom.id,
            "compute_price": "fixed",
            "fixed_price": 50,
        })

    def test_fixed_price_is_per_selected_packaging(self):
        price, rule_id = self.pricelist._get_product_price_rule(
            self.product, quantity=1, uom=self.dozen_uom
        )
        self.assertEqual(rule_id, self.rule.id)
        self.assertEqual(price, 50)

    def test_base_unit_does_not_use_packaging_rule(self):
        price, rule_id = self.pricelist._get_product_price_rule(
            self.product, quantity=1, uom=self.product_uom
        )
        self.assertFalse(rule_id)
        self.assertEqual(price, 5)
