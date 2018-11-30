#! /usr/bin/env bash

# desc:replace wrong words
# set -e

declare -A WORDS

WORDS=(
    ["请稍后"]="请稍候"
    ["登录"]="登录"
    ["重起"]="重启"
    ["冲值"]="充值"
    ["阀值"]="阈值"
)

# echo ${WORDS[@]}
# echo ${!WORDS[@]}
for word in "${!WORDS[@]}"; do 
    echo "INFO    -  Replace$word -2-> ${WORDS[$word]}"
    
    if [ -n "$1" ];then
        dir_path=$1
    else
        dir_path="."
    fi
    word_path=$(grep -rlE "$word" $dir_path)
    if [ -n "$word_path" ];then
        sed -i -E "s/$word/${WORDS[$word]}/g" $word_path
        echo -e "INFO    -  Changeed $word in -> \n$word_path"
    else
        echo "INFO    -  No files containing $word"
    fi
done

echo "INFO    -  Replace Words Done!"
