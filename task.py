# Catalog with product prices
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": (200, 10),  # Cart total exceeds $200, apply $10 flat discount
    "bulk_5_discount": (10, 0.05),  # Quantity of any single product exceeds 10 units, apply 5% discount
    "bulk_10_discount": (20, 0.1),  # Total quantity exceeds 20 units, apply 10% discount
    "tiered_50_discount": (30, 15, 0.5)  # Total quantity exceeds 30 units and any single product quantity greater than 15, apply 50% discount on quantities above 15
}

# Fees
gift_wrap_fee = 1  # Gift wrap fee per unit
shipping_fee_per_package = 5  # Shipping fee per package
items_per_package = 10  # Number of items that can be packed in one package

# Function to calculate the total amount for a product based on its quantity and discount rules
def calculate_product_total(product_name, quantity):
    price = catalog[product_name]
    total = price * quantity
    
    for rule, rule_details in discount_rules.items():
        if rule == "bulk_5_discount" and quantity > rule_details[0]:
            total -= total * rule_details[1]
        elif rule == "tiered_50_discount" and quantity > rule_details[1]:
            discountable_quantity = quantity - rule_details[1]
            total -= discountable_quantity * price * rule_details[2]
    
    return total

# Function to calculate the shipping fee based on the total quantity
def calculate_shipping_fee(quantity):
    return (quantity // items_per_package) * shipping_fee_per_package

# Function to calculate the total amount payable for the order
def calculate_order_total(product_quantities, gift_wrapped_products):
    subtotal = 0
    discount_applied = None
    discount_amount = 0
    gift_wrap_fee_total = 0

    for product_name, quantity in product_quantities.items():
        total_amount = calculate_product_total(product_name, quantity)
        subtotal += total_amount

        if product_name in gift_wrapped_products:
            gift_wrap_fee_total += quantity * gift_wrap_fee
        

    for rule, rule_details in discount_rules.items():
        if rule == "flat_10_discount" and subtotal > rule_details[0]:
            discount_applied = rule
            discount_amount = rule_details[1]
        elif rule == "bulk_10_discount" and sum(product_quantities.values()) > rule_details[0]:
            discount_applied = rule
            discount_amount = subtotal * rule_details[1]

    shipping_fee = calculate_shipping_fee(sum(product_quantities.values()))

    total = subtotal - discount_amount + gift_wrap_fee_total + shipping_fee
    print("subtotal=",subtotal)
    print("discount amount=",discount_amount)
    print("shipping fee=",shipping_fee)
    print("gift_wrap_fee_total=",gift_wrap_fee_total)
    print("total=",total)

    return subtotal, discount_applied, discount_amount, gift_wrap_fee_total, shipping_fee, total

# Main program
product_quantities = {}
gift_wrapped_products = []

# Getting quantity and gift wrap information for each product
for product_name in catalog.keys():
    quantity = int(input(f"Enter the quantity for {product_name}: "))
    product_quantities[product_name] = quantity

    gift_wrapp = input(f"Is {product_name} to be wrapped as a gift? (y/n): ")
    if gift_wrapp.lower() == "y":
        print({product_name},"wrapped")
calculate_order_total(product_quantities,gift_wrapped_products) 
