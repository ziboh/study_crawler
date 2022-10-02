# 1、查看是否有配置文件
# 2、查看是否有配置文件
import configparser
import os
DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(DIR, 'config.ini')


def create_config():
    config = configparser.ConfigParser()
    config['DEAFULT'] = {
        "SCRAPE_MODEL": 1,
        "BASE_URL": "https://www.sehuatang.org",
        "DELAY_TIME": 5,
        "SAVE_DIR": "sehuatang"
    }
    config["PROXY"] = {
        "OPEN_PROXY": 0,
        "PROXY": "http",
        "PROXY_ADDRESS": "192.168.2.1:7893"
    }
    
    config["LOG"] = {
        "OPEN_LOG":0,
        "LOG_DIR":"log"
    }
    
    
    config["DATA_SAVE"] ={
        "MODEL":0,
        "JSON_DIR":"data_json"
    }
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def check_config(config):
    config.read(CONFIG_PATH)
    print(config.sections())
    SAVE_DIR = os.path.join(DIR,config["DEAFULT"]["save_dir"])
    return True

def get_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        create_config()
        print("创建配置文件成功,请退出后重新启动")
        input("输入任意键退出：")
        os._exit(0)
    if check_config(config):
        return config
    else:
        os._exit(0)
    
    
if __name__ == "__main__":
    get_config()
