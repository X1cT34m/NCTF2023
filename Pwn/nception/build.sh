echo "nctf{nception-test-flag-7d1634d2}" > build/flag
docker build . -t nctf2023:nception
docker tag nctf2023:nception registry.cn-hangzhou.aliyuncs.com/0xgame2023/nctf2023:nception