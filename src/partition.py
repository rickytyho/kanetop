import data
import numpy as np
from config import InputFieldNames,Parameters

class PartitionClass:
    def __init__(self,config):
        self.orderData = config.orderData
        self.supplierData = config.supplierData
        self.historicalSheetData = config.historicalData
        self.productionDays = config.productionDuration
        self.capacityPercentage=config.capacityPercentage
        self.paramWeight=config.paramWeight
    def createPartition(self):
        orderSortIndex = np.flip(sorted(range(len(self.orderData[InputFieldNames.orderPieces])), key=lambda k: self.orderData[InputFieldNames.orderPieces][k]));
        self.orderObjects=[]
        for order in orderSortIndex:
            orderID=self.orderData[InputFieldNames.orderID][order]
            IEValue=self.orderData[InputFieldNames.IEValue][order]
            StyleID=self.orderData[InputFieldNames.styleNumber][order]
            customerName=self.orderData[InputFieldNames.customerName][order]
            numPieces=self.orderData[InputFieldNames.orderPieces][order]
            color=self.orderData[InputFieldNames.colorCN][order]
            clothingType=self.orderData[InputFieldNames.clothingType][order]
            productionDays=self.productionDays
            deliveryDate=self.orderData[InputFieldNames.deliveryDate][order]
            machineType=self.orderData[InputFieldNames.machineType][order]
            self.orderObjects.append(data.Order(orderID, IEValue, StyleID, customerName, numPieces, color, clothingType, productionDays, deliveryDate, machineType,self.historicalSheetData))
        manProd = self.supplierData[InputFieldNames.totalWorkers]
        supplierSortIndex = np.flip(sorted(range(len(manProd)), key=lambda k: manProd[k]))
        self.supplierObjects=[]
        for supplier in range(0,len(supplierSortIndex)):
            name=self.supplierData[InputFieldNames.supplierName][supplierSortIndex[supplier]]
            rank=0
            typeCapability=self.supplierData[InputFieldNames.clothingType][supplierSortIndex[supplier]]
            startingMan=self.supplierData[InputFieldNames.totalWorkers][supplierSortIndex[supplier]]
            IELevel=self.supplierData[InputFieldNames.IELevel][supplierSortIndex[supplier]]
            processType=self.supplierData[InputFieldNames.processType][supplierSortIndex[supplier]]
            machineType=self.supplierData[InputFieldNames.machineType][supplierSortIndex[supplier]]
            self.supplierObjects.append(data.Supplier(name, rank, typeCapability, startingMan,IELevel,processType,machineType))

    def partitionData(self):
        self.createPartition()
        def findsupplier(order,orderObjects,supplierObjects):
            if orderObjects[order].repeatStatus[0]!='False':
                supplierIndex=np.array([elem for elem in range(len(supplierObjects)) if (supplierObjects[elem].name==orderObjects[order].repeatStatus[1] and orderObjects[order].manNeeded<=supplierObjects[elem].remainingMan)])
                if len(supplierIndex)<1:
                    if (orderObjects[order].orderRange == Parameters.noneMachineType):
                        supplierIndex = np.array([elem for elem in range(len(supplierObjects))
                                              if
                                              (orderObjects[order].clothingType in supplierObjects[elem].typeCapability
                                               and orderObjects[order].IERange in supplierObjects[elem].IELevel
                                               and orderObjects[order].machineType in supplierObjects[elem].machineType
                                               and orderObjects[order].manNeeded <=supplierObjects[elem].remainingMan*0.01

                                               )])
                    else:
                        supplierIndex = np.array([elem for elem in range(len(supplierObjects))
                                                  if
                                                  (orderObjects[order].clothingType in supplierObjects[
                                                      elem].typeCapability
                                                   and orderObjects[order].IERange in supplierObjects[elem].IELevel
                                                   and orderObjects[order].manNeeded <= supplierObjects[
                                                       elem].remainingMan*0.01

                                                   )])
            else:
                if (orderObjects[order].orderRange == Parameters.noneMachineType):
                    supplierIndex = np.array([elem for elem in range(len(supplierObjects))
                                              if
                                              (orderObjects[order].clothingType in supplierObjects[elem].typeCapability
                                               and orderObjects[order].IERange in supplierObjects[elem].IELevel
                                               and orderObjects[order].machineType in supplierObjects[elem].machineType
                                               and orderObjects[order].manNeeded <=supplierObjects[elem].remainingMan*0.01
                                               )])
                else:
                    supplierIndex = np.array([elem for elem in range(len(supplierObjects))
                                              if
                                              (orderObjects[order].clothingType in supplierObjects[
                                                  elem].typeCapability
                                               and orderObjects[order].IERange in supplierObjects[elem].IELevel
                                               and orderObjects[order].manNeeded <= supplierObjects[elem].remainingMan*self.capacityPercentage*0.01
                                               )])
            return supplierIndex
        self.failedPartitions = []
        for order in range(0,len(self.orderObjects)):
            supplierIndex=findsupplier(order,self.orderObjects,self.supplierObjects)
            supplierRanks=[]
            if len(supplierIndex)>1:
                for supplier in supplierIndex:
                    supplierRanks.append(self.supplierObjects[supplier].generateRank(self.orderObjects[order],self.paramWeight[0][0],self.paramWeight[0][1]));
                chosenSupplier=supplierIndex[np.argmax(supplierRanks)]
                self.orderObjects[order].partitionOrder(self.supplierObjects[chosenSupplier].name)
                self.supplierObjects[chosenSupplier].partitionOrder(self.orderObjects[order])
            elif len(supplierIndex)==1:
                chosenSupplier=supplierIndex[0]
                chosenSupplierName = self.supplierObjects[chosenSupplier].name
                self.orderObjects[order].partitionOrder(chosenSupplierName)
                self.supplierObjects[chosenSupplier].partitionOrder(self.orderObjects[order])
            else:
                self.orderObjects[order].partitionFail();
                self.failedPartitions.append(self.orderObjects[order])
        self.generateResult()

    def generateResult(self):
        self.partitionResult = []
        for supplierData in self.supplierObjects:
            newSupplierPartition = data.SupplierPartition(supplierData)
            newSupplierPartition.portData()
            self.partitionResult.append(newSupplierPartition)

