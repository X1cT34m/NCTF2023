echo "nctf{npointment-test-flag-fc94ed89}" > build/flag
docker build . -t nctf2023:npointment
docker tag nctf2023:npointment registry.cn-hangzhou.aliyuncs.com/0xgame2023/nctf2023:npointment
