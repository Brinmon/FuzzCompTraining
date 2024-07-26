import subprocess
import os

global structline
structline = 4

class CustomException(Exception):
    """自定义异常类"""
    pass

def check_projects_file_format(file_path):
    """检查projects.txt文件的格式是否正确"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 去除空行
    #lines = [line.strip() for line in lines if line.strip()]
    
    # 检查行数是否是structline的倍数
    if len(lines) % structline != 0:
        return False, "文件中的行数不是3的倍数。每个项目应包含项目名、GitHub地址和版本号。"
    
    # 检查每一行的格式
    for i in range(len(lines) // structline):
        project_name = lines[i*structline].strip()
        repo_url = lines[i*structline + 1].strip()
        version = lines[i*structline + 2].strip()
        dividingline = lines[i*structline + 3].strip()
        
        if not project_name:
            return False, f"第 {i*structline + 1} 行: 项目名为空。"
        
        if not repo_url.startswith("https://github.com/") or not repo_url.endswith(".git"):
            print(repo_url)
            return False, f"第 {i*structline + 2} 行: GitHub地址格式不正确。地址应以 'https://github.com/' 开头并以 '.git' 结尾。"
        
        if not version:
            return False, f"第 {i*structline + 3} 行: 版本号为空。"
            
        if dividingline:
            return False, f"第 {i*structline + 4} 行: 分割线不为空。"
    
    return True, "文件格式正确。"
'''
def run_command(command):
    """运行系统命令"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
'''
def run_command(command):
    """运行系统命令并实时输出"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc
def clone_repository(repo_url, repo_dir):
    """克隆GitHub仓库"""
    if os.path.exists(repo_dir):
        print(f"目录 '{repo_dir}' 已存在，跳过克隆步骤")
    else:
        run_command(f"git clone {repo_url} {repo_dir}")

def checkout_version(repo_dir, version):
    """切换到指定版本"""
    os.chdir(repo_dir)
    run_command(f"git checkout {version}")
    os.chdir('..')  # 返回上级目录

def process_projects(file_path):
    """处理项目文件"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    total_projects = len(lines) // structline
    for i in range(total_projects):
        project_name = lines[i*structline].strip()
        repo_url = lines[i*structline + 1].strip()
        version = lines[i*structline + 2].strip()
        dividingline = lines[i*structline + 3].strip()
        
        print(f"正在处理项目 {i+1}/{total_projects}: {project_name}")
        clone_repository(repo_url, project_name)
        checkout_version(project_name, version)
        print(f"项目 {project_name} 处理完成\n")

if __name__ == "__main__":
    projects_file = 'projects.txt'
    is_valid, message = check_projects_file_format(projects_file)
    if is_valid:
        print("文件格式正确,开始下载github项目!")
    else:
        print(f"文件格式错误: {message}")
        raise CustomException("格式错误!")
    process_projects(projects_file)
