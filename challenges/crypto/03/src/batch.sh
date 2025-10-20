#!/bin/bash

# 要执行的脚本名
SCRIPT="49_fj.py"

# 检查文件是否存在
if [ ! -f "$SCRIPT" ]; then
    echo "错误：找不到脚本 '$SCRIPT'"
    exit 1
fi

# 设置执行次数
COUNT=800
COUNT=3 #generate sample problem.
echo "开始执行 $SCRIPT 共 $COUNT 次..."

# 循环执行
for ((i=1; i<=COUNT; i++))
do
    echo "第 $i 次执行..."
    # 使用Python解释器执行脚本，并捕获输出
    python3 "$SCRIPT"
    # 检查上一次命令的退出状态
    if [ $? -ne 0 ]; then
        echo "第 $i 次执行失败"
        # 可以选择退出或者继续
        # exit 1
    fi
done

echo "执行完成"