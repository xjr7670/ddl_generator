# -*- coding:utf-8 -*-

import os
import csv
import json
import chardet


def check_if_exists(fobj):
    '''
    检查文件或目录是否存在
    :param fobj: 文件或目录
    :return: 布尔值 True 或 False
    '''

    if os.path.exists(fobj):
        ret = True
    else:
        ret = False

    return ret

def check_folder_exists(folder_name):
    '''
    检查目录是否存在，如果不存在则创建它
    :param folder_name: 文件目录
    :return: 无返回值
    '''
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def prepare_common_data(csv_file, db_type, dt,
                        name_prefix, name_suffix, split_character):
    '''
    用于获取基础信息的函数，DDL 和 CDP 函数都能用到
    :param csv_file: 用于生成脚本的 CSV 文件
    :param db_type: 数据库类型
    :param dt: 分区字段
    :param name_prefix: 表名前缀
    :param name_suffix: 表名后缀
    :param split_character: 文件内各字段的分隔符
    :return: 由文件中的每行数据构成的列表、数据类型转换的json、分区字段名、
              委办局名称、ODPS表表名字符串模板
    '''

    # 判断是否为CSV文件类型，如果是的话，使用CSV模块读取
    # 可以避免单元格内包含换行符等特殊符号的情况

    # 先检查文件编码
    with open(csv_file, 'rb') as f:
        detect = chardet.detect(f.read())
        csv_coding = detect.get('encoding', 'utf-8')
    with open(csv_file, encoding=csv_coding) as fobj:
        reader_obj = csv.reader(fobj, delimiter=',')
        lines = [row for row in reader_obj]

    # 如果不是 .CSV 结尾的文件
    if csv_file[-4:].lower() != '.csv':
        with open(csv_file, encoding=csv_coding) as f:
            lines = f.readlines()
            lines = [[field.strip() for field in line] for line in lines]

    # 加载数据类型转换文件
    with open("./data_type_transform.json", "r", encoding="utf-8") as f:
        data_type_form = json.load(f)
        data_type_form = data_type_form[db_type]

    # 分区字段名
    if '=' in dt:
        dt_name = dt.split('=')[0]
    else:
        dt_name = dt

    # 委办局缩写
    # 只有表名是用的缩写
    # 文件夹名、CDP 的源名字，都用ODPS源的名字，也就是文件名
    odps_source_name = os.path.split(csv_file)[-1].split(".")[0]
    # 委办局有多个库时，数据源名字中会有下划线，此时文件名也会有下划线
    # 在生成 CDP 的时候，这个名字需要保留
    unit_abbr = odps_source_name.split('_')[0]

    full_tb_name_str = '_'.join([name_prefix, unit_abbr, "{}", name_suffix])

    return lines, data_type_form, dt_name, odps_source_name, full_tb_name_str


def generate_ddl(csv_file, db_type, dt, name_prefix,
                 name_suffix, output_folder, lifecycle, split_character):
    '''
    真正生成 DDL 的函数，每次调用处理一个输入文件
    :param csv_file: 处理后的元数据文件
    :param db_type: 数据库类型
    :param dt: 分区字段
    :param name_prefix: 要生成的表的表名前缀
    :param name_suffix: 要生成的表的表名后缀
    :param output_folder: 输出目录
    :param lifecycle: 表生命周期
    :param split_character: 文件内各字段的分隔符
    :return: 生成的 DDL 脚本个数
    '''

    ddl_count = 0

    lines, data_type_form, dt_name, odps_source_name, full_tb_name_str = \
        prepare_common_data(csv_file, db_type, dt,
                            name_prefix, name_suffix, split_character)

    tmp_name = sql = ''
    dt_tmp = "\nPARTITIONED BY (\n\t{} STRING COMMENT 'YYYYMMDD'\n)"\
        .format(dt_name)

    for idx, line in enumerate(lines[1:], start=2):
        try:
            schema, tb_name, _, tb_cmt, column, col_cmt, data_type = line
            tb_cmt, col_cmt = tb_cmt.replace('\n', ''), col_cmt.replace('\n', '')
        except ValueError as e:
            error_msg = ("\n当前行数：" + str(idx) + "\n\n"
                         "由指定分隔符分割后得到的字段数量不等于7！\n"
                         "请检查表或字段注释中是否包含分隔符或换行符")
            raise ValueError(str(e) + error_msg)
        data_type = data_type.lower()
        if data_type in data_type_form:
            odps_data_type = data_type_form[data_type]
        else:
            odps_data_type = "STRING"
        if tmp_name != tb_name or line == lines[-1]:
            if sql != '':
                # 最后一行，要先添加进来
                if line == lines[-1]:
                    sql += "\n\t{} {} COMMENT '{}',".format(column.lower(),
                                                            odps_data_type.upper(),
                                                            col_cmt)
                sql = sql[:-1]
                sql += "\n) COMMENT '{}';".format(tmp_tb_cmt)
                # sql += dt_tmp
                # sql += "\nLIFECYCLE {};".format(lifecycle)
                result_path = os.path.join(output_folder, 'ddl', odps_source_name)
                check_folder_exists(result_path)
                print(full_tb_name)
                result_name = os.path.join(result_path, full_tb_name + '.sql')
                with open(result_name.lower(), 'w', encoding='utf-8') as f:
                    f.write(sql)
                    ddl_count += 1
                # 如果当前已经是最后一行了，则退出函数
                if line == lines[-1]:
                    return ddl_count
                sql = ''
            if sql == '':
                tmp_name = tb_name
                tmp_tb_cmt = tb_cmt
                # 20191114，鹏飞意思，把 write 的 table 通过截取源表名的后面部分拼接而成
                new_tb_name = '_'.join(tb_name.split('_')[4:]).lower()
                full_tb_name = full_tb_name_str.format(new_tb_name)
                sql = "-- 文件名称： ddl_{}\n\n".format(full_tb_name)
                sql += "DROP TABLE IF EXISTS {};\n".format(full_tb_name)
                sql += "CREATE TABLE IF NOT EXISTS {} (".format(full_tb_name)

        sql += "\n\t{} {} COMMENT '{}',".format(column.lower(),
                                                odps_data_type.upper(),
                                                col_cmt)
    return ddl_count


