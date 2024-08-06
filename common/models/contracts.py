from datetime import datetime

from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, BYTEA, INTEGER, JSONB, TIMESTAMP, VARCHAR

from common.models import HemeraModel, general_converter


class Contracts(HemeraModel):
    __tablename__ = "contracts"

    address = Column(BYTEA, primary_key=True)
    name = Column(VARCHAR)
    contract_creator = Column(BYTEA)
    creation_code = Column(BYTEA)
    deployed_code = Column(BYTEA)

    block_number = Column(BIGINT)
    block_hash = Column(BYTEA)
    block_timestamp = Column(TIMESTAMP)
    transaction_index = Column(INTEGER)
    transaction_hash = Column(BYTEA)
    transaction_from_address = Column(BYTEA)

    official_website = Column(VARCHAR)
    description = Column(VARCHAR)
    email = Column(VARCHAR)
    social_list = Column(JSONB)
    is_verified = Column(BOOLEAN, default=False)
    is_proxy = Column(BOOLEAN)
    implementation_contract = Column(BYTEA)
    verified_implementation_contract = Column(BYTEA)
    proxy_standard = Column(VARCHAR)

    create_time = Column(TIMESTAMP, default=datetime.utcnow)
    update_time = Column(TIMESTAMP, onupdate=func.now())
    reorg = Column(BOOLEAN, default=False)

    @staticmethod
    def model_domain_mapping():
        return [
            {
                "domain": "Contract",
                "conflict_do_update": False,
                "update_strategy": None,
                "converter": general_converter,
            }
        ]