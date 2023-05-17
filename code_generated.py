python
def sum_of_even_numbers(n):
  """Returns the sum of all even numbers from 1 to n."""
  sum = 0
  for i in range(2, n + 1, 2):
    sum += i
  return sum


print(sum_of_even_numbers(100))
```

This code works by using a for loop to iterate over all the numbers from 2 to n, and adding each even number to the sum variable. The sum variable is then returned at the end of the function.

Here is an example of how to use the code:

```python
>>> sum_of_even_numbers(100)
5000
