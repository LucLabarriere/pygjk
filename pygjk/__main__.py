from pygjk import core
import cProfile
import pstats

def main():
    core.Application()

if __name__ == '__main__':
    main()
    #cProfile.run('main()', "output.dat")
    #with open("output_time.txt", "w") as f:
    #    p = pstats.Stats("output.dat", stream=f)
    #    p.sort_stats("time").print_stats()

    #with open("output_calls.txt", "w") as f:
    #    p = pstats.Stats("output.dat", stream=f)
    #    p.sort_stats("calls").print_stats()


