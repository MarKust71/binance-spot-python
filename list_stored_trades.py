from db.utils import db_list_trades

df = db_list_trades()

if __name__ == '__main__':
    print(df)
