# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
# packages

import json
from os import listdir
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import sys
                
vectorizer=TfidfVectorizer(analyzer='word', binary=False, decode_error='strict',
        encoding='utf-8', input='content',
        lowercase=True, max_df=1.0, max_features=None, min_df=1,
        ngram_range=(1, 1), preprocessor=None, stop_words=None,
        strip_accents=None, token_pattern='(?u)\\b\\w\\w+\\b',
        tokenizer=None, vocabulary=None)


# variables
lenght=0;
tempProfile="";

#loading .json files in utf-8 encoding and convert them to dictionaries inside list
def readJson(file,path):
   
    jsonFile = open(path + file,encoding='utf-8');
    jsonString=jsonFile.read();
    data  = json.loads(jsonString)
    
    return data
    


def analizeProfiles(path):
    for fieldType in ['"industry"','"positions"','"specialties"','"summary"','"skills"','"educations"']:
        numberOfFields=0
        usefulFields=0
        numberOfUsers=0
        for file in listdir(path):
            if file.endswith(".json"):
                lista=fileToList(file,path);

                for userProfile in lista[0]:
                    numberOfUsers=numberOfUsers+1

                    for profileField in userProfile:
                        numberOfFields=numberOfFields+1
                        if profileField==fieldType:
                            usefulFields=usefulFields+1
                            break

        print(fieldType+"  "  +str(numberOfUsers)+"  " +str(usefulFields)+"  " +str(usefulFields/numberOfUsers))

    return usefulFields        

def detectFields(path,frequency):
    numberOfFiles=0
    numberOfFields=0
    numberOfUsers=0
    fieldType=[]
    for file in listdir(path):
        numberOfFiles=numberOfFiles+1
      
        if file.endswith(".json"):
            data=readJson(file,path);  
            #reades each userprofile from the list
            for userProfile in data:
                numberOfUsers=numberOfUsers+1
                # reads each key in userprofile dictionary
                for profileField in userProfile:
                    numberOfFields=numberOfFields+1
                    fieldType.append(profileField)
              
    counts = collections.Counter(fieldType) 
    sortedList = sorted(fieldType, key=lambda x: -counts[x])   #Sorts the fieldTypes list by field frequency
    cleanList = []
    duplicatedCounts=[]
    output=[]
    for item in sortedList:
        # Remove the duplicates and count their frequencies
        if item in cleanList:
            duplicatedCounts[cleanList.index(item)]+=1
        if item not in cleanList:
            cleanList.append(item);
            duplicatedCounts.append(1)
            # assigns the frequency of each field to the output list        
    if frequency==1:
        for ch in range(1,len(cleanList)):
            if(duplicatedCounts[ch]>3):
                output.append([cleanList[ch],duplicatedCounts[ch]])
    if frequency==0:
        output=cleanList
                    
    return output

def detectSubFields(path,frequency):
    numberOfFiles=0
    numberOfFields=0
    numberOfUsers=0
    fieldType=[]
    for file in listdir(path):
        numberOfFiles=numberOfFiles+1      
        if file.endswith(".json"):
            data=readJson(file,path);
        
            #reades each userprofile from the list
            for userProfile in data:
                numberOfUsers=numberOfUsers+1
                # reads each key in userprofile dictionary
                for profileField in userProfile:
                    if profileField in ['educations','positions']:
                        keys=userProfile[profileField]
                        if not isinstance(keys, str):
                            for sections in keys:
                                if not isinstance(sections, str):
                                    for subField in sections:
                                        numberOfFields=numberOfFields+1
                                        fieldType.append(subField)
                                else:
                                    numberOfFields=numberOfFields+1
                                    fieldType.append(sections)
                                    
              
    counts = collections.Counter(fieldType) 
    sortedList = sorted(fieldType, key=lambda x: -counts[x])   #Sorts the fieldTypes list by field frequency
    cleanList = []
    duplicatedCounts=[]
    output=[]
    for item in sortedList:
        # Remove the duplicates and count their frequencies
        if item in cleanList:
            duplicatedCounts[cleanList.index(item)]+=1
        if item not in cleanList:
            cleanList.append(item);
            duplicatedCounts.append(1)
            # assigns the frequency of each field to the output list        
    if frequency==1:
        for ch in range(1,len(cleanList)):
            if(duplicatedCounts[ch]>3):
                output.append([cleanList[ch],duplicatedCounts[ch]])
    if frequency==0:
        output=cleanList
                    
    return output

