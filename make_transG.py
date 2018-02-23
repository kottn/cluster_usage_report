import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import matplotlib.cm as cm
#plt.rcParams['font.family'] = 'Times New Roman'
plt.style.use('classic')
plt.rcParams['font.size'] = 20
#
month_label = ['2014/10',\
               '2014/11',\
               '2014/12',\
               '2015/01',\
               '2015/02',\
               '2015/03',\
               '2015/04',\
               '2015/05',\
               '2015/06',\
               '2015/07',\
               '2015/08',\
               '2015/09',\
               '2015/10',\
               '2015/11',\
               '2015/12',\
               '2016/01',\
               '2016/02',\
               '2016/03',\
               '2016/04',\
               '2016/05',\
               '2016/06',\
               '2016/07',\
               '2016/08',\
               '2016/09',\
               '2016/10',\
               '2016/11',\
               '2016/12',\
               '2017/01',\
               '2017/02',\
               '2017/03',\
               '2017/04',\
               '2017/05',\
               '2016/06',\
               '2017/07',\
               '2017/08',\
               '2017/09',\
               '2017/10',\
               '2017/11',\
               '2017/12',\
               '2018/01']
#
x = np.arange(1,len(month_label)+1)
usage = np.array([0.05,\
                  0.02,\
                  0.001,\
                  0.291,\
                  0.0,\
                  0.0,\
                  0.0,\
                  0.0,\
                  1.448,\
                  19.489,\
                  4.711,\
                  1.966,\
                  8.905,\
                  20.435,\
                  35.725,\
                  48.27,\
                  11.895,\
                  3.401,\
                  16.266,\
                  11.361,\
                  11.446,\
                  0.082,\
                  12.013,\
                  41.109,\
                  9.028,\
                  10.967,\
                  17.402,\
                  24.628,\
                  49.243,\
                  64.655,\
                  68.213,\
                  30.819,\
                  15.110,\
                  41.385,\
                  10.478,\
                   8.050,\
                  29.242,\
                   5.467,\
                  12.077,\
                  18.429])
#
plt.figure(figsize=(18,9))
plt.xlim(0,len(month_label))
plt.ylim(0,100)
plt.xticks(np.arange(0,len(month_label)+1), month_label, rotation=30)
plt.yticks(np.arange(0,101,10))
plt.ylabel(u'Operation efficiency (%)')
#
#plt.set_xticklabels(month_label, rotation=30, fontsize='samll')
plt.plot(x, usage, lw=2.0, marker='o')
plt.grid(True)
plt.tight_layout()
#
plt.savefig("usage_trans.png",dpi=600)
