def allocate_chests(k1, k2, masses, indices, mass_index, n, n_ship_two):
    if mass_index > n:
        print()
    else:
        k1 -= masses[mass_index]
        if k1>=0:
            indices[i] = 0
            allocate_chests(k1, k2, masses, indices, mass_index+1, n, n_ship_two)



