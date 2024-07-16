class MT19937:
    def __init__(self, seed):
        # Constants for the MT19937
        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908B0DF
        self.u, self.d = 11, 0xFFFFFFFF
        self.s, self.b = 7, 0x9D2C5680
        self.t, self.c = 15, 0xEFC60000
        self.l = 18
        self.f = 1812433253

        # Initialize the state array with the seed
        self.MT = [0] * self.n
        self.index = self.n  # Set index to n to force a twist on the first random call
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (~self.lower_mask) & self.d

        # Initialize the generator from a seed
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = self.int_32(self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i)

    def int_32(self, x):
        # Get the 32 least significant bits
        return int(x & 0xFFFFFFFF)

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:  # lowest bit of x is 1
                xA ^= self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def random(self):
        if self.index >= self.n:
            self.twist()

        y = self.MT[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.index += 1
        return self.int_32(y) / float(0xFFFFFFFF)

# Usage example
if __name__ == "__main__":
    seed = 5489 # Example seed
    rng = MT19937(seed)
    for _ in range(10):
        print(rng.random())
