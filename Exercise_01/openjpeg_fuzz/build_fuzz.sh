#!/bin/bash
#这个是对程序进行源码插桩编译
tar -xvf openjpeg.tar.gz
cd openjpeg
#创建一个目录用来指定，程序的安装位置
mkdir build
cd build 

# 设置编译器
export CC=afl-clang-lto
export CXX=afl-clang-lto++

# 设置编译标志
export CFLAGS="-O0 -g -fsanitize=address,leak,undefined"
export CXXFLAGS="-O0 -g -fsanitize=address,leak,undefined"
#运行cmake生成Makefile文件用来供make使用
cmake ..
# 设置ASan
#方法一：export AFL_USE_ASAN=1
#方法二：添加编译选项： -fsanitize=address
#export LD_LIBRARY_PATH=/root/work/openjpeg/build/bin:$LD_LIBRARY_PATH

# 编译和安装
make
make install

