def combo_n(lst, n):
    if n == 0:
        return [[]]

    temp = []
    for i in range(0, len(lst)):
        m = lst[i]
        for j in combo_n(lst[i + 1:], n - 1):
            temp.append([m] + j)

    return temp


def allocate_chests(k1, k2, masses):
    combos = combo_n(masses, int(len(masses) / 4))
    for combo in combos:
        if sum(combo) > k2:
            pass
        elif sum(list(set(masses) - set(combo))) > k1:
            pass
        else:
            print("(", end="")
            for mass in list(set(masses) - set(combo)):
                print(masses.index(mass) + 1, end=' ')
            print(' , ', end='')
            for mass_two in combo:
                print(masses.index(mass_two)+1, end=")")
            print('\n')


allocate_chests(5, 3, [1, 1.5, 2, 2.5])
