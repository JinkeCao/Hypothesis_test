from collections import Counter, OrderedDict
import datetime  
import statsmodels.tsa.stattools as ts
import numpy

start = datetime.datetime.strptime('2017-12-31', '%Y-%m-%d')  
end = datetime.datetime.strptime('2018-05-01', '%Y-%m-%d')
date_keys = []
while start < end:  
    start += datetime.timedelta(days=1)  
    date_keys.append(start.strftime('%Y-%m-%d'))

app_date = {}
with open('qianzhan_app_0514.txt') as f:
    for i in f:
        try:
            i = i.split('\t')
            if i[4]=='ime_app' or i[4]=='sdk_log' or i[4]=='vcoam_log':
                i = eval(i[2])
                for j in i:
                    if set(j['load_info']) & set(date_keys):
                        app_date.setdefault(j['app_name'], []).extend(j['load_info'])
        except:
            continue
print(len(app_date))

n = 0

for i in app_date:
    date_seq = OrderedDict()
    date_cnt = Counter(app_date[i])
    for k in date_keys:
        date_seq[k] = date_cnt.setdefault(k, 0)
    x = numpy.array(list(date_seq.values()))
    result = ts.adfuller(x, maxlag =1)
    if result[0]<result[4]['1%']:
        with open('qz_appUsed_stationary_process.txt', 'a') as f:
            print(i, file = f)
    else:
        with open('qz_appUsed_adfuller_positive.txt', 'a') as f:
            print(i, file = f)
