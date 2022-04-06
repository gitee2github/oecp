## 0. 背景

工具聚焦openEuler内核和基础包，检测伙伴二次发行版生态核心特性不丢失，关键配置不更改 结合社区选包策略及软件包等级策略，检查L1、L2软件包版本、打包方式、接口一致性，KABI白名单，架构特性(如鲲鹏/X86特性)使能，性能优化配置，牵引实现扩展仓库openEuler系共享、共用，主流行业应用在openEuler系不同的OSV生态复用度95%。

## 1. 运行环境

### 1.1. oecp运行环境依赖组件

| 组件      | 组件描述                                                     | 可获得性                                             |
| --------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| python3   | python3.7.9及以上| 可先通过yum list命令查看，如果没有该版本需要下载安装 |
| sqlite    | v3.7.17 及以上版本                                           | 系统自带                                             |


## 3. oecp下载安装与部署


install abidiff (centos): ''' yum install -y epel-release yum install -y libabigail '''

注意：openeuler需要配置openEuler-20.03-SP2以上版本everything仓库
install abidiff (openEulerr): ''' yum install -y libabigail '''

install oecp:
'''
git clone https://gitee.com/openeuler/oecp.git
cd oecp
pip3 install -r requirement
'''

## 4. oecp使用

`python3 cli.py [-h] [-n PARALLEL] [-w WORK_DIR] [-p PLAN_PATH]
                [-c CATEGORY_PATH] [-b PERF_BASELINE_FILE] [-a {x86_64,aarch64}]
                [-f OUTPUT_FORMAT] [-o OUTPUT_FILE]
                file1 file2`
* **位置参数(必选)**
  * **`file`**
    指定两个比较的iso文件

* **可选参数**

  * **`-n, --parallel`**
    指定`进程池并发数量`，默认cpu核数

  * **`-w, --work-dir`**
    指定`工作路径`，默认路径为/tmp/oecp
  
  * **`-p, --plan`**
    指定`比较计划`，默认为oecp/conf/plan/all.json

  * **`-c, --category`**
    指定`包级别信息`，默认为oecp/conf/category/category.json

  * **`-b, --baseline`**
    指定`基线文件`，默认为oecp/conf/performance/openEuler-20.03-LTS-aarch64-dvd.iso.performance.json


  * **`-f, --format`**
    指定`输出格式`，默认为csv

  * **`-o, --output`**
    指定`输出结果路径`，默认为/tmp/oecp
    
* **举例**

  * **` python3 cli.py  /root/openEuler-20.03-LTS-aarch64-dvd.iso /root/openEuler-20.03-LTS-SP1-aarch64-dvd.iso`**

* **比较计划说明**
  * **`all.json`**
    涵盖下面所有配置项的比较
  * **`config_file.json`**
    比较rpm包中配置文件内容的差异，需依赖RPMExtractDumper（提取解压rpm的dumper类）
  * **`filelist.json`**
    比较rpm包文件列表差异，可通过rpm -pql ${rpm_path}命令获取rpm文件列表
  * **`kconfig.json`**
    比较内核配置文件，需依赖RPMExtractDumper（提取解压rpm的dumper类）
  * **`package_list.json`**
    比较两个rpm集合包名称、版本、发行版本的差异
  * **`provides_requires.json`**
    比较rpm的provides和requires差异，可通过rpm -pq --provides/requires ${rpm_path}查询



