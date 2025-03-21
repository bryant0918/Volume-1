# newtons_method.py
"""Volume 1: Newton's Method.
Bryant McArthur
Sec 002
January 25
"""

import numpy as np
import scipy.optimize as op
from autograd import grad,jacobian,elementwise_grad
from matplotlib import pyplot as plt
from scipy import linalg as la

# Problems 1, 3, and 5
def newton(f, x0, Df, tol=1e-5, maxiter=15, alpha=1.):
    """Use Newton's method to approximate a zero of the function f.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should returns when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.
        alpha (float): Backtracking scalar (Problem 3).

    Returns:
        (float or ndarray): The approximation for a zero of f.
        (bool): Whether or not Newton's method converged.
        (int): The number of iterations computed.
    """
    b = False
    #If it's a scalar
    if np.isscalar(x0):
        #Iterate at most k times
        for k in range(maxiter):
            #Apply Newton's Method with an optional alpha
            x1 = x0 - alpha*f(x0)/Df(x0)
            #Break if converged
            if abs(x1-x0) < tol:
                b = True
                break
            x0 = x1
        #Return limit, whether it converged and the number of iterations
        return x1,b,k+1
    
    #Repeat for multidimensional using la.solve to solve Ax=b
    else:
        for k in range(maxiter):
            y = np.linalg.solve(Df(x0),f(x0))
            x1 = x0 - alpha*y
            if np.linalg.norm(x1-x0) < tol:
                b = True
                break
            x0 = x1
        return x1,b,k+1
        

f = lambda x: np.exp(x) - 2
Df = lambda x: np.exp(x)
g = lambda x: np.sign(x) * np.power(np.abs(x), 1./3)
dg = grad(g)

"""
print(newton(f,1.7,Df))
print(op.newton(f,1.7,Df,tol=1e-5,maxiter=15))
print(newton(g, .1,dg))
print(newton(g,.01,dg,alpha=.4))
print(newton(g,.1,dg,alpha=.32))
"""


# Problem 2
def prob2(N1, N2, P1, P2):
    """Use Newton's method to solve for the constant r that satisfies

                P1[(1+r)**N1 - 1] = P2[1 - (1+r)**(-N2)].

    Use r_0 = 0.1 for the initial guess.

    Parameters:
        P1 (float): Amount of money deposited into account at the beginning of
            years 1, 2, ..., N1.
        P2 (float): Amount of money withdrawn at the beginning of years N1+1,
            N1+2, ..., N1+N2.
        N1 (int): Number of years money is deposited.
        N2 (int): Number of years money is withdrawn.

    Returns:
        (float): the value of r that satisfies the equation.
    """
    #This one is pretty straight forward
    f = lambda r: P1*((1+r)**N1-1)-(P2*(1-(1+r)**-N2))
    df = grad(f)
    
    return newton(f,.1,df)[0]

#print(prob2(30,20,2000,8000))


# Problem 4
def optimal_alpha(f, x0, Df, tol=1e-5, maxiter=15):
    """Run Newton's method for various values of alpha in (0,1].
    Plot the alpha value against the number of iterations until convergence.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should returns when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): a value for alpha that results in the lowest number of
            iterations.
    """
    #Initialize everything
    alphas = [i*.01 for i in range(1,100)]
    ks = []
    #If scalar
    if np.isscalar(x0):
        #Iterate through alphas
        for a in alphas:
            x = x0
            #Apply newton's method with backtracking
            for k in range(maxiter):
                x1 = x - a*f(x)/Df(x)
                if abs(x1-x) < tol:
                    break
                x = x1
            ks.append(k)
            
    #If multi-dimensional
    else:
        for a in alphas:
            x = x0
            for k in range(maxiter):
                y = la.solve(Df(x),f(x))
                x1 = x - a*y
                if la.norm(x1-x) < tol:
                    break
                x = x1
            ks.append(k)
    
    #Plot it
    plt.plot(alphas,ks)
    plt.show()
    
    #Return the optimal alpha
    index = np.argmin(ks)
    return alphas[index]
        
    
#print(optimal_alpha(g,.01,dg,maxiter = 40))


# Problem 6
def prob6():
    """Consider the following Bioremediation system.

                              5xy − x(1 + y) = 0
                        −xy + (1 − y)(1 + y) = 0

    Find an initial point such that Newton’s method converges to either
    (0,1) or (0,−1) with alpha = 1, and to (3.75, .25) with alpha = 0.55.
    Return the intial point as a 1-D NumPy array with 2 entries.
    """
    #Initialize everything
    f = lambda x: np.array([5*x[0]*x[1] - (x[0]*(1+x[1])), -x[0]*x[1] + (1-x[1])*(1+x[1])])
    df = lambda x:np.array([[4*x[1]-1,4*x[0]],[-x[1],-x[0]-2*x[1]]])
    
    xs = np.linspace(-.25,0,100)
    ys = np.linspace(0,.25,100)
    
    #Iterate through all possible points in x and y
    for x in xs:
        for y in ys:
            point = np.array([x,y])
            solution = newton(f,point,df)[0]
            #If the solution is a solution to either of these points then we will test it for our next point
            if np.allclose(solution,np.array([0,1])) or np.allclose(solution,np.array([0,-1])):
                sol = newton(f,point,df,alpha=.55)[0]
                #If our solution also works for this point then we are done.
                if np.allclose(sol,np.array([3.75,.25])):
                    return point
            
#print(prob6())


# Problem 7
def plot_basins(f, Df, zeros, domain, res=1000, iters=15):
    """Plot the basins of attraction of f on the complex plane.

    Parameters:
        f (function): A function from C to C.
        Df (function): The derivative of f, a function from C to C.
        zeros (ndarray): A 1-D array of the zeros of f.
        domain ([r_min, r_max, i_min, i_max]): A list of scalars that define
            the window limits and grid domain for the plot.
        res (int): A scalar that determines the resolution of the plot.
            The visualized grid has shape (res, res).
        iters (int): The exact number of times to iterate Newton's method.
    """
    #Initialize real and imaginary and combined parts
    xreal = np.linspace(domain[0],domain[1],res)
    ximag = np.linspace(domain[2],domain[3],res)
    Xreal,Ximag = np.meshgrid(xreal,ximag)
    X0 = Xreal + 1j*Ximag
    
    #Apply Newton's Method
    for k in range(iters):
        X1 = X0 - f(X0)/Df(X0)
        X0 = X1
    
    #Initialize Y
    Y = np.empty((res,res))
    
    #Find Y
    for i in range(res):
        for j in range(res):
            Y[i,j] = np.argmin(np.abs(X1[i,j]-zeros))
            
    #Plot it
    plt.pcolormesh(Xreal,Ximag,Y)
    plt.xlabel("Reals")
    plt.ylabel("Imaginaries")
    plt.title("Basins of Attraction (Fractals)")
    plt.show()
    
    return

f = lambda x: x**3-1
df = lambda x:3*x**2
zeros = [1,-.5+np.sqrt(3)/2*1j,-.5-np.sqrt(3)/2*1j]
domain = [-1,1,-1,1]
#plot_basins(f,df,zeros,domain)