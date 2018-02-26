import glob
import calendar
import numpy as np
import matplotlib.pyplot as plt
from subprocess import run, PIPE
import json

#plt.style.use('classic')

####### INP. #######
cluster  = ''
allcore  = 320
this_YY  = '2018'
this_MM  = '01'
####################


YYMM  = this_YY + this_MM
YY_MM = this_YY + '_' + this_MM

### GET CLUSTER INFO & TORQUE-LOGS
cmd = "mkdir -p logfiles/" + cluster + '/' + YY_MM
run(cmd, shell=True)
cmd = 'scp root@' + cluster + ':/var/spool/torque/server_priv/accounting/' + YYMM + '* ./logfiles/' + cluster + '/' + YY_MM
run(cmd, shell=True)
cmd = 'ssh root@' + cluster + ' \ls /home'
u = run(cmd, shell=True, stdout=PIPE, universal_newlines=True).stdout.splitlines()
l = [0] * len(u)
cluster_usage = dict(zip(u, l))

outname = 'Usage_' + cluster + YY_MM
filelist = glob.glob('./logfiles/' + cluster + '/' + YY_MM + '/*')


when = '(' + this_MM + ', ' + this_YY + ')'
ndays = calendar.monthrange(int(this_YY),int(this_MM))[1]


#### CHANGABLE ###
total_usage = 0

for logfile in filelist:
    data = open(logfile)
    lines_in_logfile = data.readlines()
    data.close()
    #
    for line in lines_in_logfile:
        #
        #Initialization
        resource_core = 0
        resource_time = 0
        resource_total = 0
        #
        line = line.split(' ')
        #
        #username = line[1].split('=')
        #print(username)
        #username = username[1]
        #
        flag = line[1].split(';')
        flag = flag[1]
        #
        #print(line)
        if flag == 'E': # calculate cpu_core x wall time
            ###
            username = line[1].split('=')
            username = username[1]
            ###
            #print(logfile, username)
            resource = line[10]
            resource = resource.split('+')
            resource_core = len(resource)
            #-------------------------------------
            #resource = line[10]
            #resource = resource.split(':')
            # Check # of node used
            #num_node = resource[0].split('=')
            #num_node = float(num_node[1])
            # Check # of core used
            #num_core = resource[1].split('=')
            #num_core = float(num_core[1])
            # Calculate total core resource used
            #resource_core = num_node * num_core
            # Check wall time
            walltime = line[-1].split('=')
            walltime = walltime[1].split(':')
            # Convert Wall time(h,m,s) to hour
            hours = float(walltime[0])
            minutes = float(walltime[1])
            seconds = float(walltime[2])
            resource_time = hours + (minutes/60) + (seconds/3600)
            # Claculate resource_total (# of cores x wall time)
            resource_total = resource_core * resource_time
            #
            # Add to usage dict
            cluster_usage[username] = cluster_usage[username] + resource_total
#
names = []
usage_val = []
print('                                            ')
print('                                            ')
print('--------------------------------------------')
print('Username', ':', 'Usage (CPU core x hour)')
print('--------------------------------------------')
for k, v in sorted(cluster_usage.items(), reverse=True, key=lambda x:x[1]):
    print(k, ':', round(v,3))
    names.append(k)
    usage_val.append(round(v,3))
    total_usage = total_usage + round(v,3)
print('--------------------------------------------')
print('Total usage', ' : ', round(total_usage,3), ' (CPU core x hour)')
print('Operation efficiency', ' : ', round((total_usage/(ndays*24*allcore)*100),3), '%')
print('                                            ')
print('                                            ')
#
#
outfile = open(outname+'.txt', 'w')
outfile.write('--------------------------------------------' + '\r\n')
outfile.write('Username' + ' : ' + 'Usage (CPU core x hour)' + '\r\n')
outfile.write('--------------------------------------------' + '\r\n')
for k, v in sorted(cluster_usage.items(), reverse=True, key=lambda x:x[1]):
    outfile.write(k + ' : ' + str(round(v,3)) + '\r\n')
outfile.write('--------------------------------------------' + '\r\n')
outfile.write('Total usage' + ' : ' + str(round(total_usage,3)) + ' (CPU core x hour)' + '\r\n')
outfile.write('Operation efficiency' + ' : ' + str(round(total_usage/(ndays*24*allcore)*100,3)) + '%')
outfile.close()
#
# Graphics
#fp = FontProperties(fname='/Users/fumiyasu/Library/Fonts/NotoSansCJKjp-Medium.otf');
plt.rcParams['font.size'] = 16
x = np.arange(1,len(names)+1)
# bar chart
fig = plt.figure(1, figsize=(18,9))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
ax1.grid(True)
#plt.yscale('log')
ax1.set_title('Total amount of usage')
ax1.set_ylabel('Usage (Cpu core x hour)')
ax1.bar(x, usage_val, linewidth=0.5, width=0.7, tick_label=names, align='center')
ax1.set_xticklabels(names, rotation=90, ha='center')
#ax1.tight_layout()
#ax1.savefig('usage_bar.png', dpi=600)
# pie chart
#fig = plt.figure(2, figsize=(12,12))
ax2.set_title('User percentage')
ax2.pie(usage_val, autopct='%1.1f%%', counterclock=False, startangle=90, labeldistance=0.6, textprops={'color':'white'})
ax2.axis('equal')
#
ax2.legend(names, ncol=4, loc='lower right', bbox_to_anchor=(0.9,-0.15), fontsize=12)
#ax2.tight_layout()
#
fig.subplot_adjust = (0.1,0.8)
fig.tight_layout()
fig.savefig(outname+'.png', dpi=600)
#
# report (markdown)
mdfile = open(outname+'.md', 'w')
mdfile.write('# Cluster usage report ' + when + '\r\n')
mdfile.write('NOTE: The list does NOT include users whose usage was 0' + '\r\n')
mdfile.write('\r\n')
mdfile.write('|Username|Usage (CPU core x hour)|' + '\r\n')
mdfile.write('|:--:|--:|' + '\r\n')
for k, v in sorted(cluster_usage.items(), reverse=True, key=lambda x:x[1]):
    if round(v,3) != 0:
        mdfile.write('|'+ k + '|' + str(round(v,3)) + '|' + '\r\n')
mdfile.write('|Total|' + str(round(total_usage,3)) + '|' + '\r\n')
mdfile.write('### Operation efficiency : ' + str(round(total_usage/(ndays*24*allcore)*100,1)) + '%' + '\r\n')
mdfile.write('---' + '\r\n')
mdfile.write('![](./' + outname + '.png)' + '\r\n')
mdfile.write('\r\n')

mdfile.write('<br />' + '\r\n')  # Adjust for A4 Report
mdfile.write('<br />' + '\r\n')  # Adjust for A4 Report
mdfile.write('<br />' + '\r\n')  # Adjust for A4 Report
mdfile.write('<br />' + '\r\n')  # Adjust for A4 Report
mdfile.write('<br />' + '\r\n')  # Adjust for A4 Report

mdfile.write('# Operation efficiency transition' + '\r\n')
mdfile.write('![](./usage_trans.png)')
mdfile.close()


