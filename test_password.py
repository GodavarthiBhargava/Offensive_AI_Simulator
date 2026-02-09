from backend.password_engine import simulate_password_attack

# Test 1: Simple password
print("Test 1: password='password', algorithm='MD5'")
result = simulate_password_attack("password", "MD5")
print(f"Result: {result}\n")

# Test 2: Numeric password
print("Test 2: password='123', algorithm='MD5'")
result = simulate_password_attack("123", "MD5")
print(f"Result: {result}\n")

# Test 3: Context-aware
print("Test 3: password='john', username='john', algorithm='MD5'")
result = simulate_password_attack("john", "MD5", username="john")
print(f"Result: {result}\n")
