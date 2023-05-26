def is_prime(number):
    if number <= 1:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False

    return True


def main():
    for i in range(2, 101):
        if is_prime(i):
            print(i)


if __name__ == "__main__":
    main()