from dotenv import load_dotenv
import os 
load_dotenv()

class AcessoENV():

    def __init__(self) -> None:
        pass
    
    def acessoDB(self):
        DB = {
            "database":os.getenv("DATABASE"),
            "user":os.getenv("USER"),
            "password":os.getenv("PASSOWORD"),
            "host":os.getenv("HOST"),
            "port":os.getenv("PORT")
        }
        return DB
    
    def acessoAPP(self):
        APP = {
            "versao":os.getenv("VERSAO"),
            "port":os.getenv("PORTSERV")
        }
        return APP
