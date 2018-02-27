import numpy as np
import matplotlib.pyplot as plt

####### INP. #######
HOST = 'serverhost'
####################

if HOST == 'serverhost':
    d = {'2016/09': 27.8,\
         '2016/10': 104.9,\
         '2016/11': 56.5,\
         '2016/12': 99.9,\
         '2017/01': 72.1,\
         '2017/02': 18.5,\
         '2017/03': 56.2,\
         '2017/04': 58.8,\
         '2017/05': 69.3,\
         '2017/06': 39.9,\
         '2017/07': 30.3,\
         '2017/08': 41.9,\
         '2017/09': 48.4,\
         '2017/10': 79.8,\
         '2017/11': 28.8,\
         '2017/12': 50.2,\
         '2018/01': 75.9}

#  if HOST == 'morehost':
#      d = {'2017/11': 5.6,\
#           '2017/12': 26.2,\
#           '2018/01': 23.4}
#
#  if HOST == 'moremore':
#      d = {'2017/06': 0.1,\
#           '2017/07': 9.0,\
#           '2017/08': 39.2,\
#           '2017/09': 22.9,\
#           '2017/10': 41.9,\
#           '2017/11': 15.2,\
#           '2017/12': 45.8,\
#           '2018/01': 46.9}

plt.rcParams['font.size'] = 20

lists = d.items()
x, y = zip(*lists)

plt.figure(figsize=(20,8))
plt.ylim(0,110)
plt.xticks(np.arange(0,len(d)), list(d.keys()), rotation=70)
plt.ylabel(u'Operation efficiency (%)')
plt.plot(x, y, lw=2.0, marker='o')
for i, j in zip(x, y):
    plt.text(i, j, j, ha='center', va='bottom')
plt.grid(True)
plt.title('Hostname: ' + HOST)

plt.tight_layout()
plt.savefig(HOST+"/Usage_transition.png",dpi=300)
