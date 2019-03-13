from easygui import multenterbox,choicebox
from config import UserInput,Filenames
import os
import partition
import data
import xlsxwriter
import shutil
import pdb;

pdb.set_trace()

def writeExcel(partitionResult,failedPartitions,partitionFileOutput,ordersFileOutput):
        partitionWorkbook = xlsxwriter.Workbook(partitionFileOutput,{'nan_inf_to_errors': True})
        partitionWorksheet = partitionWorkbook.add_worksheet(Filenames.partition_worksheet)
        partitionFailedSheet=partitionWorkbook.add_worksheet(Filenames.failed_worksheet)
        ordersWorkbook = xlsxwriter.Workbook(ordersFileOutput,{'nan_inf_to_errors': True})
        ordersWorksheet=ordersWorkbook.add_worksheet(Filenames.partition_worksheet)
        ordersFailedSheet=ordersWorkbook.add_worksheet(Filenames.failed_worksheet)
        partition_row_index = 1
        partition_column_index = 1
        orders_row_index=0
        orders_column_index=0
        ordersWorksheet.write(orders_row_index,orders_column_index,'供应商');
        ordersWorksheet.write(orders_row_index,orders_column_index+1,'平均订单IE值');
        ordersWorksheet.write(orders_row_index,orders_column_index+2, 'ET-序号');
        ordersWorksheet.write(orders_row_index,orders_column_index+3, 'IE值');
        ordersWorksheet.write(orders_row_index,orders_column_index+4, '订单件数');
        ordersWorksheet.write(orders_row_index,orders_column_index+5, '款式颜色');
        ordersWorksheet.write(orders_row_index,orders_column_index+6, '款号');
        ordersWorksheet.write(orders_row_index,orders_column_index+7, '订单交期日');
        ordersWorksheet.write(orders_row_index,orders_column_index+8, '品牌');
        ordersWorksheet.write(orders_row_index,orders_column_index+9, '返单');
        for partitionSupplier in partitionResult:
            partitionWorksheet.write(partition_row_index - 1, partition_column_index + 1, '工厂月人数')
            partitionWorksheet.write(partition_row_index - 1, partition_column_index + 2, '工厂甚于月人数')
            partitionWorksheet.write(partition_row_index - 1, partition_column_index + 3, '总排单订单件数')
            partitionWorksheet.write(partition_row_index - 1, partition_column_index + 4, '平均订单IE值')
            partitionWorksheet.write(partition_row_index, partition_column_index, partitionSupplier.supplierName)
            partitionWorksheet.write(partition_row_index, partition_column_index + 1, partitionSupplier.startingMan)
            partitionWorksheet.write(partition_row_index, partition_column_index + 2, partitionSupplier.remainingMan)
            partitionWorksheet.write(partition_row_index, partition_column_index + 3, partitionSupplier.orderPiecesTotal)
            partitionWorksheet.write(partition_row_index, partition_column_index + 4, partitionSupplier.IEAverage)
            if len(partitionSupplier.orderID) > 0:
                partitionWorksheet.write(partition_row_index + 2, partition_column_index, 'ET-序号')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 1, 'IE值')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 2, '订单件数')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 3, '款式颜色')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 4, '款号')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 5, '订单交期日')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 6, '品牌')
                partitionWorksheet.write(partition_row_index + 2, partition_column_index + 7, '返单')
                for orderIndex in range(0, len(partitionSupplier.orderID)):
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index,partitionSupplier.supplierName);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+1, partitionSupplier.IEAverage);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+2, partitionSupplier.orderID[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+3, partitionSupplier.orderIE[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+4, partitionSupplier.orderPieces[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+5, partitionSupplier.orderColor[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+6, partitionSupplier.orderStyle[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+7, partitionSupplier.orderDeliveryDate[orderIndex].strftime('%m/%d/%Y'));
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+8, partitionSupplier.orderCustomer[orderIndex]);
                    ordersWorksheet.write(orders_row_index+orderIndex+1, orders_column_index+9, partitionSupplier.orderRepeatStatus[orderIndex]);
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index, partitionSupplier.orderID[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 1, partitionSupplier.orderIE[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 2, partitionSupplier.orderPieces[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 3, partitionSupplier.orderColor[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 4, partitionSupplier.orderStyle[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 5, partitionSupplier.orderDeliveryDate[orderIndex].strftime('%m/%d/%Y'))
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 6, partitionSupplier.orderCustomer[orderIndex])
                    partitionWorksheet.write(partition_row_index + orderIndex + 3, partition_column_index + 7, partitionSupplier.orderRepeatStatus[orderIndex])
                partition_row_index += len(partitionSupplier.orderID) + 5
                orders_row_index+=len(partitionSupplier.orderID)
            else:
                partition_row_index += 3
        partition_row_index = 1
        partition_column_index = 1
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index, 'ET-序号')
        partitionFailedSheet.write(partition_row_index -1, partition_column_index+1, 'IE值')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+2, '订单件数')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+3, '款式颜色')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+4, '款号')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+5, '订单交期日')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+6, '品牌')
        partitionFailedSheet.write(partition_row_index - 1, partition_column_index+7, '返单')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index, 'ET-序号')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 1, 'IE值')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 2, '订单件数')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 3, '款式颜色')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 4, '款号')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 5, '订单交期日')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 6, '品牌')
        ordersFailedSheet.write(partition_row_index - 1, partition_column_index + 7, '返单')
        for failedOrder in range(0,len(failedPartitions)):
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index, failedPartitions[failedOrder].orderID)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 1, failedPartitions[failedOrder].IEValue)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 2, failedPartitions[failedOrder].numPieces)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 3, failedPartitions[failedOrder].color)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 4, failedPartitions[failedOrder].styleID)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 5, failedPartitions[failedOrder].deliveryDate.strftime('%m/%d/%Y'))
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 6, failedPartitions[failedOrder].customerName)
            ordersFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 7, failedPartitions[failedOrder].repeatStatus[0])
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index, failedPartitions[failedOrder].orderID)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 1, failedPartitions[failedOrder].IEValue)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 2, failedPartitions[failedOrder].numPieces)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 3, failedPartitions[failedOrder].color)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 4, failedPartitions[failedOrder].styleID)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 5, failedPartitions[failedOrder].deliveryDate.strftime('%m/%d/%Y'))
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 6, failedPartitions[failedOrder].customerName)
            partitionFailedSheet.write(partition_row_index + failedOrder, partition_column_index + 7, failedPartitions[failedOrder].repeatStatus[0])
        partitionWorkbook.close()
        ordersWorkbook.close()