def generate_cdp(csv_file, db_type, dt, name_prefix,
                 name_suffix, output_folder, split_character):
    '''
    真正用于生成 CDP 的函数，每次调用处理一个输入文件
    :param csv_file: 处理后的元数据文件
    :param db_type: 数据库类型
    :param dt: 分区字段
    :param name_prefix: 要生成的表的表名前缀
    :param name_suffix: 要生成的表的表名后缀
    :param output_folder: 输出目录
    :param split_character: 文件中各个字段的分隔符
    :return: 生成的 CDP 脚本个数
    '''

    cdp_count = 0
    lines, data_type_form, dt_name, cdp_source_name, full_tb_name_str = \
        prepare_common_data(csv_file, db_type, dt,
                            name_prefix, name_suffix, split_character)

    tmp_name = ''
    reader_column = []
    writer_column = []

    for idx, line in enumerate(lines[1:], start=2):
        try:
            schema, tb_name, _, _, column, _, _ = line
        except ValueError as e:
            error_msg = ("\n当前行数：" + str(idx) + "\n\n"
                         "由指定分隔符分割后得到的字段数量不等于7！\n"
                         "请检查表或字段注释中是否包含分隔符或换行符")
            raise ValueError(str(e) + error_msg)
        if tmp_name != tb_name or line == lines[-1]:
            if writer_column:
                # 最后一行，要先添加进来
                if line == lines[-1]:
                    reader_column.append(column)
                    writer_column.append(column.lower())
                # 不等于空的时候保存文件
                cdp_tpl['steps'][0]['parameter']['column'] = reader_column
                cdp_tpl['steps'][0]['stepType'] = db_type
                cdp_tpl['steps'][1]['parameter']['column'] = writer_column
                cdp_tpl['steps'][1]['parameter']['partition'] = dt
                result_path = os.path.join(output_folder, 'cdp', cdp_source_name)
                check_folder_exists(result_path)
                print(full_tb_name)
                result_name = os.path.join(result_path, full_tb_name + '.json')
                with open(result_name.lower(), 'w', encoding='utf-8') as f:
                    f.write(json.dumps(cdp_tpl, ensure_ascii=False, indent=4))
                    cdp_count += 1
                # 如果当前已经是最后一行了，则退出函数
                if line == lines[-1]:
                    return cdp_count
                reader_column = []
                writer_column = []

            if not writer_column:
                # 等于空的新文件开始

                # 读入模板
                with open('./cdp_template.json') as f:
                    cdp_tpl = json.load(f)

                tmp_name = tb_name
                # 20191114，鹏飞意思，把 write 的 table 通过截取源表名的后面部分拼接而成
                new_tb_name = '_'.join(tb_name.split('_')[4:]).lower()
                full_tb_name = full_tb_name_str.format(new_tb_name)
                # 20191114，鹏飞意思，把 reader 的 datasource 写死为 sjz_tyzhengshi
                # cdp_tpl['steps'][0]['parameter']['datasource'] = cdp_source_name
                cdp_tpl['steps'][0]['parameter']['datasource'] = 'sjz_tyzhengshi'
                cdp_tpl['steps'][0]['parameter']['table'] = tb_name
                cdp_tpl['steps'][1]['parameter']['table'] = full_tb_name

        reader_column.append(column)
        writer_column.append(column.lower())

    return cdp_count


def check_pure_dir(directory, end_str):
    '''
    检查输入的 directory 中的文件名是否都以 end_str 结尾
    :param directory: 目录路径
    :param end_str: 结尾字符串
    :return: 布尔值 True 或 False
    '''

    file_lists = os.listdir(directory)
    if not all([f.endswith(end_str) for f in file_lists]):
        return False
    else:
        return True


