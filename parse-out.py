import os
import csv
import matplotlib.pyplot as plt

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
    


likertQs = ["There was enough information provided during prebrief to provide direction and encouragement.", "I clearly understood the purpose and objectives of the simulation.", "I was supported in the learning process.", "The simulation was designed for my specific level of knowledge and skills.", "The simulation allowed me to analyze my own behavior and actions.", "Feedback provided was constructive.", "There was an opportunity after the simulation to receive guidance/feedback to build knowledge and understanding.", "The scenario resembled a real-life situation.", "I actively participated in the debriefing session.", "Debriefing enhanced my learning.", "I had the chance to work with or learn from my peers or others during the simulation.", "I enjoyed how the instructor taught the simulation.", "I knew what was expected of me in my role.", "It is my responsibility as the student to learn what I need to know from this simulation activity.", "It is my course instructor's responsibility to tell me what I need to learn during class time.", "I am confident I am developing the skills and required knowledge from this simulation to practice the skills safely in the clinical setting.", "I know how to use simulation activities to learn critical aspects of nursing care." ]
saQs = ["What did you value most about this simulation experience?","What could have been improved to enhance your learning?","Is there anything else you would like us to know about your experience today?"]

def generateBody (scale, techPie, sa):
    figNum = 1
    #Likert Pies
    for s in scale:
        #count likert responses
        pieVals = [s.count(5), s.count(4), s.count(3), s.count(2), s.count(1)]
        #legend labels (including counts)
        labels = [str(pieVals[0]) + ' - Strongly Agree', str(pieVals[1]) + ' - Agree', str(pieVals[2]) + ' - Undecided', str(pieVals[3]) + ' - Disagree', str(pieVals[4]) + ' - Strongly Disagree']
        fig, ax = plt.subplots()
        ax.pie(pieVals, colors=colors, startangle=90, autopct='%1.1f%%', pctdistance=0.5)
        ax.axis('equal') #good irrational ratios
        plt.legend(labels, loc="best")
        saveFile = date.replace('/', '-') + ' ' + instructor + ' ' + scenario + ' - ' + str(figNum) + '.png'
        print('\n')
        #print ("### " + likertQs[figNum-1])
        print ('![' + likertQs[figNum-1] + '](' + saveFile + ' "Pie Chart")')
        plt.savefig( saveFile )
        plt.close()
        figNum+=1

    techColors = "tab:red", "tab:green"
    #Tech Issues Pie
    pieVals = [techPie.count("Yes"), techPie.count("No")]
    labels = [str(pieVals[0]) + ' - Yes', str(pieVals[1]) + ' - No']
    fig, ax = plt.subplots()
    ax.pie(pieVals, colors=techColors, startangle=90, autopct='%1.1f%%', pctdistance=0.5)
    ax.axis('equal') #good irrational ratios
    plt.legend(labels, loc="best")
    saveFile = date.replace('/', '-') + ' ' + instructor + ' ' + scenario + ' - ' + str(figNum) + '.png'
    print('\n')
    #print ("### " + likertQs[figNum-1])
    print ('![Did you experience technical issues during your session (e.g., manikin)?](' + saveFile + ' "Pie Chart")')
    plt.savefig( saveFile )
    plt.close()

    i = 0
    for q in sa:
#        print ('\n')
#        print ("\n \\pagebreak \n")
        print ( "\n### " + saQs[i] + '\n')
        i+=1
        for r in q:
 #           print()
            print("* " + r)

def swapPos (arr, a, b): #swap positions of a and b in arr
    arr[a], arr[b] = arr[b], arr[a]
    return arr

#Extract data from csv
allEvals = [] #init result array
with open('se.csv', newline='') as csvfile:
    seReader = csv.reader(csvfile, delimiter=',')
    for row in seReader:
        if row[21][0].isdigit(): #ignore header rows by checking date column
            if [row[21], row[20], row[18], row[19]] not in allEvals:
                #change header order to: date, instructor, pt, role 
                allEvals.append([row[21], row[20], row[18], row[19]])
            #add subarray with likert/saq result for this result
            allEvals[allEvals.index([row[21], row[20], row[18], row[19]])].append(swapPos(row[26:-1],17,18))

#treat three elements as single string for sort key
allEvals.sort(key = lambda x: (x[0][6:10]+x[0][5]+x[0][0:5]).replace('/','-') + x[1] + x[2], reverse=True)

date=''
instructor=''
scenario=''
colors = 'tab:green', 'yellow', 'tab:cyan', 'tab:orange', 'tab:red' #custom pie colors

#Loop through each eval, create pie chart, produce pandoc input
for thisEval in allEvals:

    #print(thisEval)

    if date != thisEval[0].replace('/','-') or instructor != thisEval[1] or scenario != thisEval[2]:

        #create document body with previous dataset
        if date != '':
            generateBody(scale, techPie, sa)

        #Reset vars
        scale = []
        for i in range(0,17): scale.append([])
        sa = []
        for i in range(0,3): sa.append([])
        techPie = []
        date = thisEval[0].replace('/','-')
        instructor = thisEval[1]
        scenario = thisEval[2]
        #filename
        docTitle = date + " " + instructor + " " + scenario + ".docx"
        print ( "<>:" + docTitle )
        #Print document headers
        print ( "## " + date )
        print ( "## " + instructor )
        print ( "## " + scenario )

    for i in range(0,17):
        if thisEval[4][i] != '':        #exclude the empty responses
            scale[i].append(likertNum(thisEval[4][i]))
    for i in range(18, 21):
        if thisEval[4][i] != '':
            sa[i-18].append("**" + thisEval[3] + "**: " + thisEval[4][i]) #append role to saqs
    if thisEval[4][17] != '':
        techPie.append(thisEval[4][17])
#    resI += 1

generateBody(scale, techPie, sa)
