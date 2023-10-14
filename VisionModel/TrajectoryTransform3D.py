import numpy as np
import pandas as pd

shiftStep = 150
#100mm is the shift step, which is 0.1m



dataset= pd.read_excel("datasetModified.xlsx")

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


        reachedinclusiveMinX = False
        reachedinclusiveMaxX = False
        reachedinclusiveMinY = False
        reachedinclusiveMaxY = False
        reachedinclusiveMinZ = False
        reachedinclusiveMaxZ = False
        returnedDFX = None
        returnedDFY = None
        returnedDFZ = None

        # start of X loop
        newX = new
        while True:
            returnedDFX, reachedinclusiveMinX, reachedinclusiveMaxX = transformX(newX,100,4000,reachedinclusiveMinX,reachedinclusiveMaxX) #lower range is 0, need plus 100
            
            if returnedDFX is None: 
                break
            
            dataset=pd.concat([dataset,returnedDFX],ignore_index=True)

            # start of Y loop
            newY = returnedDFX
            while True:
                returnedDFY, reachedinclusiveMinY, reachedinclusiveMaxY = transformY(newY,-2490,2590, reachedinclusiveMinY, reachedinclusiveMaxY) #lower range is -2590, need plus 100
                
                if returnedDFY is None:
                    break

                dataset=pd.concat([dataset,returnedDFY],ignore_index=True)
                

                # start of Z loop
                newZ = returnedDFY
                while True:
                    returnedDFZ, reachedinclusiveMinZ, reachedinclusiveMaxZ = transformZ(newZ,200,3000, reachedinclusiveMinZ, reachedinclusiveMaxZ) #lower range is 100, need plus 100

                    if returnedDFZ is None:
                        break
                    
                    dataset=pd.concat([dataset,returnedDFZ],ignore_index=True)
                    newZ= returnedDFZ
                # runs after Z loop terminates
                newY = returnedDFY

            # runs after Y loop terminates
            newX = returnedDFX


    dataset.to_excel('datasetTBFilled3D.xlsx',index=False)


def getLastLabel():
    return dataset.iloc[-1]['label']


def transformX(originalDF,inclusiveMin,inclusiveMax, reachedinclusiveMin, reachedinclusiveMax):
    '''
    returns the new altered X dataframe if either inclusiveMin or inclusiveMax has not been reached, else return None
    '''
    if not reachedinclusiveMin:
        if originalDF.iloc[0]["LocationX"] > inclusiveMin:
            newDF=originalDF.copy(deep=True)
            newDF['LocationX'] = (newDF['LocationX']-shiftStep)
            newDF['label'] = getLastLabel() + 1
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMin = True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    elif not reachedinclusiveMax:
        if originalDF.iloc[0]["LocationX"] < inclusiveMax:
            newDF=originalDF.copy(deep=True)
            newDF['LocationX'] = (newDF['LocationX']+shiftStep)
            newDF['label'] = getLastLabel() + 1
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMax= True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    else:
        return None,reachedinclusiveMin, reachedinclusiveMax

        
    


def transformY(originalDF,inclusiveMin,inclusiveMax, reachedinclusiveMin, reachedinclusiveMax):
    '''
    returns the new altered Y dataframe if either inclusiveMin or inclusiveMax has not been reached, else return None
    '''
    if not reachedinclusiveMin:
        if originalDF.iloc[0]["LocationY"] > inclusiveMin:
            newDF=originalDF.copy(deep=True)
            newDF['LocationY'] = (newDF['LocationY']-shiftStep)
            newDF['label'] = getLastLabel() + 1
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMin = True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    elif not reachedinclusiveMax:
        if originalDF.iloc[0]["LocationY"] < inclusiveMax:
            newDF=originalDF.copy(deep=True)
            newDF['LocationY'] = (newDF['LocationY']+shiftStep)
            newDF['label'] = getLastLabel() + 1
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMax= True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    else:
        return None,reachedinclusiveMin, reachedinclusiveMax

def transformZ(originalDF,inclusiveMin,inclusiveMax, reachedinclusiveMin, reachedinclusiveMax):
    '''
    returns the new altered Z dataframe if either inclusiveMin or inclusiveMax has not been reached, else return None.
    ONLY for Z, filter out all those transformed Z coordinate values which are less than 0, since they are impossible. 
    This also means all those trajectories will be truncated.
    '''
    if not reachedinclusiveMin:
        if originalDF.iloc[0]["LocationZ"] > inclusiveMin:
            newDF=originalDF.copy(deep=True)
            newDF['LocationZ'] = (newDF['LocationZ']-shiftStep)
            newDF['label'] = getLastLabel() + 1
            newDF = newDF[newDF['LocationZ']>0]
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMin = True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    elif not reachedinclusiveMax:
        if originalDF.iloc[0]["LocationZ"] < inclusiveMax:
            newDF=originalDF.copy(deep=True)
            newDF['LocationZ'] = (newDF['LocationZ']+shiftStep)
            newDF['label'] = getLastLabel() + 1
            newDF = newDF[newDF['LocationZ']>0]
            return newDF, reachedinclusiveMin, reachedinclusiveMax
        else:
            reachedinclusiveMax= True
            return originalDF, reachedinclusiveMin, reachedinclusiveMax
    else:
        return None,reachedinclusiveMin, reachedinclusiveMax

if __name__ == '__main__':
    main()