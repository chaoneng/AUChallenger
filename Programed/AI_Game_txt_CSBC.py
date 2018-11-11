import os
import re
import csv
import pandas as pd

def strB2Q(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += chr(inside_code)
    return rstring


def strQ2B(ustring):

    rstring = ""

    for uchar in ustring:
        inside_code = ord(uchar)

        if inside_code == 12288:
            inside_code = 32

        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248

        rstring += chr(inside_code)

    return rstring



Resident_data = open('ResidentData.csv', 'w')

csvwriter = csv.writer(Resident_data)

# 將我們要的表頭先寫出來
csvwriter.writerow(["Article_ID", "NE_Type", "Position","Length","Text","count"])

# 將所在的文件夹的txt路径設為root變數
root =('C:/Users/ASIA-I627-A/Desktop/123/demo_txt')

# 讀取文件夹下txt的文件名
file_names = os.listdir(root)


# 讀出所有txt檔並在前面加上路徑，放入list
file_ob_list = []  #放入完整的txt檔路徑
film_name_list = [] #只有txt檔的檔名

for file_name in file_names:

    # 在路徑後加上檔名
    fileob = root + '/' + file_name
    filename = re.sub('.txt', '', file_name)
    print(filename)
    #append函數是將檔名放進list的函數
    file_ob_list.append(fileob)
    film_name_list.append(filename)



#放小寫文本
character_lower_list = []
#放原文
character_list = []

# 將txt檔讀出後，分別將小寫及原文各放入list
for i in file_ob_list:
    # print(i)
    if os.path.splitext(i)[1] == ".txt":
        total = open(i).read()

        character_lower_list.append(strB2Q(str.lower(total))) # 小寫

        character_list.append(strB2Q(total)) #原文


# 用pandas將id,文本,及小寫文本轉dataframe

data_mathon = {'text_id':film_name_list,'mathon_lower':character_lower_list,'mathon':character_list}
# print(data_mathon)

txt_frame = pd.DataFrame(data_mathon)
# print(txt_frame)


# 利用pandas把資料讀進來
data_chembl = pd.read_csv('C:/Users/ASIA-I627-A/Desktop/123/demo_mapping_csv/Compound.csv')

data_diease = pd.read_csv('C:/Users/ASIA-I627-A/Desktop/123/demo_mapping_csv/diease.csv')

data_gene = pd.read_csv('C:/Users/ASIA-I627-A/Desktop/123/demo_mapping_csv/gene.csv')




# 取出txt_frame裡的id,小寫文本,文本
for x in txt_frame.values:

    # 比對化合物庫裡的NAME欄位,將dataframe裡的資料遍歷
    for o in data_chembl.values:
        # print(o[4])
#
        # 這邊使用re比對函數比對
        if re.search(r'\b' + strB2Q(str(o[4])) + r'\b', x[2]):
            n = [m.span() for m in re.finditer(r'\b' + strB2Q(str(o[4])) + r'\b', x[2])]

             # 將位置標示出來
            for length_1 in n:
                chembl_Position = length_1[0]
                chembl_Length = length_1[1] - length_1[0]

            print(x[0],'Chemical',chembl_Position,chembl_Length,o[4],len(n))

            csvwriter.writerows([[x[0],'Chemical',chembl_Position,chembl_Length,o[4],len(n)]])

    # 比對基因庫裡的symbol欄位,將dataframe裡的資料遍歷
    for z in data_gene.values:

    # 這邊使用re比對函數比對,這裡用原文比對,因縮寫皆為大寫
        if re.search(r'\b' + strB2Q(z[2]) + r'\b', x[2]):
            n = [m.span() for m in re.finditer(r'\b' + strB2Q(z[2]) + r'\b', x[2])]

        # 將位置標示出來
            for length_1 in n:
                symbol_Position = length_1[0]
                symbol_Length = length_1[1] - length_1[0]

            print(x[0], 'Gene', symbol_Position, symbol_Length, z[2],len(n))

            csvwriter.writerows([[x[0],'Gene', symbol_Position, symbol_Length, z[2],len(n)]])

    # 比對基因庫裡的name欄位,將dataframe裡的資料遍歷,這裡是使用小寫比對
    for y in data_gene.values:

    # 這邊使用re比對函數比對
        if re.search(r'\b' + strB2Q(str.lower(y[3])) + r'\b', x[1]):
            n = [m.span() for m in re.finditer(r'\b' + strB2Q(str.lower(y[3])) + r'\b', x[1])]

        # 將位置標示出來
            for length_1 in n:
                gene_Position = length_1[0]
                gene_Length = length_1[1] - length_1[0]

            print(x[0], 'Gene', gene_Position, gene_Length, y[3],len(n))

            csvwriter.writerows([[x[0], 'Gene', gene_Position, gene_Length, y[3],len(n)]])


    #比對疾病庫裡的String欄位,將dataframe裡的資料遍歷
    for h in data_diease.values:
        # print(h[2])

        # 因疾病有多種名稱,所以我們用re把名稱用逗點隔開
        for t in re.split(', ', h[2]):
            #開頭有空格的話,將空格取代
            diease_name = re.sub('^\s', '', t)

        # 這邊使用re比對函數比對
            if re.search(r'\b' + strB2Q(str.lower(diease_name)) + r'\b', x[1]):
                n = [m.span() for m in re.finditer(r'\b' + strB2Q(str.lower(diease_name)) + r'\b', x[1])]
                print(n)
            # 將位置標示出來
                for length_1 in n:
                    chembl_Position = length_1[0]
                    chembl_Length = length_1[1] - length_1[0]

                print(x[0],'Disease', chembl_Position, chembl_Length, diease_name,len(n))

                csvwriter.writerows([[x[0], 'Disease', chembl_Position, chembl_Length, diease_name,len(n)]])

# split範例
'''
a = 'aaa,bbb, ccc, dddd'

ans = a.split(',')

print(ans)
#
# for i in ans:
#
#     j = re.sub('^\s', '', i)
#
#     print(j)'''


