def addDt(dt, input_folder, output_folder):
    '''
    添加分区。此时的输入只能是文件夹
    :param dt: 分区表达式
    :param input_folder: 需要添加分区的文件所在的文件夹
    :param output_folder: 添加分区后的文件保存的位置
    :return: 返回添加了分区后的文件个数或警告文本
    '''

    # 先检测输入输出的值是否都是文件夹
    if not (os.path.isdir(input_folder) and os.path.isdir(output_folder)):
        return "输入输出位置都应该是文件夹"

    # 再检查输入的目录里面是否包含有非 cdp 文件
    cdp_files = os.listdir(input_folder)
    if not all([f.endswith('.cdp') for f in cdp_files]):
        return "输入位置里面包含有非 cdp 文件，请先移除！"

    check_if_exists(output_folder)
    add_dt_count = 0
    # 在目标目录内先创建 add_dt 文件夹
    add_dt_dir = os.path.join(output_folder, 'add_dt')
    check_folder_exists(add_dt_dir)

    for cdp_file in cdp_files:

        # 先移除不必要的字段
        cdp_full_path = os.path.join(input_folder, cdp_file)
        with open(cdp_full_path, encoding='utf-8') as f:
            raw_json = json.load(f)
        if "baseId" in raw_json:
            raw_json.pop("baseId")
        if "projectId" in raw_json:
            raw_json.pop("projectId")
        if "traceId" in raw_json:
            raw_json.pop("tenantId")
        if "traceId" in raw_json:
            raw_json.pop("traceId")
        if "instanceId" in raw_json['configuration']['reader']['parameter']:
            raw_json['configuration']['reader']['parameter'].pop("instanceId")
        if "instanceId" in raw_json['configuration']['writer']['parameter']:
            raw_json['configuration']['writer']['parameter'].pop("instanceId")

        # 再添加 dt 字段
        raw_json['configuration']['writer']['parameter']['partition'] = dt
        tgt_name = cdp_file.split('.')[0]
        tgt_name = tgt_name + '.json'

        # 获取委办局缩写
        department_name = cdp_file.split('_')[1]
        result_dir = os.path.join(add_dt_dir, department_name)
        check_folder_exists(result_dir)
        result_json_path = os.path.join(result_dir, tgt_name)
        with open(result_json_path, 'w') as f:
            f.write(json.dumps(raw_json, ensure_ascii=False, indent=4))
            add_dt_count += 1
    else:
        return "完成 cdp 文件处理个数： {}".format(add_dt_count)


def makeDDL(db_type, dt, name_prefix, name_suffix, input_value,
            output_folder, lifecycle, split_character):
    '''
    生成 DDL 的主函数
    :param db_type: 数据库类型
    :param dt: 分区表达式
    :param name_prefix: 要生成的 DDL 的表名前缀
    :param name_suffix: 要生成的 DDL 的表名后缀
    :param input_value: 用于生成 DDL 脚本的文件或目录
    :param output_folder: DDL 生成后保存的位置
    :param lifecycle: 表生命周期
    :param split_character: 文件内各字段的分隔符
    :return: 返回生成的 DDL 脚本个数或警告文本
    '''

    if os.path.isdir(input_value):
        # 输入的是目录
        csv_files = os.listdir(input_value)
        if not all([f.endswith('.csv') for f in csv_files]):
            return "输入目录中包含有非 csv 文件，请移除"

        ddl_count = 0
        for csv_file in csv_files:
            csv_file = os.path.join(input_value, csv_file)
            count = generate_ddl(csv_file,
                                 db_type,
                                 dt,
                                 name_prefix,
                                 name_suffix,
                                 output_folder,
                                 lifecycle,
                                 split_character)
            ddl_count += count
    else:
        # 输入的是文件
        ddl_count = generate_ddl(input_value,
                                 db_type,
                                 dt,
                                 name_prefix,
                                 name_suffix,
                                 output_folder,
                                 lifecycle,
                                 split_character)

    return "完成处理表个数： {}".format(ddl_count)


def makeCDP(db_type, dt, name_prefix, name_suffix,
            input_value, output_folder, split_character):
    '''
    生成 CDP 的主函数
    :param db_type: 数据库类型
    :param dt: 分区表达式
    :param name_prefix: 要生成的 CDP 的目标表表名前缀
    :param name_suffix: 要生成的 CDP 的目标表表名后缀
    :param input_value: 用于生成 CDP 脚本的文件或目录
    :param output_folder: CDP 生成后保存的位置
    :param split_character: 文件内各字段的分隔符
    :return: 返回生成的 CDP 脚本个数或警告文本
    '''

    if os.path.isdir(input_value):
        # 输入的是目录
        csv_files = os.listdir(input_value)
        if not all([f.endswith('.csv') for f in csv_files]):
            return "输入目录中包含有非 csv 文件，请移除"

        cdp_count = 0
        for csv_file in csv_files:
            csv_file = os.path.join(input_value, csv_file)
            count = generate_cdp(csv_file,
                                 db_type,
                                 dt,
                                 name_prefix,
                                 name_suffix,
                                 output_folder,
                                 split_character)
            cdp_count += count
    else:
        # 输入的是文件
        cdp_count = generate_cdp(input_value,
                                 db_type,
                                 dt,
                                 name_prefix,
                                 name_suffix,
                                 output_folder,
                                 split_character)

    return "完成处理表个数： {}".format(cdp_count)
