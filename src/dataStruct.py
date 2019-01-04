import numpy as np

class Order:
    def __init__(self, orderID, IEValue,styleID,customerName, numPieces, color,clothingType, ProductionDays,deliveryDate,historicalData):
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
    def __getattr__(self,name):
        return self.name
    def partitionOrder(self,SupplierName,repeatStatus):
        self.partitionStatus='True'
        self.givenFactory=SupplierName
        self.repeatStatus=repeatStatus
    def isRepeat(self):
        historicalIndexID=np.array([elem for elem in range(len(self.historicalData['StyleNo'])) if self.historicalData['StyleNo'][elem]==self.styleID])
        if len(historicalIndexID)>0:
            historicalIndexID=historicalIndexID[0]
            return np.array([self.historicalData.get('ExpContractNo')[historicalIndexID],self.historicalData.get('SupplierName')[historicalIndexID]])
        else:
            return 'False'
    def dateGroup(self):
        day=self.deliveryDate.day
        if day<=10:
            return 1
        elif day<=20:
            return 2
        else:
            return 3

class Supplier:
    def __init__(self,name,rank,typeCapability,startingMan):
        self.name=name
        self.rank=rank
        self.typeCapability=typeCapability
        self.startingMan=startingMan
        self.remainingMan=startingMan
        self.givenOrder=[]
        self.givenIE=[]
        self.givenDateGroup=[]
        self.givenPieces=[]
    def __getattr__(self, name):
        return self.name
    def partitionOrder(self,order):
        if order.partitionStatus=='False':
            self.remainingMan=self.remainingMan-order.manNeeded
            self.givenOrder.append(order)
            self.givenIE.append(order.IEValue)
            self.givenDateGroup.append(order.deliveryGroup)
            self.givenPieces.append(order.numPieces)
    def generateRank(self,newOrder,targetIE,paramWeight,repeatDatePenalty):
        totalGivenOrders=len(self.givenOrder)
        orderDateGroup=newOrder.deliveryGroup
        if totalGivenOrders>0:
            if orderDateGroup==1:
                numRepeatedDate=self.givenDateGroup.count(1)
            elif orderDateGroup==2:
                numRepeatedDate=self.givenDateGroup.count(2)
            else:
                numRepeatedDate=self.givenDateGroup.count(3)
            averageGivenIE=sum(self.givenIE)/float(len(self.givenIE))
            totalGivenPieces=sum(self.givenPieces)
        else:
            averageGivenIE=0
            totalGivenPieces=0
            numRepeatedDate=0
        if (targetIE - averageGivenIE) > 0:
            if newOrder.IEValue > averageGivenIE:
                IESimilarityCost = 0
            else:
                IESimilarityCost = 20
        else:
            if newOrder.IEValue > averageGivenIE:
                IESimilarityCost = 20
            else:
                IESimilarityCost = 0

        dateGroupRepeatCost=(numRepeatedDate*repeatDatePenalty)*paramWeight[0]
        IESimilarityCost=IESimilarityCost*paramWeight[1]
        totalGivenOrdersCost=totalGivenOrders*3*paramWeight[2]
        return (100-dateGroupRepeatCost-IESimilarityCost-totalGivenOrdersCost)







