```
sudo docker build --no-cache -t daily-rainfall-sls . && 
sudo docker run --rm -v $PWD:/export daily-rainfall-sls cp daily-rainfall-sls.zip /export
```