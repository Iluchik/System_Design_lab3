import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://stud:stud@postgreDB/archdb", echo = True)

data = {
	"first_name": ["Ivan", "Petr", "User"],
	"last_name": ["Ivanov", "Petrov", "Useov"],
	"email": ["ii@email.com", "pp@yandex.ru", "uu@umail.use"],
	"password": ["qwerty", "ytrewq", "userty"],
	"age": ["22", "44", ""],
	"adress": ["Moscow", "notMoscow", ""],
	"phone": ["", "", "+7 (777) 777-77-77"]
}
df = pd.DataFrame(data)
df.to_sql("users", con=engine, if_exists = "append", index=False)
data = {
	"sender_id": [1, 2, 3],
	"recipient_id": [2, 3, 1],
	"package_weight": [.4, 2.3, 24],
	"package_dimensions": [0.52, 0.68, 1.6],
	"package_descriptions": ["Конверт. Документы", "Хрупкое. Электоника(ноутбук)", "Тяжелое. Спортинвентарь(гантели)"]
}
df = pd.DataFrame(data)
df.to_sql("packages", con=engine, if_exists = "append", index=False)