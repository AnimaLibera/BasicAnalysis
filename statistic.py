import pandas as pd
import scipy.stats as st

def wealtch_index(returns: pd.Series):
    """Take Return Series and calculate Wealthindex"""

    return (1 + returns).cumprod()

def annualized_returns(returns: pd.Series, periods_per_year: int = 52):
    """Calculate annualzide Returns for Return Series"""
    compounded_growth = (1 + returns).prod()
    n_periods = returns.shape[0]
    return compounded_growth ** (periods_per_year / n_periods) - 1

def annualized_volatility(returns: pd.Series, periods_per_year: int = 52):
    """Calculate annualzide Volatility for Return Series"""

    return returns.std() * (periods_per_year ** 0.5)

def skewness(returns: pd.Series):
    """Skewness of a Return Series"""

    demeaned_return = returns - returns.mean()
    sigma_return = demeaned_return.std(ddof=0) #Population STDDEV
    exp = (demeaned_return ** 3).mean()
    return exp / sigma_return ** 3

def kurtosis(returns: pd.Series):
    """Kurtosis of a Return Series"""

    demeaned_return = returns - returns.mean()
    sigma_return = demeaned_return.std(ddof=0) #Population STDDEV
    exp = (demeaned_return ** 4).mean()
    return exp/sigma_return ** 4

def is_normal_distributed(returns: pd.Series, level=0.01):
    """Jargue-Bera Test"""

    _, p_value = st.jarque_bera(returns)
    return p_value > level

def show_descriptive_statistics(returns: pd.DataFrame, periods_per_year: int = 52):
    """Show Descriptive Statistics for Returns DataFrame"""
    ann_returns = returns.aggregate(annualized_returns, periods_per_year=periods_per_year).round(2)
    ann_volatility = returns.aggregate(annualized_volatility, periods_per_year=periods_per_year).round(2)
    skew = returns.aggregate(skewness).round(2)
    kurt = returns.aggregate(kurtosis).round(2)
    normal = returns.aggregate(is_normal_distributed)
    return pd.DataFrame({   "Annualized Return": ann_returns,
                            "Annualized Volatility": ann_volatility,
                            "Skewness": skew,
                            "Kurtosis": kurt,
                            "Normal Distribution": normal
                            })