#!/bin/bash
# 四庫全書逐句校對

TXT_FILE="$1"
MISS="$2"

if [ ! -f "$TXT_FILE" ]; then
	echo "[ERROR]: Invalid file $TXT_FILE"
	exit 1
fi

if [ "$MISS" == "" ]; then
    WORD="failed"
	ACT="Missing"
	echo " * 正在檢查《四庫全書》中並不存在的句子，用於發現文本中可能的訛誤......"
else
    WORD="ok"
	ACT="Found"
	echo " * 正在檢查《四庫全書》中可能存在的句子，用於補充原始文本中的缺字......"
fi

URL="http://127.0.0.1:5000/check"
for i in  $(grep -Ev '(\#|:)' $TXT_FILE|perl -pe 's/(︰|﹕|』|『|，|。|、|：|？|！|「|」|《|》|；)/\n/g' | perl -pe 's/（.*?）//g;s/\(.*?\)//g;'|grep -Ev "(\#|:|‧|^$)|grep -v '#'"); do
	if [ $(curl -sS "$URL" -X POST   --data-raw "text=$i&dynasty=&author=&title=&qc=%E6%90%9C%E7%B4%A2") == "$WORD" ]; then
		echo "$ACT $i"
	fi
done
