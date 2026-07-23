def fibonacci(n):
    """Calculates the Fibonacci sequence up to n terms and prints it."""
    if n <= 0:
        return "Please enter a positive integer for the number of terms."
    elif n == 1:
        return "The first term is: 0"
    else:
        sequence = [0, 1]
        while len(sequence) < n:
            next_term = sequence[-1] + sequence[-2]
            sequence.append(next_term)
        return f"Fibonacci Sequence up to {n} terms: {', '.join(map(str, sequence))}"

if __name__ == "__main__":
    try:
        # Prompt the user for input in a real interactive setting, 
        # but for a runnable script example, we'll set a default value.
        num_terms = int(input("Enter the number of Fibonacci terms you want to calculate (e.g., 10): "))
        result = fibonacci(num_terms)
        print("-" * 40)
        print(result)
        print("-" * 40)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")