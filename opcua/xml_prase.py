import xml.etree.ElementTree as ET
import csv
import sys

# 检查命令行参数数量
if len(sys.argv) < 3:
    print("Usage: python xml_parse.py <input_xml_file> <output_csv_file>")
    sys.exit(1)

# 使用命令行参数获取文件路径
xml_file_path = sys.argv[1]  # 第一个命令行参数：XML文件路径
csv_file_path = sys.argv[2]  # 第二个命令行参数：CSV文件路径

# Load and parse the XML file
tree = ET.parse(xml_file_path)  # Replace with the path to your XML file
root = tree.getroot()

# 定义命名空间字典
namespaces = {
    'ns': 'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd',  # 示例：默认命名空间
    'si': 'http://www.siemens.com/OPCUA/2017/SimaticNodeSetExtensions'  # 确保这里正确定义了si命名空间
}


# Prepare the CSV file for writing
csv_headers = ['NodeId', 'DataType', 'VariableMapping']

node_id_list = []

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)

    # Iterate through all UAVariable elements
    for uavariable in root.findall('.//ns:UAVariable', namespaces=namespaces):
        node_id = uavariable.get('NodeId')
        
        data_type = uavariable.get('DataType')

        #如果date_type不属于[INT,REAL,BOOL,UINT,DINT,UDINT,USINT]则跳过
        if data_type not in ['INT','REAL','BOOL','UINT','DINT','UDINT','USINT']:
            continue
    
        # Find the VariableMapping
        variable_mapping = None
        for extension in uavariable.findall('ns:Extensions/ns:Extension', namespaces=namespaces):
            var_map = extension.find('si:VariableMapping', namespaces=namespaces)  # Replace with actual namespace
            if var_map is not None:
                node_id_list.append(node_id)
                
                variable_mapping = var_map.text
                #去除variable_mapping中的"
                variable_mapping = variable_mapping.replace('"','')
                
                break

        # Check if all required attributes are present
        if node_id and data_type and variable_mapping:
            writer.writerow([node_id, data_type, variable_mapping])

print(f'Exported data to {csv_file_path}')
print(node_id_list)
