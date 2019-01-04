import dataStruct
import numpy as np

class PartitionClass:
    def __init__(self,orderData,supplierData,historicalData,productionDays,targetIE,paramWeight,repeatDatePenalty):
        self.orderData = orderData
        self.supplierData = supplierData
        self.historicalSheetData = historicalData
        self.productionDays = productionDays
        self.targetIE = targetIE
        self.paramWeight=paramWeight
        self.repeatDatePenalty=repeatDatePenalty
    def __getattr_(self,name):
        return self.name
    def createPartition(self):
        def createOrderClass():
            def setPriority():
                orderPieces = self.orderData['SizeNum']
                sortIndex = np.flip(sorted(range(len(orderPieces)), key=orderPieces.__getitem__))
                return sortIndex
            sortIndex=setPriority()
            orderObjects=[]
            for order in sortIndex:
                orderID=self.orderData['BillNo'][order]
                IEValue=self.orderData['IEValue'][order]
                StyleID=self.orderData['GoodsNo'][order]
                customerName=self.orderData['CustomerShortName'][order]
                numPieces=self.orderData['SizeNum'][order]
                color=self.orderData['CnColor'][order]
                clothingType=self.orderData['ClothingType'][order]
                productionDays=self.productionDays
                deliveryDate=self.orderData['DeliveryDate'][order]
                newClass=dataStruct.Order(orderID,IEValue,StyleID,customerName,numPieces,color,clothingType,productionDays,deliveryDate,self.historicalSheetData)
                orderObjects.append(newClass)
            return orderObjects
        def createSupplierClass():
            def setPriority():
                manProd = self.supplierData['Man']
                sortIndex = np.flip(sorted(range(len(manProd)), key=manProd.__getitem__))
                return sortIndex
            sortIndex=setPriority()
            supplierObjects=[]
            for supplier in range(0,len(sortIndex)):
                name=self.supplierData['SupplierName'][sortIndex[supplier]]
                rank=0
                typeCapability=self.supplierData['ClothingType'][sortIndex[supplier]]
                startingMan=self.supplierData['Man'][sortIndex[supplier]]
                supplierObject=dataStruct.Supplier(name,rank,typeCapability,startingMan)
                supplierObjects.append(supplierObject)
            return supplierObjects
        return np.array([createOrderClass(),createSupplierClass()])
    def partitionData(self):
        PartitionData=self.createPartition()
        orderObjects=PartitionData[0]
        supplierObjects=PartitionData[1]
        numOrders=len(orderObjects)
        def findsupplier(orderObjects,order,supplierObjects):
            if orderObjects[order].repeatStatus[0]!='False':
                supplierIndex=np.array([elem for elem in range(len(supplierObjects)) if supplierObjects[elem].name==orderObjects[order].repeatStatus[1]])
                repeatStatus='True'
            else:
                supplierIndex=np.array([elem for elem in range(len(supplierObjects)) if orderObjects[order].clothingType in supplierObjects[elem].typeCapability
                        and orderObjects[order].manNeeded<=supplierObjects[elem].remainingMan])
                repeatStatus='False'
            return np.array([supplierIndex,repeatStatus])
        for order in range(0,numOrders):
            supplierIndex=findsupplier(orderObjects,order,supplierObjects)[0]
            orderRepeatStatus=findsupplier(orderObjects,order,supplierObjects)[1]
            supplierRanks=[]
            if len(supplierIndex)>0:
                for supplier in supplierIndex:
                    supplierRanks.append(supplierObjects[supplier].generateRank(orderObjects[order],self.targetIE,self.paramWeight,self.repeatDatePenalty))
                SortIndex=np.flip([i[0] for i in sorted(enumerate(supplierRanks), key=lambda x:x[1])])
                chosenSupplier=supplierIndex[SortIndex[0]]
                supplierObjects[chosenSupplier].partitionOrder(orderObjects[order])
                chosenSupplierName=supplierObjects[chosenSupplier].name
                orderObjects[order].partitionOrder(chosenSupplierName, orderRepeatStatus)
        return np.array([orderObjects,supplierObjects])

