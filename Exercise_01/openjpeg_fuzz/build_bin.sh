#!/bin/bash

tar -xvf openjpeg.tar.gz
cd openjpeg
mkdir build
cd build
# 设置编译器
export CC=clang
export CXX=clang++

# 设置编译标志
export CFLAGS="-O0 -g"
export CXXFLAGS="-O0 -g"
cmake ..

# 编译和安装
make
make install