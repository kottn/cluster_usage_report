import glob
import numpy as np
import matplotlib.pyplot as plt
from subprocess import run, PIPE
import getpass
import calendar

####### INP. #######
HOST    = 'kimchi'
allcore = 320
YY      = '2018'
MM      = '01'
####################

### GET CLUSTER INFO & TORQUE-LOGS
cmd = "mkdir -p logfiles/" + HOST + '/' + YY + '_' + MM
run(cmd, shell=True)
cmd = 'scp root@' + HOST + ':/var/spool/torque/server_priv/accounting/' + YY + MM + '* ./logfiles/' + HOST + '/' + YY + '_' + MM
run(cmd, shell=True)
cmd = 'ssh root@' + HOST + ' \ls /home'
u = run(cmd, shell=True, stdout=PIPE, universal_newlines=True).stdout.splitlines()
l = [0] * len(u)
cluster_usage = dict(zip(u, l))

cmd = 'mkdir -p ' + HOST
run(cmd, shell=True)
outname = HOST + '/Usage_' + YY + '_' + MM
filelist = glob.glob('./logfiles/' + HOST + '/' + YY + '_' + MM + '/*')

when  = '(' + MM + ', ' + YY + ')'
ndays = calendar.monthrange(int(YY),int(MM))[1]

total_usage = 0
for logfile in filelist:
    data = open(logfile)
    lines_in_logfile = data.readlines()
    data.close()

    for line in lines_in_logfile:
        resource_core  = 0
        resource_time  = 0
        resource_total = 0
        line = line.split(' ')

        flag = line[1].split(';')
        flag = flag[1]

        # ENDED-JOBS
        #-----------
        if flag == 'E':
            username = line[1].split('=')
            username = username[1]
            resource = line[10]
            resource = resource.split('+')
            resource_core = len(resource)

            # CHECK WALL TIME
            walltime = line[-1].split('=')
            if walltime[0] == 'Output_Path':
                walltime = line[-3].split('=')
            walltime = walltime[1].split(':')

            # CONVERT WALL TIME(H,M,S) TO HOUR
            hours   = float(walltime[0])
            minutes = float(walltime[1])
            seconds = float(walltime[2])
            resource_time = hours + (minutes/60) + (seconds/3600)

            # CLACULATE RESOURCE_TOTAL
            resource_total = resource_core * resource_time

            # ADD TO USAGE DICT
            cluster_usage[username] = cluster_usage[username] + resource_total

names = []
usage_val = []

# REPORT (TXT)
outfile = open(outname+'.txt', 'w')
outfile.write('Hostname: '+ HOST + '\r\n')
outfile.write('--------------------------------------------' + '\r\n')
outfile.write('Username' + ' : ' + 'Usage (CPU core x hour)' + '\r\n')
outfile.write('--------------------------------------------' + '\r\n')
for k, v in sorted(cluster_usage.items(), reverse=True, key=lambda x:x[1]):
    outfile.write(k + ' : ' + str(round(v,2)) + '\r\n')
    names.append(k)
    usage_val.append(round(v,2))
    total_usage = total_usage + round(v,2)
outfile.write('--------------------------------------------' + '\r\n')
outfile.write('Total usage' + ' : ' + str(round(total_usage,2)) + ' (CPU core x hour)' + '\r\n')
outfile.write('Operation efficiency' + ' : ' + str(round(total_usage/(ndays*24*allcore)*100,1)) + '%' + '\r\n')
outfile.close()

cmd = "cat " + outname + '.txt'
run(cmd, shell=True)


# REPORT (MARKDOWN)
mdfile = open(outname+'.md', 'w')
mdfile.write('# Cluster usage report ' + when + '\r\n')
mdfile.write('### Hostname: ' + HOST + '\r\n')
mdfile.write('NOTE: The list does NOT include users whose usage was 0' + '\r\n')
mdfile.write('\r\n')
mdfile.write('|Username|Usage (CPU core x hour)|' + '\r\n')
mdfile.write('|:--:|--:|' + '\r\n')
for k, v in sorted(cluster_usage.items(), reverse=True, key=lambda x:x[1]):
    if round(v,2) != 0:
        mdfile.write('|'+ k + '|' + str(round(v,2)) + '|' + '\r\n')
mdfile.write('|Total|' + str(round(total_usage,2)) + '|' + '\r\n')
mdfile.write('### Operation efficiency : ' + str(round(total_usage/(ndays*24*allcore)*100,1)) + '%' + '\r\n')
mdfile.write('---' + '\r\n')
mdfile.write('![](../' + outname + '.png)' + '\r\n')
mdfile.write('\r\n')

mdfile.write('# Transition of operation efficiency' + '\r\n')
mdfile.write('![](./Usage_Transition.png)')
mdfile.close()


# PLOT ACCOUNTING
plt.rcParams['font.size'] = 20
x = np.arange(1,len(names)+1)

fig = plt.figure(1, figsize=(20,8))
ax = plt.axes()


ax.grid(True)
ax.set_title('Usage rate of each user')
ax.set_ylabel('Usage (Cpu core x hour)')
ax.bar(x, usage_val, linewidth=0.5, width=0.7, tick_label=names, align='center')
ax.set_xticklabels(names, rotation=90, ha='center')

for i, j in zip(x, usage_val):
    percentage = 0
    if total_usage > 0:
        percentage = j/total_usage*100
    if percentage > 0.1:
        plt.text(i, j, "%.1f%%" % percentage, rotation=60, ha='center', va='bottom')

fig.tight_layout()
fig.savefig(outname+'.png', dpi=300)

