
import matplotlib.pyplot as plt
import numpy as np
import json

def s_time(end,start):
    result =end-start
    return result

with open('final_output.json') as f:
   data = json.load(f)
   print(data)
time_arrA=[]
time_arrB=[]
label=[]
for i in data:
    s=i['speaker']
    label.append(s)
    start_time=i['start']/1000
    end_time=i['end']/1000

    # print(label,start_time,end_time)


    if i['speaker']=='A':
        
        ta=s_time(end_time,start_time)
        time_arrA.append(ta)

    elif i['speaker']=='B':
        tb=s_time(end_time,start_time)
        time_arrB.append(tb)

# print(time_arrA)
# print(time_arrB)
# print(label)

output = []
for x in label:
    if x not in output:
        output.append(x)
# print(output)


sumA=0
for i in range(0, len(time_arrA)):    
   sumA = sumA + time_arrA[i];    
     
# print(sumA); 

sumB=0
for i in range(0, len(time_arrB)):    
   sumB = sumB + time_arrB[i];    
     
# print(sumB); 

total_time=sumA+sumB
# print(total_time)

chartA=round(sumA*100/total_time)
chartB=round(sumB*100/total_time)

# print(chartA,chartB)

y=[]
y.append(chartA)
y.append(chartB)

# y = np.array([35, 25, 25, 15])
mylabels = output

plt.pie(y, labels = mylabels)
plt.legend(title = "Speakers")
# plt.setp(autotexts, size = 8, weight ="bold")
plt.show() 