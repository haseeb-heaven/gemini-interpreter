c++
#include <iostream>

using namespace std;

int main() {
  int num = 10;
  int factorial = 1;

  for (int i = 1; i <= num; i++) {
    factorial *= i;
  }

  cout << "The factorial of 10 is " << factorial << endl;

  return 0;
}
```

This code will print the following output:

```
The factorial of 10 is 3628800
