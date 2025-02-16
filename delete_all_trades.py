"""
This module deletes all trades from the database.
"""


from db.utils.db_delete_all_trades import db_delete_all_trades


if __name__ == '__main__':
    db_delete_all_trades()
    print("All trades deleted.")
