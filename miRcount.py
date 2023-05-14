from sys import argv
import os
import pandas as pd


# 获取文件
def list_sam_file(sam_format):
    print(os.getcwd())
    sam_files_path = os.getcwd()
    for sam_file in os.listdir(sam_files_path):
        if os.path.splitext(sam_file)[1] in sam_format:
            sam_file_list.append(os.path.splitext(sam_file)[0])
        else:
            continue


# 读取文件
def send_line(path):
    with open(path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            else:
                if '@' not in line:
                    count_num(line)


# 计数，并返回结果
def count_num(line):
    line = line.split('\t')
    ref_id, seq_seq = line[2], line[9]
    cur_key = ref_id + '@' + seq_seq
    if ref_id == '*':
        # 判断sam文件中是否包含有未比对的序列
        print('this seq did not map to any ref :' + seq_seq)
    else:
        if line[1] == '0':  # 第二列为0表示为比对成功，为16时为反向比对成功。
            if cur_key in result_dict.keys():
                result_dict[cur_key] += 1
            else:
                result_dict[cur_key] = 1


# 输出分类结果CSV
def result_output(result, file_name):
    try:
        os.mkdir(os.getcwd() + r'/result/')
    except:
        pass
    result_file_path = os.getcwd() + '\\result\\' + file_name + '.csv'
    isomir_count_filepath.append(result_file_path)
    with open(result_file_path, 'a') as result_file:
        result_file.write('miRNA@isomirSEQ,'+ file_name + '\n')
        for i in result:
            title = str(i).split('@')
            ref, iso = title[0], title[1]
            result_file.write(f'{ref}@{iso},{result_dict[i]}\n')
    print('数据保存至' + result_file_path)


# 将所有结果merge到一个csv中
def merge_table(csv_file_list):
    n = 1
    for file in csv_file_list:
        print('合并文件'+file)
        if n == 1:
            df = pd.read_csv(file, index_col=0)
        else:
            df = pd.concat([df, pd.read_csv(file, index_col=0)], axis=1, join="outer")
        n += 1
    df.to_csv(os.getcwd()+'//result//merge.csv')


if __name__ == '__main__':
    sam_file_list = []  # 搜索到目录下sam文件的数量
    isomir_count_filepath = []  # 统计结果文件存放目录
    Const_Image_Format = ['.sam', '.SAM']  # 要搜索目录下的文件后缀名

    list_sam_file(Const_Image_Format)  # 搜索文件，并加入列表

    print('已找到' + str(len(sam_file_list)) + '个sam文件')
    # for sam_file in sam_file_list:  # 对每一个sam文件进行isomir的计数
    #     result_dict = {}  # 计数结果的保存字典
    #     print('正在处理' + sam_file + '.sam')
    #     send_line(os.getcwd() + '\\' + sam_file + '.sam')  # 分析计数
    #     result_output(result_dict, sam_file)  # 计数结果写入文件
    #
    # merge_table(isomir_count_filepath)  # 将所有结果merge到一起

    print('DONE!')
