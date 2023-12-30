echo "nctf{checkin-test-flag-ce624708}" > build/flag
docker build . -t nctf2023:checkin
docker tag nctf2023:checkin registry.cn-hangzhou.aliyuncs.com/0xgame2023/nctf2023:checkin