# Gets the input file directory and presents it to the user.

currentDirectory=os.getcwd()
InputFileDirectory=''.join([currentDirectory,'/Data'])
OutputFileDirectory=''.join([currentDirectory,'/Result'])

## Generate folder for input
if not os.path.exists(InputFileDirectory):
    os.makedirs(InputFileDirectory)
if not os.path.exists(OutputFileDirectory):
    os.makedirs(OutputFileDirectory)

fileDirs=[]
for root, dirs, files in os.walk(InputFileDirectory):
    for file in files:
        if not file.startswith('.'):
            fileDirs.append(os.path.join(root,file))

msg ="请选择数据文件?"
title = UserInput.paramterTitle
choices = fileDirs
inputFilePath = choicebox(msg, title, choices)
fileNamePath=os.path.basename(inputFilePath)
fileName=os.path.splitext(fileNamePath)[0]

# Load input data into config.
# fileName='AdjustedMay'
# choice='/Users/Ricky/PycharmProjects/SCP-Optimization/Data/Source/AdjustedMay.xlsx'

configuration = data.Configuration(fileName,inputFilePath,OutputFileDirectory)

#Asks users for paremters
newmsg = UserInput.paramterMessage
newtitle = UserInput.paramterTitle
fieldNames=[UserInput.deliveryDate,UserInput.capacityPercentage,UserInput.deliveryDateWeight,UserInput.processWeight]
fieldValues = []  # we start with blanks for the values
fieldValues = multenterbox(newmsg,newtitle, fieldNames)

# make sure that none of the fields was left blank
while 1:
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
      if fieldValues[i].strip() == "":
        errmsg = errmsg + ('"%s" 是必填的.\n\n' % fieldNames[i])
    if errmsg == "": break # no problems found
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

intValues=[int(i) for i in fieldValues]

##Load parameters into config.
# intValues=[60,100,20,100]
configuration.readData(intValues)

## Partition data based on config.
result=partition.PartitionClass(configuration)
result.partitionData()
successfulPartitions=result.partitionResult
failedPartitions=result.failedPartitions

## Creates directory and writes the partition result and the orders result into the directory.
os.mkdir(configuration.outputDirectory)
writeExcel(successfulPartitions, failedPartitions, configuration.partitionFilePath,configuration.ordersFilePath )

# This zips the archive folder and deletes the folder after the zip has been moved to the correct directory. The zip should include both the partition file and the orders file.
shutil.make_archive(''.join([fileName,Filenames.result_name]), 'zip', configuration.outputDirectory)
shutil.move(''.join([os.getcwd(),'/',fileName,Filenames.result_name,'.zip']),''.join([configuration.outputDirectory,Filenames.result_name,'.zip']))
shutil.rmtree(configuration.outputDirectory)

















