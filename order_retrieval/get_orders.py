import os
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

def get_new_orders():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to ebay.yaml
        config_path = os.path.join(current_dir, 'ebay.yaml')
        
        print(f"Using config file: {config_path}")
        
        api = Trading(config_file=config_path, domain='api.ebay.com')
        response = api.execute('GetOrders', {'NumberOfDays': 30, 'OrderStatus': 'All'})
        return response.dict()
    except ConnectionError as e:
        print(f"Error connecting to eBay API: {e}")
        print(f"Error details: {e.response.dict()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    orders = get_new_orders()
    if orders and 'OrderArray' in orders and 'Order' in orders['OrderArray']:
        order_list = orders['OrderArray']['Order']
        if isinstance(order_list, list):
            print(f"Retrieved {len(order_list)} orders")
            for order in order_list:
                print(f"Order ID: {order['OrderID']}")
                print(f"Order Status: {order['OrderStatus']}")
                print(f"Total: {order['Total']['value']} {order['Total']['_currencyID']}")
                print("---")
        elif isinstance(order_list, dict):
            print("Retrieved 1 order")
            print(f"Order ID: {order_list['OrderID']}")
            print(f"Order Status: {order_list['OrderStatus']}")
            print(f"Total: {order_list['Total']['value']} {order_list['Total']['_currencyID']}")
        else:
            print("No orders found")
    else:
        print("Failed to retrieve orders or no orders were found")
        if orders:
            print("API Response:")
            print(orders)