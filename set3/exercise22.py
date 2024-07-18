from time import time
from random import randint
from exercise21 import MT19937

# Usage example
if __name__ == "__main__":
    # Cracking the seed
    now = int(time())
    delta1 = randint(40, 1000)
    seed = now  + delta1
    delta2 = randint(40, 1000)
    prng = MT19937(seed).yield_random()
    random_nb = next(prng)
    time_of_output = now + delta1 + delta2

    for i in range(40, 1000):
        seed = time_of_output - i
        prng = MT19937(seed).yield_random()
        if next(prng) == random_nb:
            guess = seed
            break
    else:
        raise Exception('could not regenerate random nb')   
    
    print(f'Guessed seed: {guess}')