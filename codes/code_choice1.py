python
def is_prime(n):
  """Returns True if n is a prime number, False otherwise."""
  if n <= 1:
    return False
  for i in range(2, n):
    if n % i == 0:
      return False
  return True


primes = []
for i in range(2, 51):
  if is_prime(i):
    primes.append(i)

print("The prime numbers from 1 to 50 are:")
print(*primes)
```

This code will print the following output:

```
The prime numbers from 1 to 50 are:
2
3
5
7
11
13
17
19
23
29
31
37
41
43
47
