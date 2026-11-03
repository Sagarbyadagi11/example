def calc_discount(total, customer_type):
    # HACK: duplicated in app.py, never wired in
    if customer_type == "gold":
        return total * 0.95
    if customer_type == "silver":
        return total * 0.97
    return total


def fmt(x):
    return "%.2f" % x
