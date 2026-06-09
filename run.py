import os
import shutil
import time
import allure
import pytest
# import subprocess
# from config import Config
#

import pytest
import subprocess
import shutil
import time
from pathlib import Path

RESULT_DIR = "./allure-results"   # 确保与 pytest --alluredir 一致
REPORT_DIR = "./allure-report"
LOG_FILE = "logs/frame.log"

def run_pytest():
    print("正在执行测试用例...")
    Path(RESULT_DIR).mkdir(exist_ok=True)
    exit_code = pytest.main(['-vs', f'--alluredir={RESULT_DIR}'])
    print("pytest 执行成功" if exit_code == 0 else f"pytest 执行结束，退出码: {exit_code}")

def generate_allure_report():
    print("正在生成 Allure 报告...")
    # 关键：添加 shell=True 以便 Windows 识别 allure.bat
    result = subprocess.run(
        f"allure generate {RESULT_DIR} -o {REPORT_DIR} --clean",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"报告生成失败：\n{result.stderr}")
        raise RuntimeError("Allure generate 失败")
    print("报告生成成功")

def open_allure_report():
    print("正在打开 Allure 报告...")
    subprocess.run(f"allure open {REPORT_DIR}", shell=True, check=True)

def backup_log():
    log_path = Path(LOG_FILE)
    if log_path.exists():
        timestamp = int(time.time())
        backup_path = Path("logs") / f"frame_{timestamp}.log"
        shutil.move(str(log_path), str(backup_path))
        print(f"日志已备份至 {backup_path}")

def main():
    try:
        run_pytest()
        generate_allure_report()
        open_allure_report()
        print("测试报告已生成并打开，请查看浏览器")
    except Exception as e:
        print(f"执行过程中出现异常：{e}")
        raise
    finally:
        backup_log()

if __name__ == "__main__":
    main()
# if __name__ == "__main__":
#     pytest.main(['-vs'])
#     time.sleep(3)
#     os.system("allure generate ./temps -o ./reports --clean")
#     os.system("allure open ./reports")
#     # os.system('allure generate allure-results -o allure-report --clean')
#     # # 手动打开报告
#     os.system('allure open allure-report')
#     # 自动打开报告
#     os.system('allure open reports')
#     print(f'测试报告已生成，请查看')
#     #复制日志
#     shutil.move("logs/frame.log","logs/frame_"+str(int(time.time()))+".log")
#





#
# def run_tests():
#     # 创建必要目录
#     os.makedirs(Config.LOG_DIR, exist_ok=True)
#     os.makedirs("./reports/allure-results", exist_ok=True)
#
#     # 执行pytest测试
#     pytest_args = [
#         "-v",
#         "-s",
#         "--alluredir=./reports/allure-results",
#         "--clean-alluredir"
#     ]
#     exit_code = pytest.main(pytest_args)
#
#     # 生成Allure报告
#     # if exit_code == 0:
#     #     subprocess.run("allure generate ./reports/allure-results -o ./reports/allure-report --clean", shell=True)
#     #     print("\n测试报告已生成，使用以下命令查看：")
#     #     print("allure open ./reports/allure-report")
#     # else:
#     #     print("\n测试执行失败，请检查日志")
#
#
# if __name__ == "__main__":
#     run_tests()
