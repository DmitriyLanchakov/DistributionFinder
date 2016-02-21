import numpy as np
import scipy.stats as st
import MySQLdb as mdb
import pandas as pd
import matplotlib.pyplot as plt
import time

scriptStart = time.time()

#connect to DB
def connect_DB():
    # connect to <a href="http://www.talaikis.com/mysql/">MySQL</a>
    db_host = '127.0.0.1'
    db_user = 'root'
    db_pass = '8h^=GP655@740u9'
    db_name = 'lean'
    
    con = mdb.connect(db_host, db_user, db_pass, db_name)
    
    return con

#disconnect from databse
def disconnect(con):
    # disconnect from server
    con.close()

#get data
def req_sql(sym, con):
    # Select all of the historic close data
    sql = """SELECT DATE_TIME, CLOSE FROM `"""+sym+"""` WHERE PERIOD = 1440 ORDER BY DATE_TIME ASC;"""

     #create a pandas dataframe
    df = pd.read_sql_query(sql, con=con, index_col='DATE_TIME')

    return df

#distribution finder function
def distribution_finder(data):
    #list of distributions
    distributions = [st.laplace, st.norm, st.anglit, st.arcsine, st.beta,
                 st.bradford, st.cauchy, st.chi, st.chi2, st.cosine,
                 st.dgamma, st.dweibull, st.expon, st.exponpow,
                 st.fatiguelife, st.foldnorm, st.frechet_r, st.frechet_l,
                 st.genlogistic, st.gennorm, st.genexpon, st.gausshyper,
                 st.gamma, st.gengamma, st.genhalflogistic, st.gilbrat,
                 st.gompertz, st.gumbel_r, st.gumbel_l, st.halflogistic,
                 st.halfnorm, st.halfgennorm, st.hypsecant, st.invgauss, 
                 st.johnsonsb, st.johnsonsu, st.kstwobign, st.logistic,
                 st.loggamma, st.lognorm, st.maxwell, st.nakagami, st.ncx2, 
                 st.pearson3, st.powerlaw, st.powernorm, st.rdist,
                 st.rayleigh, st.rice, st.recipinvgauss, st.semicircular,
                 st.t, st.truncexpon, st.uniform, st.vonmises, st.wald,
                 st.weibull_min, st.weibull_max, st.alpha, st.burr, st.pareto]
    
    mles = []

    for dist in distributions:
        #find parameters
        param_ = dist.fit(data)
        
        #negative loglikelihood function
        mle = dist.nnlf(param_, data)
        
        #add to list
        mles.append(mle) 

    res = [(dist.name, mle) for dist, mle in zip(distributions, mles)]
    results = sorted(zip(distributions, mles), key=lambda d: d[1])
    
    for i in range(1, len(results)):
        print str(i) + ": " + results[i][0].name + ", MLE: "+ str(results[i][1])

if __name__ == "__main__":
    
    sym = ["S&P500"]
    
    con = connect_DB()
    
    returns = req_sql(sym[0], con).pct_change()
    
    disconnect(con)
    
    np_data =  returns["CLOSE"].dropna().as_matrix()
    
    if len(np_data) > 100:
        distribution_finder(np_data)
    
    plt.hist(np.sort(np_data), bins=100, histtype='barstacked')
    plt.show()

    timeused = (time.time()-scriptStart)/60

    print("Done in ",timeused, " minutes")