# Quantum period of hyperbolic toral automorphisms (classical cat maps)
# Nir Schwartz
# Description:
# In [NS21] we consider extremely short quantum periods P(N) for the quantum cat map
# related to classical periods (cf. \cite{BDB00} for the connection). The code below
# finds the quantum periods through this connection and marks as well all elements of the set
# mathcal{N}_4 defined in [NS21].

import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool


def fast_find_order(dimat):
    # find the quantum period of a hard-coded classical cat map mod N
    # (being the inverse of effective Plank's constant)
    print(f'Finding order for N=:{dimat}')
    cat = np.matrix([[2, 1], [3, 2]], dtype=object)
    order = 1
    curr_cat = cat
    while not (np.mod(curr_cat, dimat) == np.eye(2)).all():
        order += 1
        curr_cat = np.linalg.matrix_power(cat, order)

    if np.mod(dimat, 2) == 1:
        return order

    reminder = (curr_cat - np.matrix([[1, 0], [0, 1]], dtype=object)) // dimat

    if np.mod(reminder[0, 1], 2) == 0 and\
            np.mod(reminder[1, 0], 2) == 0 and\
            np.mod(dimat, 2) == 0:
        return order

    return 2 * order


def plot_periods(max_num):
    small_np = np.loadtxt('small_periods.txt', skiprows=2)
    entire_np = np.loadtxt('all_periods.txt', skiprows=2)
    t = np.linspace(2.0, float(max_num + 1), max_num ** 2)
    s1 = 2 * np.log10(t) / np.log10(2 + np.sqrt(3))
    s2 = 1.5 * t * np.log(np.abs(np.log(t)))
    fig = plt.figure(figsize=(20, 10))
    fig.add_subplot(211)
    plt.plot(t, s1, c='red', label=r"$2\frac{\log N}{\log \lambda}$")
    plt.plot(t, s2, c='purple', label=r"$N^{1+\epsilon}$")
    plt.scatter(entire_np[:, 0], entire_np[:, 1], s=4, c='blue', label="P(N)")
    plt.scatter(small_np[:, 0], small_np[:, 1], s=5, c='orange', label="Short P(N)")
    # plt.yscale("log")
    plt.xlabel("$N$")
    plt.ylim([1, 2 * max_num])
    plt.xlim([2, max_num + 1])
    plt.ylabel("$P(N)$")
    plt.legend(loc="upper left")
    plt.title('All classical periods under ' + str(max_num))
    fig.tight_layout(pad=3.0)
    fig.add_subplot(212)
    plt.plot(t, s1, c='red', label=r'2$\frac{\log N}{\log \lambda}$')
    s3 = 4 * np.log10(t) / np.log10(2 + np.sqrt(3))
    plt.plot(t, s3, c='orange', label=r'4$\frac{\log N}{\log \lambda}$')
    plt.scatter(small_np[:, 0], small_np[:, 1], s=6, c='blue', label=r'Short $P(N)$')
    plt.xscale("log")
    plt.xlim([2, max_num + 1])
    plt.ylabel("Short $P(N)$")
    plt.xlabel("$N$")
    plt.legend(loc="upper left")
    plt.title('Extremely short periods under '+str(max_num))
    #plt.show()
    plt.savefig(f'Quantum periods with extremely short ones until N={max_num}')


def main():
    # hard code maximal N and list all periods in one file and the extremly short ones in another.
    max_num = 10000
    orders = np.zeros([1, max_num - 1])
    idx = 0

    filenames = ['all_periods.txt', 'small_periods.txt', 'degNs.txt']
    for filename in filenames:
        if os.path.exists(filename):
            os.remove(filename)

    with open('all_periods.txt', "w") as file:
        with open('small_periods.txt', "w") as small_file:
            with open('degNs.txt', "w") as deg_Ns:
                N = -1
                file.write(f'Dataset: Quantum periods until N={max_num}\n')
                file.write('N P(N)\n')
                small_file.write(f'Dataset: Short quantum periods until N={max_num}\n')
                small_file.write('N P(N)\n')
                deg_Ns.write(f'List of Ns having small quantum period until N={max_num}\n')
                deg_Ns.write('N\n')
                # orders = await asyncio.gather(*[fast_find_order(N) for N in range(2, max_num + 1)])
                pool = Pool()
                orders = pool.map(fast_find_order, range(2, max_num + 1))

                for N in range(2, max_num + 1):
                    # an extremely short classical period s.t. its quantum analogue is in N_alpha
                    if orders[idx] < 4 * np.log(N) / np.abs(np.log(2 + np.sqrt(3))):
                        small_file.write(f"{idx+2} {orders[idx]} \n")
                        deg_Ns.write(str(idx+2) + '\n')

                    file.write(f"{idx+2} {orders[idx]} \n")
                    print(f'done with:{N}')
                    idx += 1

    print(f'Done finding all quantum periods until N={max_num}')

    # plot the results
    plot_periods(max_num)


if __name__ == "__main__":
    main()
