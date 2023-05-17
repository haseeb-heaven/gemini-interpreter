python
def is_prime(number):
  """Returns True if the number is a prime number, False otherwise."""
  if number <= 1:
    return False
  for i in range(2, number):
    if number % i == 0:
      return False
  return True


primes = []
for i in range(2, 51):
  if is_prime(i):
    primes.append(i)

print("The prime numbers from 1 to 50 are:")
print(*primes)

