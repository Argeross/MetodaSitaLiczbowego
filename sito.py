import math

def check_prime(n): # Test pierwszości
    if n < 2 :
        return False

    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

def pow_idx(n, p): # Wykładnik danego czynnika pierwszego
    p_idx = 0
    while n % p == 0:
        p_idx += 1
        n /= p
    return int(n), p_idx

def preliminary_check(n, base): # Sprawdzenie czy czynniki n są w bazie czynników pierwszych
    p_indexes = [0]*len(base)

    for i, p in enumerate(base):
        n, p_indexes[i] = pow_idx(n, p)
    
    return n, p_indexes

def factor_base(B): # Generowanie bazy czynników pierwszych
    fbase = []

    for i in range(2, B+1):
        if check_prime(i):
            fbase.append(i)
    
    return fbase

def b_smooth(z, base): # Sprawdzanie czy liczba jest B-gładka (Tak -> zwraca wykładniki czynników pierw.)
    z, p_indexes = preliminary_check(z, base)
    
    if z != 1:
        return False
    return p_indexes

def gcd(a, b): # Największy wspólny dzielnik (algorytm Euklidesa)
    while b:
        a, b = b, a%b
    return a

def create_relations(n, B): # Wyszukiwanie par z i z+n
    relations = []  # Przechowuje wykładniki czynników pierwszych
    fbase = factor_base(B)

    for i in range(2, int(n)):
        z_pow = b_smooth(i, fbase)
        z_n_pow = b_smooth(i+n, fbase)

        if z_pow and z_n_pow: # z i z+n są b-gładkie
            relations.append([z_pow, z_n_pow])

        if len(relations) >= 2*len(fbase):
            break
    
    return relations

def sum_list(list_a, list_b): # Dodawanie elementów 2 list
    return [a + b for a,b in zip(list_a, list_b)]

def even(pow_idxes1, pow_idxes2): # Sprawdza czy wykładniki po odejmowaniu są parzyste
    L = sum_list(pow_idxes1[0], pow_idxes2[0])
    P = sum_list(pow_idxes1[1], pow_idxes2[1])
    for l, p in zip(L, P):
        if (l-p) % 2 != 0:
            return False
    
    return [L, P]

def get_factors(L, P, n, base):
    evenL = []  # Dzięki funkcji even() wiemy, że wykładniki nieparzyste możemy odjąć i otrzymać parzyste
    evenP = []

    for l, p in zip(L, P):
        if p%2 == 1:  # Skoro wykładnik po prawej jest nieparzysty to po lewej też musi^
            if l >= p:
                evenL.append(l-p)
                evenP.append(0)
            else:
                evenP.append(p-l)
                evenL.append(0)
        else:
            evenL.append(l)
            evenP.append(p)
    
    l_number = 1
    p_number = 1

    for i, prime in enumerate(base):
        l_number *= pow(prime, evenL[i]/2)  # Dzielenie przez 2 aby otrzymac x, a nie x^2 w kongruencji kwad.
        p_number *= pow(prime, evenP[i]/2)
    
    factor1 = gcd(abs(l_number - p_number), n)
    factor2 = gcd(l_number + p_number, n)
    
    if factor1 == 1 or factor2 == 1: # Faktoryzacja trywialna
        return False
    
    new_factors = []
    
    if not check_prime(factor1): # Sprawdanie czy czynnik jest l. złożoną
        new_factors += rational_sieve(int(factor1), base[-1], base)
    else:
        new_factors.append(factor1)
    
    if not check_prime(factor2):
        new_factors += rational_sieve(int(factor2), base[-1], base)
    else:
        new_factors.append(factor2)
    
    return new_factors


def combine_relations(n, relations, base): # Tworzenie kongruencji kwadratowej

    for i, r1 in enumerate(relations):
        for r2 in relations[i+1:]:
            quadratic = even(r1, r2)
            
            if quadratic:
                factors = get_factors(quadratic[0], quadratic[1], n, base)
                if factors:
                    return factors
    
    return False

def rational_sieve(n, B, primeBase=[]): # Metoda  sita liczbowego

    if primeBase == []:
        primeBase = factor_base(B)

    n, factors_idxs = preliminary_check(n, primeBase)
    factors = [[primeBase[i], factors_idxs[i]] for i in range(len(factors_idxs)) if factors_idxs[i]]

    while n > 1:
        if check_prime(n):
            factors.append([n, 1])
            break

        relations = create_relations(n, B)
        new_factors = combine_relations(n, relations, primeBase)

        if not new_factors:
            print("Faktoryzacja danej liczby się nie powiodła, liczba postaci p^m\
 lub źle dobrany parameter B")
            return False
        
        else:
            for f in new_factors:
                if isinstance(f, list):
                    factors.append(f) # W przypadku gdy NWD zwróciło l. zlożoną to zwrócona została lista (rational_sieve() dla dzielnika)
                    n /= pow(f[0], f[1])
                else:
                    n, f_idx = pow_idx(n, f)
                    factors.append([int(f), f_idx])
    
    return factors

if __name__ == "__main__":
    # W przypadku zmiany testów, sprawdzić sys.maxsize dla maksymalnej możliwej liczby obsługiwanej przez Python na danym komputerze
    # Test -> (Liczba do faktoryzacji, czynnik B)
    tests = [(23423454, 1000), (45234523423, 3600), 
    (5523452342346, 30000), (7523452342312, 30000), (8523452343241, 30000)]
    # Poprawność testów sprawdzona z Wolframalpha

    base30000 = factor_base(30000)
    for t in tests:
        if t[1] == 30000:
            factors = rational_sieve(t[0], t[1], base30000)
        else:
            factors = rational_sieve(t[0], t[1])
        
        if factors:
            result = f"{t[0]} = "
            for f in factors:
                result += f"{f[0]}^{f[1]} * "
        
            print(result.rstrip(" *"))

