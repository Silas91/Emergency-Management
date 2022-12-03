import pandas as pd
from sklearn.linear_model import BayesianRidge
df = pd.read_csv(r'C:\Users\M3ECHJJJ\github\GIS_Tasks\Data_Science\Glide_Path_v2.csv')
df
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def power_law(x, a, b):
    return a*np.power(x, b)

x = df['Mission Day'].head().to_numpy()
y = df["Active"].head().to_numpy().astype('int')

x = x.reshape(-1, 1)
y = y.reshape(-1, 1)


x
#%%


poly_reg = PolynomialFeatures(degree=5)
X_poly = poly_reg.fit_transform(x)
pol_reg = LinearRegression()
pol_reg.fit(X_poly, y)

# Visualizing the Polymonial Regression results
def viz_polymonial():
    plt.scatter(x, y, color='red')
    plt.plot(x, pol_reg.predict(poly_reg.fit_transform(x)), color='blue')
    plt.title('Truth or Bluff (Linear Regression)')
    plt.xlabel('Position level')
    plt.ylabel('Salary')
    plt.show()
    return
viz_polymonial()
#%%
coef = pol_reg.coef_[0]
print(pol_reg.intercept_ + coef[0] + coef[1]*x + coef[2]*x**2 + coef[3]*x**3 + coef[4]*x**4 + coef[5]*x**5)

df = pd.read_csv(r'C:\Users\M3ECHJJJ\github\GIS_Tasks\Data_Science\Ida_Blue_Roof.csv')


df.dateqccomplete=pd.to_datetime(df.dateqccomplete)
df.dateqccomplete=df.dateqccomplete.dt.strftime('%Y-%m-%d')
pd.pivot_table(df,index=["appcountyname","qccontractorname"],
               values=["roeidpk"],
               aggfunc='count',fill_value=0,
               columns=["dateqccomplete"]
                      )
    df

df.groupby(['dateqccomplete', 'qccontractorname']).size()
