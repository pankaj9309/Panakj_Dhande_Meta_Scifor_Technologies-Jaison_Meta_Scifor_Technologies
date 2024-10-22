import streamlit as st

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to find prime numbers in a range
def get_prime_numbers(start, end):
    primes = [num for num in range(start, end + 1) if is_prime(num)]
    return primes

# Streamlit app
st.title("Prime Numbers Finder")

# User input for selecting the range (start and end values)
start = st.number_input("Select the start of the range:", min_value=0, value=10)
end = st.number_input("Select the end of the range:", min_value=start + 1, value=50)

# Button to trigger the calculation of primes
if st.button("Find Prime Numbers"):
    # Get the list of primes in the selected range
    prime_numbers = get_prime_numbers(start, end)
    
    if prime_numbers:
        st.write(f"Prime numbers between {start} and {end}:")
        st.write(prime_numbers)
    else:
        st.write(f"No prime numbers found in the range {start} to {end}.")
