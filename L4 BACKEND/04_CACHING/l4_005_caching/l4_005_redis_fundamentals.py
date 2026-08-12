import redis

# -----------------------------------------------------------------------------
# Create Redis Connection
# -----------------------------------------------------------------------------

redis_client = redis.Redis(

    host='localhost',
    port=6379,
    decode_responses=True,
)

# -----------------------------------------------------------------------------
# Set Cache Value
# -----------------------------------------------------------------------------

def l4_005SetCustomers() -> None:
    """Store customer name in Redis."""

    redis_client.set(                  # --> is equivalent to Redis CLI: SET customer:1:name Ahmed
        "customer:1:name",       # --> KEY customer:1:name
        "Ahmed"                  # --> VALUE Ahmed
    )

    redis_client.set(
        "customer:2:name",
        "Lokesh"
    )

    print("Customers cached successfully.")

# -----------------------------------------------------------------------------
# Get Cache Value
# -----------------------------------------------------------------------------

def l4_005GetCustomer() -> None:
    """Read customer name from Redis."""

    customer_1 = redis_client.get("customer:1:name")      # --> is equivalent to GET customer:1:name
    customer_2 = redis_client.get("customer:2:name")      # --> is equivalent to GET customer:2:name

    print(customer_1)
    print(customer_2)

# -----------------------------------------------------------------------------
# Delete Cache Value
# -----------------------------------------------------------------------------

def l4_005DeleteCustomer() -> None:
    """Delete customer value from Redis."""

    redis_client.delete(                  # --> removes the key, returns None
        "customer:1:name"
    )

    print("Customer cache deleted.")

# -----------------------------------------------------------------------------
# Set Customer With Expiry
# -----------------------------------------------------------------------------

def l4_005SetCustomerWithExpiry() -> None:
    """Store customer name with an expiry time."""

    redis_client.set(
        "customer:3:name",
        "Sara",
        ex=10
    )


    print("Customer cached for 10 seconds.")

# -----------------------------------------------------------------------------
# Check Customer TTL
# -----------------------------------------------------------------------------

def l4_005CheckCustomerTtl() -> None:
    """Check remaining expiry time."""

    ttl = redis_client.ttl(
        "customer:3:name"
    )

    print(f"TTL: {ttl} seconds")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_005GetCustomer()


