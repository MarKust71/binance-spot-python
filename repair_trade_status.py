"""
This module deletes all trades from the database.
"""


from db.utils.db_repair_trade_status import db_repair_trade_status


if __name__ == '__main__':
    db_repair_trade_status()
    print("All trades repaired.")
