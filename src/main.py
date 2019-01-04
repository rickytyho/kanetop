import os, sys
import pandas as pd
import partition

fn="/Users/Ricky/PycharmProjects/Partition/Data/"+sys.argv[1]
filePath=os.path.abspath(fn)

producionDays=30
targetIE=40
repeatDatePenalty=15
IESimilarityImportance=60
DateSimilarityImportance=80
paramWeight=[1.5,0.5,0.2]

orderData=pd.read_excel(filePath,sheet_name=0).to_dict()
supplierData=pd.read_excel(filePath,sheet_name=1).to_dict()
historicalData=pd.read_excel(filePath,sheet_name=2).to_dict()

newPartitionClass=partition.PartitionClass(orderData,supplierData,historicalData,producionDays,targetIE,paramWeight,repeatDatePenalty)
PartitionResult=newPartitionClass.partitionData()

OrderPartitionResult=PartitionResult[0]
SupplierPartitionResult=PartitionResult[1]






