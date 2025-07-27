import os

def print_order(product_name, product_price):
    text = f"New Order:\n{product_name} - €{product_price:.2f}\n\n"

    # For now, simulate the print (for testing without printer)
    print(text)

    # If using an actual printer (like Epson):
    # os.system(f'echo "{text}" | lp -d Epson_TM_T20III')
