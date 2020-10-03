import numpy as np
import pandas as pd
import csv


def sphere_creation():
    # r = 1.0
    # phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
    # r = 1.01
    # phi, theta = np.mgrid[0.0:np.pi:20j, 0.0:2.0*np.pi:20j]
    r = 2.0
    phi, theta = np.mgrid[0.0:np.pi:20j, 0.0:2.0*np.pi:20j]
    X = r*np.sin(phi)*np.cos(theta)
    Y = r*np.sin(phi)*np.sin(theta)
    Z = r*np.cos(phi)
    print(len(X))
    print(len(Y))
    print(len(Z))
    _x = [item for sublist in X for item in sublist]
    _y = [item for sublist in Y for item in sublist]
    _z = [item for sublist in Z for item in sublist]
    return [_x, _y, _z]


def surface_creation():
    a, b, c, d = 1, 2, 3, 4
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    X, Y = np.meshgrid(x, y)
    # 1.
    # a*y*x^3 + b*y*y/x + c*z = d
    # Z = (d - a*X*X*X*Y - (b*Y*Y)/X) / c
    # 2.
    # a*x + b*y + c*z = d
    Z = (d - a*X - b*Y) / c
    print(len(X))
    print(len(Y))
    print(len(Z))
    _x = [item for sublist in X for item in sublist]
    _y = [item for sublist in Y for item in sublist]
    _z = [item for sublist in Z for item in sublist]
    print(len(_x))
    print(len(_y))
    print(len(_z))
    return [_x, _y, _z]


def create_csv(list_of_args, default_name='test.csv'):
    df = pd.DataFrame(list_of_args)
    print(df)
    df.to_csv(default_name, index=False, header=False)


def main():
    create_csv(surface_creation(), 'surface_0.csv')
    create_csv(sphere_creation(), 'sphere_0.csv')


if __name__ == "__main__":

    main()
