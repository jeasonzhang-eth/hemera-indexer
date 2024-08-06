from datetime import datetime

from sqlalchemy import Column, Index, PrimaryKeyConstraint, desc, func
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, BYTEA, NUMERIC, TIMESTAMP

from common.models import HemeraModel, general_converter


class CoinBalances(HemeraModel):
    __tablename__ = "address_coin_balances"

    address = Column(BYTEA, primary_key=True)
    balance = Column(NUMERIC(100))
    block_number = Column(BIGINT, primary_key=True)
    block_timestamp = Column(TIMESTAMP)

    create_time = Column(TIMESTAMP, default=datetime.utcnow)
    update_time = Column(TIMESTAMP, onupdate=func.now())
    reorg = Column(BOOLEAN, default=False)

    __table_args__ = (PrimaryKeyConstraint("address", "block_number"),)

    @staticmethod
    def model_domain_mapping():
        return [
            {
                "domain": "CoinBalance",
                "conflict_do_update": False,
                "update_strategy": None,
                "converter": general_converter,
            }
        ]


Index(
    "coin_balance_address_number_desc_index",
    desc(CoinBalances.address),
    desc(CoinBalances.block_number),
)