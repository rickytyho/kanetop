import numpy as np
from config import Filenames,InputFieldNames,Parameters
import os
import pandas as pd
from sklearn import preprocessing

class Configuration:
    def __init__(self,fileName,inputFilePath,outputFilePath):
        self.inputFilePath = inputFilePath
        self.outputDirectory = outputFilePath
        self.partitionFilePath = os.path.abspath(''.join([self.outputDirectory,'/', Filenames.partition_output_file_name]))
        self.ordersFilePath = os.path.abspath(''.join([self.outputDirectory,'/', Filenames.orders_output_file_name]))
    def initialize_settings(self,settings):
        self.productionDuration=settings[0]
        self.capacityPercentage=settings[1]
        self.dateSimilarityWeight=settings[2]
        self.processWeight=settings[3]
    def readData(self,settings):
        self.initialize_settings(settings)
        self.orderData = pd.read_excel(self.inputFilePath, sheet_name=0).to_dict()
        self.supplierData = pd.read_excel(self.inputFilePath, sheet_name=1).to_dict()
        self.historicalData = pd.read_excel(self.inputFilePath, sheet_name=2).to_dict()
        self.paramWeight = preprocessing.normalize([np.array([self.dateSimilarityWeight, self.processWeight])])

class Order:
    def __init__(self, orderID, IEValue,styleID,customerName, numPieces, color,clothingType, ProductionDays,deliveryDate,machineType,historicalData):
        self.orderID = orderID
        self.IEValue = IEValue
        self.styleID=styleID
        self.customerName=customerName
        self.numPieces = numPieces
        self.color=color
        self.clothingType = clothingType
        self.ProductionDays = ProductionDays
        self.deliveryDate = deliveryDate
        self.historicalData=historicalData
        self.deliveryGroup=self.dateGroup()
        self.partitionStatus='False'
        self.repeatStatus=self.isRepeat()
        self.manNeeded=(numPieces)/(ProductionDays*IEValue)
        self.machineType=machineType
        self.IERange=self.orderRange()

    def partitionOrder(self,SupplierName):
        self.partitionStatus='True'
        self.givenFactory=SupplierName
    def isRepeat(self):
        historicalIndexID=np.array([elem for elem in range(len(self.historicalData[InputFieldNames.historicalStyleNumber])) if self.historicalData[InputFieldNames.historicalStyleNumber][elem]==self.styleID])
        if len(historicalIndexID)>0:
            historicalIndexID=historicalIndexID[0]
            return np.array([self.historicalData.get(InputFieldNames.historicalOrdersNumber)[historicalIndexID],self.historicalData.get(InputFieldNames.historicalSupplierName)[historicalIndexID]])
        else:
            return np.array(['False'])
    def dateGroup(self):
        day=self.deliveryDate.day
        if day<=10:
            return 1
        elif day<=20:
            return 2
        else:
            return 3
    def orderRange(self):
        if self.IEValue in Parameters.lowIERange:
            return 1
        elif self.IEValue in Parameters.middleIERange:
            return 2
        else:
            return 3
    def partitionFail(self):
        self.partitionStatus = 'Fail'

class Supplier:
    def __init__(self,name,rank,typeCapability,startingMan,IELevel,processType,machineType):
        self.name=name
        self.rank=rank
        self.typeCapability=typeCapability
        self.startingMan=startingMan
        self.remainingMan=startingMan
        self.IEGroup=IELevel
        self.IELevel=self.IERange()
        self.processType=processType
        self.processRank=len(processType.split('-'))
        self.machineType=machineType
        self.givenOrder=[]
        self.givenIE=[]
        self.givenDateGroup=[]
        self.givenPieces=[]
    def IERange(self):
        if self.IEGroup==Parameters.lowRange:
            return np.array([1])
        elif self.IEGroup==Parameters.midRange:
            return np.array([2,3])
        else:
            return np.array([1,2,3])

    def partitionOrder(self,order):
        self.remainingMan=self.remainingMan-order.manNeeded
        self.givenOrder.append(order)
        self.givenIE.append(order.IEValue)
        self.givenDateGroup.append(order.deliveryGroup)
        self.givenPieces.append(order.numPieces)
    def generateRank(self,newOrder,repeatDateWeight,processWeight):


        def generateRepeatedDateGroup(newOrder, repeatDateWeight,givenDateGroup):
            if newOrder.deliveryGroup == 1:
                numRepeatedDate = 4 - givenDateGroup.count(1)
            elif newOrder.deliveryGroup == 2:
                numRepeatedDate = 4 - givenDateGroup.count(2)
            else:
                numRepeatedDate = 4 - givenDateGroup.count(3)
            return preprocessing.normalize([np.array([numRepeatedDate, 3])])[0][0] * repeatDateWeight

        def processRank(processRank,processWeight):
            return processRank*processWeight

        Rank=generateRepeatedDateGroup(newOrder,repeatDateWeight,self.givenDateGroup)+processRank(self.processRank,processWeight)
        return Rank



class SupplierPartition:
    def __init__(self,supplierData):
        self.supplierData=supplierData
        self.supplierName=supplierData.name
        self.startingMan =supplierData.startingMan
        self.remainingMan =supplierData.remainingMan
        self.orderID =[]
        self.orderIE=[]
        self.orderPieces =[]
        self.orderColor =[]
        self.orderStyle =[]
        self.orderDeliveryDate =[]
        self.orderCustomer =[]
        self.orderRepeatStatus=[]

    def getPartitionAverage(self):
        if len(self.orderIE)>0:
            self.IEAverage = sum(self.orderIE) / float(len(self.orderIE))
        else:
            self.IEAverage=0
    def getTotalOrderSize(self):
        self.orderPiecesTotal = sum(self.orderPieces)
    def portData(self):
        for order in self.supplierData.givenOrder:
            self.orderID.append(order.orderID)
            self.orderIE.append(order.IEValue)
            self.orderPieces.append(order.numPieces)
            self.orderColor.append(order.color)
            self.orderStyle.append(order.styleID)
            self.orderDeliveryDate.append(order.deliveryDate)
            self.orderCustomer.append(order.customerName)
            self.orderRepeatStatus.append(order.repeatStatus[0])
        self.getPartitionAverage()
        self.getTotalOrderSize()








