global_count = 0


def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


def add_item_explicit(item, order):
    order.append(item)
    return order


def make_order_adder():
    order = []
    def add(item):
        order.append(item)
        return order.copy()
    return add


def calculate_bill(amount, gst_rate=0.05):
    gst = amount * gst_rate
    return amount + gst, gst


def parameter_examples():
    print("positional:", calculate_bill(100.0))
    print("keyword:", calculate_bill(amount=200.0, gst_rate=0.05))
    print("default:", calculate_bill(50.0))


def scope_examples():
    message = "local"
    print("local:", message)

    def update_global():
        global global_count
        global_count += 1
        return global_count
    update_global()
    print("global:", global_count)

    def make_counter():
        count = 0
        def increment():
            nonlocal count
            count += 1
            return count
        return increment
    counter = make_counter()
    print("nonlocal:", counter(), counter())


def main():
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print("buggy defaults:", add_item_buggy.__defaults__)
    customers = [add_item("Tea"), add_item("Coffee"), add_item("Vada")]
    print("three independent customers:", customers)
    explicit_order = []
    print("explicit list:", add_item_explicit("Idli", explicit_order))
    closure_order = make_order_adder()
    print("closure order:", closure_order("Tea"), closure_order("Vada"))
    parameter_examples()
    scope_examples()
    total, gst = calculate_bill(500.0, gst_rate=0.05)
    print(f"total={total:.2f}, GST={gst:.2f}")

if __name__ == "__main__":
    main()
