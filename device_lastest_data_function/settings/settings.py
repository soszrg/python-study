import os

env = os.getenv("ENV")

# anxin function staging databases settings
if env == "staging":

    #======PG Settings======
    PG_HOST = "" # 公网地址
    PG_PORT = 3433
    PG_DATABASE = ""
    PG_USER = ""
    PG_PASSWORD = ""

    #======MONGO Settings======
    MONGODB_HOST =""
    MONGODB_PASSWORD = ""
    MONGODB_USERNAME = ""
    MONGODB_PORT = "3717"
    MONGODB_DB = ""


# anxin function production databases settings
elif env == "production":
    #======PG Settings======
    PG_HOST = "rm-uf63je5703hs56n6l.pg.rds.aliyuncs.com"
    PG_PORT = 3433
    # PG_DATABASE = "anxin"
    # PG_USER = "anxin_production_user"
    # PG_PASSWORD = "Anxin@Production@User"
    PG_DATABASE = "anxin_pro"
    PG_USER = "postgres"
    PG_PASSWORD = "Zhrmghg@1949"

    #======MONGO Settings======
    MONGODB_HOST ="dds-uf6e3f923b9354841.mongodb.rds.aliyuncs.com"
    MONGODB_PORT = "3717"
    MONGODB_DB = "anxin"
    MONGODB_USERNAME = "anxin_production_user"
    MONGODB_PASSWORD = "Anxin_Production_User"
    

else:
    raise Exception("No Env Settings!")


THREE_PHASE_ELECTRIC_METER_PRODUCT_ID = ('decfe2450402d6a25e62416be05014', 'b6cdb13b6da93011c8c0bdd78856d3')
PRODUCT_CATEGORY_ID_DB = 1  # distribution box
PRODUCT_CATEGORY_ID_EM = 2  # electric meter
PRODUCT_CATEGORY_ID_WM = 3  # water meter
PRODUCT_CATEGORY_ID_CL = 4  # collector
PRODUCT_CATEGORY_ID_RT = 5  # repeater