#!/bin/sh
# 必须使用绝对路径指向沙盒内的库
export LD_LIBRARY_PATH=/app/lib:$LD_LIBRARY_PATH
# 进入主目录执行
cd /app
exec /app/chrome_pwa_desktop_manage "$@"