def sortFieldsByContent(profiles,fieldKey,frequency):
    numberOfFields=0
    numberOfUsers=0
    keyName=[]
       
	#reades each userprofile from the list
    for userProfile in profiles:
        numberOfUsers=numberOfUsers+1
        # reads each key in userprofile dictionary
        
        numberOfFields=numberOfFields+1
        if userProfile[fieldKey] in ['Greater New York City Area', 'London, United Kingdom', 'Greater Chicago Area', 'San Francisco Bay Area', 'Greater Los Angeles Area', 'Toronto, Canada Area', 'Greater Atlanta Area', 'Washington D.C. Metro Area', 'Greater Boston Area',  'United Kingdom', 'Dallas/Fort Worth Area', 'Greater Philadelphia Area', 'Houston, Texas Area',  'Greater Detroit Area',  'Greater Seattle Area', 'Miami/Fort Lauderdale Area', 'Melbourne Area, Australia', 'Sydney Area, Australia', 'Orange County, California Area',  'United States', 'Venezuela', 'Montreal, Canada Area','Orlando, Florida Area', 'Greater Denver Area',  'Ohio Area',   'Madrid Area, Spain',  'New York, New York', 'Raleigh-Durham, North Carolina Area', 'London, Greater London, United Kingdom', 'Greater San Diego Area', 'Canada', 'Greater St. Louis Area']:
            keyName.append(userProfile[fieldKey])
   
    counts = collections.Counter(keyName) 
    sortedList = sorted(keyName, key=lambda x: -counts[x])   #Sorts the fieldTypes list by field frequency

    cleanList = []
    duplicatedCounts=[]
    output=[]
    for item in sortedList:
        # Remove the duplicates and count their frequencies
        if item in cleanList:
            duplicatedCounts[cleanList.index(item)]+=1
        if item not in cleanList:
            cleanList.append(item);
            duplicatedCounts.append(1)
            # assigns the frequency of each field to the output list        
    if frequency==1:
        for ch in range(1,len(cleanList)):
            if(duplicatedCounts[ch]>3):
                output.append([cleanList[ch],duplicatedCounts[ch]])
    if frequency==0:
        output=cleanList    
    print(len(sortedList))    
    return output

def checkFields(ourList,fieldTypes):
    checked=0
    #numberOfUsers=numberOfUsers+1
    usefulFields=0
    #print("numberOfUsers = ",numberOfUsers)
    for item in fieldTypes:
        for fields in ourList:
            if fields==item:
                #print(item)
                usefulFields+=1
                #print(usefulFields)
                if usefulFields==len(fieldTypes):
                    checked=1
                    break
                continue    
    return checked    
    
def filterCompleteProfiles(path):
    numberOfFiles=0
    numberOfUsers=0
    fieldType=[]
    checked=1
    completeList=[]
    for file in listdir(path):
        numberOfFiles=numberOfFiles+1
        print(numberOfFiles)        
        if file.endswith(".json"):
            data=readJson(file,path);
        
            #reades each userprofile from the list
            for userProfile in data:
                #numberOfUsers=numberOfUsers+1
                checked=0
                if (checkFields(userProfile,['industry','positions','educations','skills','summary','location'])):
                # reads each key in userprofile dictionary

                    if userProfile['location'] in ['Greater New York City Area', 'London, United Kingdom', 'Greater Chicago Area', 'San Francisco Bay Area', 'Greater Los Angeles Area', 'Toronto, Canada Area', 'Greater Atlanta Area', 'Washington D.C. Metro Area', 'Greater Boston Area',  'United Kingdom', 'Dallas/Fort Worth Area', 'Greater Philadelphia Area', 'Houston, Texas Area',  'Greater Detroit Area',  'Greater Seattle Area', 'Miami/Fort Lauderdale Area', 'Melbourne Area, Australia', 'Sydney Area, Australia', 'Orange County, California Area',  'United States', 'Venezuela', 'Montreal, Canada Area','Orlando, Florida Area', 'Greater Denver Area',  'Ohio Area',   'Madrid Area, Spain',  'New York, New York', 'Raleigh-Durham, North Carolina Area', 'London, Greater London, United Kingdom', 'Greater San Diego Area', 'Canada', 'Greater St. Louis Area']:    
                        for profileField in userProfile:
                            if profileField=="positions":
                                keys=userProfile[profileField]
                                if not isinstance(keys, str):
                                    for sections in keys:
                                        if not isinstance(sections, str):
                                            checked=(checkFields(sections,['title','company-name','summary']))

                                            if not checked:
                                                break

                                    if not checked:
                                        break # double break

                            if profileField=="educations":
                                keys=userProfile[profileField]
                                if not isinstance(keys, str):
                                    for sections in keys:
                                        if not isinstance(sections, str):
                                            checked=(checkFields(sections,['school-name', 'degree', 'field-of-study']))
                                            if not checked:
                                                break
                                
                                            
                                    if not checked:
                                        break # double break
                            
                    if checked==1:
                        numberOfUsers+=1           
                        completeList.append(userProfile)

    print(numberOfUsers)  
    return completeList    

