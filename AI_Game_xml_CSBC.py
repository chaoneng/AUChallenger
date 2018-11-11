import xml.etree.ElementTree as ET
import csv
import pandas as pd
import numpy as np
import re

#以文件方讀取XML，解析XML
tree = ET.parse('C:/Users/ASIA-I627-A/PycharmProjects/untitled/pubmed_result_50.xml')
root = tree.getroot()
#開啟一個新檔案裝東西用
Resident_data = open('Resident_data.csv', 'w',newline='')
#設定一變數用來裝等一下要存的東西
csvwriter = csv.writer(Resident_data)
# print(csvwriter)
#將CSV標題寫入檔案
csvwriter.writerow(["PMID","Affiliation", "Year", "ArticleTitle","journal","Abstract","Country"])

# print(root.findall('PubmedArticle'))

Pmid_list = {}
#開始抓資料
for a in root.findall('PubmedArticle'):

    text_list = []

    PMID = a.find('MedlineCitation/PMID').text
    for i in a.findall('MedlineCitation/Article/Abstract/AbstractText'):
        text_list.append(i.text)
        # print(i.text)
    Pmid_list[PMID] = text_list

    # print('##################################')

# txt_frame = pd.DataFrame([data_mathon])
#print(txt_frame.PMID.values)
data_gene = pd.read_csv('C:/Users/ASIA-I627-A/PycharmProjects/untitled/gene.csv')
# print(data_gene.symbol)

# ########
for abstract in Pmid_list:
    # print(Pmid_list[abstract])
    for text in Pmid_list[abstract]:
        # print(text)
        # print('#######################')
        for gene_name in data_gene.symbol:
            # print(gene_name)
            if re.search(r'\b' +gene_name+ r'\b', text):
                # print([row for row in re.finditer(r'\b' + gene_name + r'\b', text)])
                for get_match_data in re.finditer(r'\b' + gene_name + r'\b', text):
                    print(abstract, 'Gene', get_match_data.start(), len(gene_name), gene_name)

