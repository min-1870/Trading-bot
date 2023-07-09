import pandas as pd
from Bot import reset
import Trade as bi
import sys
import time
import random

emas = ['EMA', 'DEMA', 'TEMA']
smas = ['SMA']
others = ['PRICE']

sma_spans = [10, 30, 50]
ema_spans = [3]


#=========== what you can fix ============
max_span = 15
money_value = 100
file_name = 'BTCUSDT-4h-2021-12.csv'
#=========================================

partial_combinations = []
temp_partial_combinations = []
combinations = []

results = pd.DataFrame({'Profit (%)' : [],'Winrate (%)' : [], 'File' : [], 'Buy_1' : [], 'Buy_value_1' : [], 'Buy_2' : [], 'Buy_value_2' : [], 'Sell_1' : [], 'Sell_value_1' : [], 'Sell_2' : [], 'Sell_value_2' : []})
progress = 0

#========== generate all the possible combinations ==========

for sign_1 in others + smas + emas:
    
    for span_1 in list(set(sma_spans+ema_spans)):

        for sign_2 in others + smas + emas:

            for span_2 in list(set(sma_spans+ema_spans)):

                partial_combinations.append([sign_1, span_1, sign_2, span_2])
    

#========== filter duplicated & nonsense combinations ==========

for i in range(len(partial_combinations)):
    if partial_combinations[i][0] == 'PRICE':
        partial_combinations[i][1] = 0 #price does not need any value

    if partial_combinations[i][2] == 'PRICE':
        partial_combinations[i][3] = 0 #price does not need any value

    if (partial_combinations[i][0] in smas and partial_combinations[i][1] not in sma_spans) or (partial_combinations[i][0] in emas and partial_combinations[i][1] not in ema_spans):
        partial_combinations[i] = [None, None, None, None] 

    if (partial_combinations[i][2] in smas and partial_combinations[i][3] not in sma_spans) or (partial_combinations[i][2] in emas and partial_combinations[i][3] not in ema_spans):
        partial_combinations[i] = [None, None, None, None] 

    if partial_combinations[i][0] == partial_combinations[i][2] and partial_combinations[i][1] == partial_combinations[i][3]:
        partial_combinations[i] = [None, None, None, None] #mark the case has same signs 
    
temp_partial_combinations = partial_combinations[:]
partial_combinations.clear()

for i in temp_partial_combinations:
    if i != [None, None, None, None] and i not in partial_combinations:
        partial_combinations.append(i) #remove all nonsense combinations and duplicated combinations

#========== generate full combinations ==========

for i in partial_combinations:
    for j in partial_combinations:
        if i != j:
            combinations.append([i,j]) #append only for different buy and sell combinations

random.shuffle(combinations) #spread the combinations
    
#========== time to drive the car ==========

c = 0
amounts = len(combinations)
for i in combinations:
    result = bi.run_test(money_value, 'Datas\\'+file_name, i)
    results = results.append(pd.DataFrame({'Profit (%)' : [result[0]],'Winrate (%)' : [result[1]], 'File' : [result[2]], 'Buy_1' : [result[3]], 'Buy_value_1' : [result[4]], 'Buy_2' : [result[5]], 'Buy_value_2' : [result[6]], 'Sell_1' : [result[7]], 'Sell_value_1' : [result[8]], 'Sell_2' : [result[9]], 'Sell_value_2' : [result[10]]}), ignore_index = True)
 
    if c % 50 == 0:
        results.to_csv (r'D:\Users\Documents\Develop\Programming\Python\Trading_bot\Simulation_results.csv', index = False, header=True)

    progress += 100/amounts
    time = (amounts - c) * 0.2 / 60
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line 
    print("PROGRESS : " + str(round(progress,0)) + '%          TESTS : '+ str(amounts - c) +'          ' + str(time)[0:5] + ' minutes left..')
    c += 1

#========== let's extract the dataframe into csv ==========

results.to_csv (r'D:\Users\Documents\Develop\Programming\Python\Trading_bot\Simulation_results.csv', index = False, header=True)


#print(bi.run_test(money_value, file_name, [['SMA', 10,'PRICE', None], ['PRICE', None,'TEMA', 15]]))


