def mask_dollar(amount):
    # Convert to string
    str_amount = str(amount)

    # Check if amount has decimal point
    if '.' in str_amount:
        dollars, cents = str_amount.split('.')
    else:
        dollars = str_amount
        cents = '00'

    # Mask all but the last 4 digits
    masked_dollars = ''.join(['*' if i < len(dollars) - 4 else dollars[i] for i in range(len(dollars))])

    # Return the masked dollar amount
    return f'{masked_dollars}.{cents}'

