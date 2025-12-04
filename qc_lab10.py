# Quantum Computing Lab 10
# Diffie–Hellman Key Exchange with Man-in-the-Middle Attack
# Alice, Bob, Tom (Attacker)

# Step 1: Shared prime and generator
p = 23                      # Prime number
g = 5                       # Generator

print("Public parameters:")
print("Prime p =", p)
print("Generator g =", g)
print()

# Step 2: Private keys
a = 6                       # Alice private key
b = 15                      # Bob private key
t = 9                       # Tom private key

# Step 3: Genuine public keys
A_real = pow(g, a, p)       # g^a mod p
B_real = pow(g, b, p)       # g^b mod p

print("REAL public keys (before interception):")
print("Alice public key A =", A_real)
print("Bob public key B =", B_real)
print()

# Step 4: Tom intercepts and replaces keys
T_public = pow(g, t, p)

print("Tom intercepts and replaces keys:")
print("Alice receives FAKE B =", T_public)
print("Bob receives FAKE A =", T_public)
print()

# Step 5: Alice computes shared key thinking it is Bob
shared_A_T = pow(T_public, a, p)

# Step 6: Bob computes shared key thinking it is Alice
shared_B_T = pow(T_public, b, p)

# Step 7: Tom computes real shared keys with both sides
shared_T_A = pow(A_real, t, p)
shared_T_B = pow(B_real, t, p)

print("=== FINAL SHARED KEYS ===")
print("Alice's secret key (actually with Tom):", shared_A_T)
print("Tom's key with Alice:", shared_T_A)
print()

print("Bob's secret key (actually with Tom):", shared_B_T)
print("Tom's key with Bob:", shared_T_B)
print()

print("=== VERIFICATION ===")
print("Do Alice and Bob share the same key? ", shared_A_T == shared_B_T)
print()

# ---------------------------------------------
# Visualization of MITM Attack
# ---------------------------------------------
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))

# Positions of players
alice = (0, 1)
tom = (1, 0.5)
bob = (2, 1)

plt.scatter(*alice, s=300)
plt.scatter(*tom, s=300)
plt.scatter(*bob, s=300)

plt.text(alice[0], alice[1]+0.08, "Alice", ha="center", fontsize=12)
plt.text(tom[0], tom[1]+0.08, "Tom (Attacker)", ha="center", fontsize=12)
plt.text(bob[0], bob[1]+0.08, "Bob", ha="center", fontsize=12)

# Intercepted paths
plt.arrow(alice[0], alice[1], 0.8, -0.4, width=0.005, length_includes_head=True)
plt.text(0.45, 0.6, "Alice sends A\nTom intercepts", fontsize=10)

plt.arrow(bob[0], bob[1], -0.8, -0.4, width=0.005, length_includes_head=True)
plt.text(1.55, 0.6, "Bob sends B\nTom intercepts", fontsize=10)

# Fake keys from Tom
plt.arrow(tom[0], tom[1], -0.8, 0.4, width=0.005, color="red", length_includes_head=True)
plt.text(0.3, 0.95, "Fake key to Alice", fontsize=10, color="red")

plt.arrow(tom[0], tom[1], 0.8, 0.4, width=0.005, color="red", length_includes_head=True)
plt.text(1.7, 0.95, "Fake key to Bob", fontsize=10, color="red")

plt.title("Man in the Middle Attack on Diffie Hellman")
plt.axis("off")
plt.show()
