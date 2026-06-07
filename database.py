from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:Aas%402007@localhost/hrms"

engine = create_engine(DATABASE_URL)