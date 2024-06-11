from datetime import datetime
from sqlalchemy import Column, PrimaryKeyConstraint, Index, desc
from sqlalchemy.dialects.postgresql import BYTEA, BIGINT, TIMESTAMP, NUMERIC, VARCHAR, JSONB
from exporters.jdbc.schema import Base


class ERC721TokenIdDetails(Base):
    __tablename__ = 'erc721_token_id_details'

    address = Column(BYTEA, primary_key=True)
    token_id = Column(NUMERIC(78), primary_key=True)
    token_owner = Column(BYTEA)
    token_uri = Column(VARCHAR)
    token_uri_info = Column(JSONB)

    block_number = Column(BIGINT)
    block_timestamp = Column(TIMESTAMP)

    create_time = Column(TIMESTAMP, default=datetime.utcnow)
    update_time = Column(TIMESTAMP)

    __table_args__ = (
        PrimaryKeyConstraint('address', 'token_id'),
    )


Index('erc721_detail_owner_address_id_index',
      desc(ERC721TokenIdDetails.token_owner), ERC721TokenIdDetails.address, ERC721TokenIdDetails.token_id)