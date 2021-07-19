import matplotlib.pyplot as plt


def helloworld():
    fig = plt.figure()
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    fig.savefig("test.png")
