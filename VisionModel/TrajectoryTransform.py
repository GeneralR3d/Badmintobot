import numpy as np
import pandas as pd

shiftStep = 100 
#100mm is the shift step, which is 0.1m


dataset= pd.read_excel("dataset.xlsx")

def main():
    global dataset
    # the for loop way, which does the same thing but is less cryptic
    timeZeroList=[]
    for index in dataset.index:
        if dataset.iloc[index]['time'] == 0:
            timeZeroList.append(index)
    
    for startIndex in timeZeroList:
        index = startIndex
        # this condition in while loop will be false when we index+1 is a zero. Since zero minus any value before will be negative. 
        #This way we stop at index, which is before zero.
        while dataset.iloc[index+1]['time'] - dataset.iloc[index]['time'] > 0:
            index +=1
        new= dataset.iloc[startIndex: index+1] #recall python list slicing doesnt include the end point
        transformX(new,100,4000) #lower range is 0, need plus 100
        print(dataset)
        transformY(new,-2490,2590) #lower range is -2590, need plus 100
        print(dataset)
        transformZ(new,200,3000) #lower range is 100, need plus 100


    dataset.to_excel('datasetTBFilled.xlsx',index=False)


def getLastLabel():
    return dataset.iloc[-1]['label']


def transformX(originalDF,inclusiveMin,inclusiveMax):
    global dataset
    
    currentDF= originalDF
    while currentDF.iloc[0]["LocationX"] > inclusiveMin:
        newDF=currentDF.copy(deep=True)
        newDF['LocationX'] = (newDF['LocationX']-shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF
        
    currentDF = originalDF
    while currentDF.iloc[0]["LocationX"] < inclusiveMax:
        newDF=currentDF.copy(deep=True)
        newDF['LocationX'] = (newDF['LocationX']+shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF

def transformY(originalDF,inclusiveMin,inclusiveMax):
    global dataset
    
    currentDF= originalDF
    while currentDF.iloc[0]["LocationY"] > inclusiveMin:
        newDF=currentDF.copy(deep=True)
        newDF['LocationY'] = (newDF['LocationY']-shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF
        
    currentDF = originalDF
    while currentDF.iloc[0]["LocationY"] < inclusiveMax:
        newDF=currentDF.copy(deep=True)
        newDF['LocationY'] = (newDF['LocationY']+shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF


def transformZ(originalDF,inclusiveMin,inclusiveMax):
    global dataset
    
    currentDF= originalDF
    while currentDF.iloc[0]["LocationZ"] > inclusiveMin:
        newDF=currentDF.copy(deep=True)
        newDF['LocationZ'] = (newDF['LocationZ']-shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF
        
    currentDF = originalDF
    while currentDF.iloc[0]["LocationZ"] < inclusiveMax:
        newDF=currentDF.copy(deep=True)
        newDF['LocationZ'] = (newDF['LocationZ']+shiftStep)
        newDF['label'] = getLastLabel() + 1
        dataset=pd.concat([dataset,newDF],ignore_index=True)
        currentDF= newDF


if __name__ == '__main__':
    main()