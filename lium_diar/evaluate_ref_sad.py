import os
import sys
from os.path import join
import os.path

lst_filename = 'lst/bnews.lst'

#ref_filename = '/home/wangry/work/data/bnews/bnews_cpd/paaa.cpd'
#det_filename = '/home/wangry/work/spk_seg/lium_diar/seg/paaa.s.seg'

ft = 0.3

lst_l = open(lst_filename).readlines()

lst = []

for i in lst_l:
    lst.append(i[:-1])

#print ref
#print det
def genref(ref_filename):
    ref = []
    ref_l = open(ref_filename).readlines()
    for index, i in enumerate(ref_l):
        time = float(i.split('     ')[-2])
        name = i.split('     ')[-1].split(' ')[-1]
        if index==0:
            #ref.append(time)
            continue
        elif name!=ref_l[index-1].split('     ')[-1].split(' ')[-1]:
            ref.append(time)
    return ref

def gendet(det_filename):
    det = []
    detdict = {}
    det_l = open(det_filename).readlines()
    for i in det_l:
        each = i[:-1].split(' ')
        detdict[float(each[1])] = each
    #print sorted(detdict)

    detdict = [(float(k),float(detdict[k][2]),detdict[k][4]) for k in sorted(detdict)]
    for i, each in enumerate(detdict):
        if i==0:
            continue
        if each[2]!=detdict[i-1][2]:
            det.append(each[0])
    #print detdict
    return det

def gensad(sad_filename):
    sad = []
    fin_sad = open(sad_filename)
    lines_sad = fin_sad.readlines()
    for i in lines_sad:
        sad.append(float(i[:8]))
        sad.append(float(i[8:-1]))
    return sad

def cal_singal(ref_filename, det_filename, sad_filename):
    #ref_l = open(ref_filename).readlines()
    #det_l = open(det_filename).readlines()
    ref = []
    det = []
    sad = gensad(sad_filename)
    ref = genref(ref_filename)
    det = gendet(det_filename)
    #ref = ref+sad
    '''
    for i in det_l:
        each = i[:-1].split(' ')
        if float(each[1])==0:
            continue
        det.append(float(each[1]))
    '''

    #print ref
    det.sort()
    #print det
    #false alarm
    false_alarm = 0
    right_alarm = 0
    for i in det:
        shot = 0
        for j in ref:
            if abs(i-j)<=ft:
                #print 'right alarm',i, j
                right_alarm += 1
                shot = 1
                break
        if shot==0:
            false_alarm += 1
            #print 'false alarm',i, j

    #print false_alarm
    #print right_alarm

    #miss detection
    miss_detection = 0
    right_detection = 0
    for i in ref:
        shot = 0
        for j in det:
            if abs(i-j)<=ft:
                right_detection += 1
                shot = 1
                break
        if shot==0:
            miss_detection += 1

    #print miss_detection
    #print right_detection
    return len(ref),len(det), false_alarm, miss_detection, right_alarm


def test(winlen, winshift, l, h, type):
    total = 0
    det_total = 0
    false_alarm = 0
    miss_detection = 0
    right_alarm = 0

    #print cal_singal(ref_filename, det_filename)
    for i in lst:
        ref_filename = '/home/wangry/work/data/bnews/bnews_ref/'+i+'.ref'
        sad_filename = '/home/wangry/work/data/bnews/bnews_sad/'+i+'.sad'
        #det_filename = '/home/wangry/work/spk_seg/lium_diar/bnews_BIC_25_10_1_1/'+i+'.s.seg'
        det_filename = '/home/wangry/work/spk_seg/lium_diar/bnews_BIC_'+winlen+'_'+winshift+'_'+l+'_'+h+'/'+i+'.'+type+'.seg'
        #print "==========="+i
        cal =  cal_singal(ref_filename, det_filename, sad_filename)
        #print cal
        total += cal[0]
        det_total +=  cal[1]
        false_alarm += cal[2]
        miss_detection += cal[3]
        right_alarm += cal[4]

    print 'total:',total, 'detected:',det_total, 'false alarm:',false_alarm, 'miss detection:',miss_detection, 'right detected:', right_alarm

    FAR = float(false_alarm)/(total+false_alarm)
    MDR = float(miss_detection)/total
    RCL = float(right_alarm)/total
    RRL = float(right_alarm)/det_total

    print 'FAR:',FAR
    print 'MDR:',MDR
    print 'RCL:',RCL
    print 'RRL:',RRL

winlen_l = [75,100,250]
l='2'
h='2'
print '//////////////l='+l+', h='+h+'///////////////'
for i in winlen_l:
    print '========winlen:',i,'=========='
    test(str(i),'100',l,h,'s')
    test(str(i),'100',l,h,'l')
    test(str(i),'100',l,h,'h.'+h)
    test(str(i),'100',l,h,'d.'+h)
    test(str(i),'100',l,h,'adj.'+h)




#print gensad('/home/wangry/work/data/bnews/bnews_sad/paaa.sad')