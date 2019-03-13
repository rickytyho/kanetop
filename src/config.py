
class Filenames:
    userInputQuestion='请输入文件名'
    partition_output_file_name='排单总结.xlsx'
    orders_output_file_name='订单总结.xlsx'
    result_name=' 排单结果'
    partition_worksheet='订单排单结果'
    failed_worksheet='未排出订单'

class Settings:
    productionDuration='生产周期'
    DeliveryDateWeight='交货期比重'
    processWeight='生产流程比重'

class InputFieldNames:
    orderPieces='SizeNum'
    IEValue='IEValue'
    IELevel='IELevel'
    orderID='BillNo'
    styleNumber='GoodsNo'
    customerName='CustomerShortName'
    pieces='SizeNum'
    colorCN='CnColor'
    machineType='VehicleTypeName'
    processType='ProProcess'
    clothingType='ClothingType'
    deliveryDate='DeliveryDate'
    totalWorkers='Man'
    supplierName='SupplierName'
    historicalStyleNumber='StyleNo'
    historicalOrdersNumber='ExpContractNo'
    historicalSupplierName='SupplierName'

class UserInput:
    paramterMessage='请输入排单参数'
    paramterTitle='Kanetop智能排单'
    deliveryDate='生产周期'
    capacityPercentage='产能百分比'
    deliveryDateWeight='交期冲突比重'
    processWeight='生产流程比重'

class Parameters:
    noneMachineType='无'
    lowRange='低'
    midRange='中'
    highRange='高'

    lowIERange=[1,16]
    middleIERange=[16,35]
    highIERange=[36,100]