def extractFields(profiles,userIndex):

    fieldsList=dict()
    userProfile=profiles[userIndex]

    for profileField in userProfile:
        if profileField in ['industry','summary','skills']:
            fieldsList[profileField]=userProfile[profileField]
        
        if profileField=="positions":          
            tempList1={}
            tempList2=[]
            for sections in userProfile[profileField]:

                for subField in sections:
                    if subField in ['title','company-name']:
                        tempList1.setdefault(subField, []).append(sections[subField])

                    elif subField=='summary':
                        #print(userProfile[profileField].index(sections))
                        tempList2.append(sections[subField])
                        fieldsList['positions-summary']=tempList2
                        #print("check2")
                        
            for subField in ['title','company-name']:
                        fieldsList[subField]=tempList1[subField]                     
                   
        if profileField=="educations":
            tempList1={}            
            for sections in userProfile[profileField]:

                for subField in sections:
                    if subField in ['school-name', 'degree', 'field-of-study']:
                        tempList1.setdefault(subField, []).append(sections[subField])
                        
            for subField in ['school-name', 'degree', 'field-of-study']:
                        fieldsList[subField]=tempList1[subField]    

    return fieldsList

def convertProfiles(file,outputName,path):
    convertedprofiles=[]
    profiles=readJson(file,path)
    for userIndex in profiles:
        
        fields=extractFields(profiles,profiles.index(userIndex))
        convertedprofiles.append(fields)    
    f = open(outputName, 'w')
    json.dump(convertedprofiles, f)
    f.close()
    print(profiles.index(userIndex)+1)
    #print(convertedprofiles)
    return 1
	
def fieldToString(fieldData):
    
    #convert lists to string
    if not isinstance(fieldData, str):
        listString=(' '.join(map(str, fieldData)))
    else:
        listString=fieldData
    return listString

def compareFields(field1,field2,convertion):
    
    if convertion==1:       

        field1=fieldToString(field1)      
        field2=fieldToString(field2)
    #put field in a list
    corpus=[]
    corpus.extend((field1,field2))
    X = vectorizer.fit_transform(corpus)
    #Y=vectorizer.get_feature_names()
    similarityMatrix = X * X.T
    
    return similarityMatrix[0,1]

def profilesToString(file,outputName,path):
    counter=0
    newList=[]
    newProfile={}

    profiles=readJson(file,path)
    for userProfile in profiles:

        for fieldType in ['skills','summary','positions-summary','title','company-name','school-name','degree','field-of-study','industry']:
            #print(fieldType)

            if fieldType in userProfile:
                counter+=1
                #print(counter)
                string=fieldToString(userProfile[fieldType])

                newProfile[fieldType]=string
                #print(newProfile[fieldType])
        newList.append(newProfile)
        newProfile={}
        #print(newList)
    f = open(outputName, 'w')
    json.dump(newList, f)
    f.close()
    #print(newList)    
    return newList
                  
def compareProfiles(profiles,userIndex1,userIndex2):

    userProfile1=profiles[userIndex1]
    userProfile2=profiles[userIndex2]
    similarityVector=[0,0,0,0,0,0,0,0,0]
    counter=0
    errorCounter=0
    for fieldType in ['skills','summary','positions-summary','title','company-name','school-name','degree','field-of-study','industry']:
#        print(fieldType)
        counter+=1

        try:
#            print("counter= ",counter-1,fieldType)
            similarityVector[counter-1]=round(compareFields(userProfile1[fieldType],userProfile2[fieldType],0),4)
#            print(similarityVector[counter-1])
        except ValueError:
            errorCounter+=1
#            print("error count= ", errorCounter)

            if userProfile1[fieldType]==userProfile2[fieldType]:
                similarityVector[counter-1]=1
            else:
                similarityVector[counter-1]=0
            pass
#           print(similarityVector[counter-1])
#        else:
#            similarityVector[counter-1]=0  
    weightedSimilarity=sum(similarityVector)/len(similarityVector)
#    print("W= ",weightedSimilarity)
    #return round(weightedSimilarity,4)
    return similarityVector

def compareAllProfiles(file,outputName,path):
    
    profiles=readJson(file,path)
    matrixSize=len(profiles)
    similarityMatrix=np.zeros((10,matrixSize, matrixSize))
    
    for row in range (0,matrixSize):
        print(row,end=",")
        for col in range (0,matrixSize):

 
            similarity=compareProfiles(profiles,row,col)

            for fieldMatrix in range (0,8):
                
                similarityMatrix[fieldMatrix][row][col]=similarity[fieldMatrix]
    
    
            weightedSimilarity=sum(similarity)/len(similarity)
            round(weightedSimilarity,4)                   
            similarityMatrix[9][row][col]=weightedSimilarity    
    #f = open(outputName)
    np.save(outputName, similarityMatrix)
    #f.close()
    
    return similarityMatrix

def cutListFile(file,output,path,cutSize):
    profiles=readJson(file,path)
    newList=[]
    for i in range (0,cutSize):
        print(i)
        newList.append(profiles[i])
    f = open(output, 'w',encoding='utf-8')
    json.dump(newList, f,ensure_ascii=False)
    f.close()
    return f     

def compareFiles(file1,file2):
    f1=open(file1,encoding='utf-8')
    f2=open(file2,encoding='utf-8')
    counter=0
    while True:
        counter+=1
#        print(counter)
        ch1=f1.read(1)
        ch2=f2.read(1)
        if counter%1000==0:
            print(counter)
        if ch1!=ch2:
            print("bad character detected!")
            print(counter)
            print(ch1,ch2)
            break


    return 0   
        
