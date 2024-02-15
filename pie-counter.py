import csv
import matplotlib.pyplot as plt
import datetime

#convert response into corresponding numerical value
def likertNum (likertStr):
    if likertStr == 'Strongly Agree':
        return 5
    elif likertStr == 'Agree':
        return 4
    elif likertStr == 'Undecided':
        return 3
    elif likertStr == 'Disagree':
        return 2
    elif likertStr == 'Strongly Disagree':
        return 1

likertQs = ["I clearly understood the purpose and objectives of the simulation.", "I was supported in the learning process.", "The simulation was designed for my specific level of knowledge and skills.", "I was able to self-reflect on the choices I made during debriefing.", "Feedback provided was constructive.", "The scenario resembled a real-life situation.", "I actively participated in the debriefing session.", "Debriefing enhanced my learning.", "I had the chance to work with my peers or others during the simulation.", "I enjoyed how the simulation was conducted.", "I knew what was expected of me in my role.", "I am confident I am developing the skills and knowledge from this simulation necessary for the clinical setting.", "I know how to use simulation activities to learn critical aspects of skills."]
saQs = ["What did you value most about this simulation experience?","What could have been improved to enhance your learning?","Is there anything else you would like us to know about your experience today?"]

def generateBody (scale, sa):
    pieVals = [0, 0, 0, 0, 0]
    for s in scale:
        #count likert responses
        pieVals[0] += s.count(5)
        pieVals[1] += s.count(4)
        pieVals[2] += s.count(3)
        pieVals[3] += s.count(2)
        pieVals[4] += s.count(1)
        #legend labels (including counts)
    labels = [str(pieVals[0]) + ' - Strongly Agree', str(pieVals[1]) + ' - Agree', str(pieVals[2]) + ' - Undecided', str(pieVals[3]) + ' - Disagree', str(pieVals[4]) + ' - Strongly Disagree']
    fig, ax = plt.subplots()
    ax.pie(pieVals, colors=colors, startangle=90, autopct='%1.1f%%', pctdistance=0.5)
    ax.axis('equal') #good irrational ratios
    plt.legend(labels, loc="best")
    saveFile = scenario + '.png'
    print ('![' + scenario + '](' + saveFile + ' "Pie Chart")')
    for likert in pieVals: print(likert, end='\t')
    print('\n')
    plt.savefig( saveFile )
    plt.close()
    i = 0
    for q in sa:
        print ( "\n### " + saQs[i] + '\n')
        i+=1
        for r in q:
            print("* " + r)
 


#Extract data from csv
allEvals = [] #init result array
with open('se.csv', newline='') as csvfile:
    seReader = csv.reader(csvfile, delimiter=',')
    for row in seReader:
        if row[20][0].isdigit(): #ignore header rows by checking date column
            if [row[20], row[19], row[18]] not in allEvals:
                allEvals.append([row[20], row[19], row[18]])
            allEvals[allEvals.index([row[20], row[19], row[18]])].append(row[25:])
        #print(', '.join(row))

allEvals.sort(key = lambda x: x[2])


scenario=''
colors = 'tab:green', 'yellow', 'tab:cyan', 'tab:orange', 'tab:red' #custom pie colors

semesterStart = datetime.datetime(2022, 1, 1)
semesterEnd = datetime.datetime(2022, 5, 30)
lastDate=semesterStart
#Loop through each eval, create pie chart, produce pandoc input
for thisEval in allEvals:
    thisDate = datetime.datetime(int(thisEval[0][6:10]), int(thisEval[0][0:2]), int(thisEval[0][3:5]))
    if thisDate > semesterStart and thisDate < semesterEnd:
        if thisDate != lastDate:
            print(thisDate)
            lastDate = thisDate
        if scenario != thisEval[2]:
            #create document body with previous dataset
            if scenario != '':
                print(scenario)
                generateBody(scale, sa)

            #Reset vars
            scale = []
            for i in range(0,13): scale.append([])
            sa = []
            for i in range(0,3): sa.append([])
            scenario = thisEval[2]
            print ( "## " + scenario )

        for i in range(0,13):
            if thisEval[3][i] != '':        #exclude the empty responses
                scale[i].append(likertNum(thisEval[3][i]))
        for i in range(13, 16):
            if thisEval[3][i] != '':
                sa[i-13].append(thisEval[3][i])
    #    resI += 1

generateBody(scale,sa)
