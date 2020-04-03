

import os
import sys
pyinstaller='pyinstaller.exe'
import shutil


if __name__=='__main__':
    # 参数说明：
    #  -n  生成exe名字
    #  -w  不显示后台控制窗口
    # --distpath    保存路径
    cmd = pyinstaller + ' -n prePrePrinter_v2.0.1.2 --distpath ./Bin/ products_sn_printer.py'
    print(cmd)
    os.system(cmd)

    cmd = pyinstaller + ' -F --icon=orbbecUI products_sn_printer.py'
    print(cmd)
    os.system(cmd)
    # # 拷贝文件
    while not os.path.exists('./Bin/prePrePrinter_v2.0.1.2'):
        print('wait')

    src_path = 'Bin/prePrePrinter_v2.0.1.2/'
    shutil.copytree('Config', src_path + 'Config')
    shutil.copytree('Code', src_path + 'Code')
    shutil.copytree('font', src_path + 'font')

