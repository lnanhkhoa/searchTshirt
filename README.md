# seleniumPython #
**RUN in Windows, Linux, MAC**

## Install ##
I encourage to use `virtualenv` for this project, or make this ez with `PyCharm IDE`.

**Virtualenv:** 
 https://virtualenv.pypa.io/en/stable/installation/


**Install package with:**
`
pip install -r requirement.txt
`

## Config file ##
 in *config.py*
 
|   |   |
|---|---|
|pathImage| default folder Images|
|treePath | saving images folder for each account|
|username, password| info account|
|textsearch | text search shirts |
|enable_change_proxy|True/False|
|proxy_host, proxy_port| need US proxy change|
|type_of_run_script| this features is coming soon, now value is *1*|

**Get Proxy in :** https://free-proxy-list.net/

**Example:**
```    
DATABASE_CONFIG = dict(
    pathImage='img',
    treePath="1",
    username="username",
    password="password",
    textsearch="i want this shirt",
    proxy_host="0.0.0.0",
    proxy_port="8080",
    type_of_run_script=1  # 0 is default (testing, not release), 1 is faster run script
)
```


## Run Script ##
This project is using Python3.

`
python main.py
`
## Advices ##
*Project use PyCharm IDE*
s