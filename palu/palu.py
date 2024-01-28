import subprocess

# 定义可执行文件的完整路径
executable_path = r'R:\SteamLibrary\steamapps\common\PalServer\Pal\Binaries\Win64\PalServer-Win64-Test-Cmd.exe'

# 启动进程


# 如果需要同步执行并等待程序结束，可以使用 run 方法
# subprocess.run([executable_path], check=True)  # 添加check=True来检查程序是否正常退出

# 若要传递参数给可执行文件，可以这样做：
# subprocess.Popen([executable_path, 'arg1', 'arg2'])

def creatpalu(content):
    subprocess.Popen([executable_path])


# if __name__ == '__main__':
