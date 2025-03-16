"""
This module deletes all trades from the database.
"""
from db.utils.db_repair_take_profit_safe import db_repair_take_profit_safe


if __name__ == '__main__':
    db_repair_take_profit_safe()
    print("All trades repaired.")
