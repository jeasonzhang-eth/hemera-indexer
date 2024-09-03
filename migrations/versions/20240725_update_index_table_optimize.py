"""update index & table optimize

Revision ID: 9f2cf385645f
Revises: b15f744e8582
Create Date: 2024-07-25 10:53:54.958874

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9f2cf385645f"
down_revision: Union[str, None] = "b15f744e8582"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "address_current_token_balances",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=True),
        sa.Column("token_type", sa.VARCHAR(), nullable=True),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("balance", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("address", "token_address", "token_id"),
    )
    op.create_index(
        "current_token_balances_token_address_balance_of_index",
        "address_current_token_balances",
        ["token_address", sa.text("balance DESC")],
        unique=False,
    )
    op.create_index(
        "current_token_balances_token_address_id_balance_of_index",
        "address_current_token_balances",
        ["token_address", "token_id", sa.text("balance DESC")],
        unique=False,
    )
    op.drop_index(
        "erc721_token_holders_token_address_balance_of_index",
        table_name="erc721_token_holders",
    )
    op.drop_table("erc721_token_holders")
    op.drop_index(
        "erc20_token_holders_token_address_balance_of_index",
        table_name="erc20_token_holders",
    )
    op.drop_table("erc20_token_holders")
    op.drop_table("wallet_addresses")
    op.drop_index(
        "erc1155_token_holders_token_address_balance_of_index",
        table_name="erc1155_token_holders",
    )
    op.drop_table("erc1155_token_holders")
    op.create_index(
        "coin_balance_address_number_desc_index",
        "address_coin_balances",
        [sa.text("address DESC"), sa.text("block_number DESC")],
        unique=False,
    )
    op.create_index(
        "token_balance_address_id_number_index",
        "address_token_balances",
        [
            "address",
            "token_address",
            sa.text("token_id DESC"),
            sa.text("block_number DESC"),
        ],
        unique=False,
    )
    op.add_column("blocks", sa.Column("blob_gas_used", sa.NUMERIC(precision=100), nullable=True))
    op.add_column("blocks", sa.Column("excess_blob_gas", sa.NUMERIC(precision=100), nullable=True))
    op.add_column("blocks", sa.Column("traces_count", sa.BIGINT(), nullable=True))
    op.add_column("blocks", sa.Column("internal_transactions_count", sa.BIGINT(), nullable=True))
    op.create_index(
        "blocks_hash_unique_when_not_reorg",
        "blocks",
        ["hash"],
        unique=True,
        postgresql_where=sa.text("reorg = false"),
    )
    op.create_index(
        "blocks_number_unique_when_not_reorg",
        "blocks",
        ["number"],
        unique=True,
        postgresql_where=sa.text("reorg = false"),
    )
    op.drop_index(
        "internal_transactions_address_number_transaction_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "internal_transactions_block_timestamp_index",
        table_name="contract_internal_transactions",
    )
    op.create_index(
        "internal_transactions_block_number_index",
        "contract_internal_transactions",
        [sa.text("block_number DESC")],
        unique=False,
    )
    op.create_index(
        "internal_transactions_from_address_number_transaction_index",
        "contract_internal_transactions",
        [
            "from_address",
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "internal_transactions_number_transaction_index",
        "contract_internal_transactions",
        [sa.text("block_number DESC"), sa.text("transaction_index DESC")],
        unique=False,
    )
    op.create_index(
        "internal_transactions_to_address_number_transaction_index",
        "contract_internal_transactions",
        ["to_address", sa.text("block_number DESC"), sa.text("transaction_index DESC")],
        unique=False,
    )
    op.drop_index("erc1155_detail_desc_address_id_index", table_name="erc1155_token_id_details")
    op.drop_constraint("erc1155_token_id_details_pkey", "erc1155_token_id_details", type_="primary")
    op.alter_column("erc1155_token_id_details", "address", new_column_name="token_address")
    op.create_index(
        "erc1155_detail_desc_address_id_index",
        "erc1155_token_id_details",
        [sa.text("token_address DESC"), "token_id"],
        unique=False,
    )
    op.create_primary_key(
        "erc1155_token_id_details_pkey",
        "erc1155_token_id_details",
        ["token_address", "token_id"],
    )
    op.alter_column(
        "erc1155_token_transfers",
        "token_id",
        existing_type=sa.NUMERIC(precision=78, scale=0),
        nullable=False,
    )
    op.alter_column(
        "erc1155_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=False,
    )
    op.drop_index(
        "erc1155_token_transfers_address_block_number_log_index_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_block_timestamp_index",
        table_name="erc1155_token_transfers",
    )
    op.create_index(
        "erc1155_token_transfers_from_address_number_log_index_index",
        "erc1155_token_transfers",
        ["from_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_number_log_index",
        "erc1155_token_transfers",
        [sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_to_address_number_log_index_index",
        "erc1155_token_transfers",
        ["to_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_token_address_from_index",
        "erc1155_token_transfers",
        ["token_address", "from_address"],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_token_address_id_index",
        "erc1155_token_transfers",
        ["token_address", "token_id"],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_token_address_number_log_index_index",
        "erc1155_token_transfers",
        ["token_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_token_address_to_index",
        "erc1155_token_transfers",
        ["token_address", "to_address"],
        unique=False,
    )
    op.alter_column(
        "erc20_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=False,
    )
    op.drop_index(
        "erc20_token_transfers_address_block_number_log_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index(
        "erc20_token_transfers_block_timestamp_index",
        table_name="erc20_token_transfers",
    )
    op.create_index(
        "erc20_token_transfers_from_address_number_log_index_index",
        "erc20_token_transfers",
        ["from_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_number_log_index",
        "erc20_token_transfers",
        [sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_to_address_number_log_index_index",
        "erc20_token_transfers",
        ["to_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_token_address_from_index_index",
        "erc20_token_transfers",
        ["token_address", "from_address"],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_token_address_number_log_index_index",
        "erc20_token_transfers",
        ["token_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_token_address_to_index_index",
        "erc20_token_transfers",
        ["token_address", "to_address"],
        unique=False,
    )

    op.drop_index(
        "erc721_change_address_id_number_desc_index",
        table_name="erc721_token_id_changes",
    )
    op.drop_constraint("erc721_token_id_changes_pkey", "erc721_token_id_changes", type_="primary")
    op.alter_column("erc721_token_id_changes", "address", new_column_name="token_address")
    op.create_index(
        "erc721_change_address_id_number_desc_index",
        "erc721_token_id_changes",
        ["token_address", "token_id", sa.text("block_number DESC")],
        unique=False,
    )
    op.create_primary_key(
        "erc721_token_id_changes_pkey",
        "erc721_token_id_changes",
        ["token_address", "token_id", "block_number"],
    )

    op.drop_index("erc721_detail_owner_address_id_index", table_name="erc721_token_id_details")
    op.drop_constraint("erc721_token_id_details_pkey", "erc721_token_id_details", type_="primary")
    op.alter_column("erc721_token_id_details", "address", new_column_name="token_address")
    op.create_index(
        "erc721_detail_owner_address_id_index",
        "erc721_token_id_details",
        [sa.text("token_owner DESC"), "token_address", "token_id"],
        unique=False,
    )
    op.create_primary_key(
        "erc721_token_id_details_pkey",
        "erc721_token_id_details",
        ["token_address", "token_id"],
    )

    op.alter_column(
        "erc721_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=False,
    )
    op.drop_index(
        "erc721_token_transfers_address_block_number_log_index_index",
        table_name="erc721_token_transfers",
    )
    op.create_index(
        "erc721_token_transfers_from_address_number_log_index_index",
        "erc721_token_transfers",
        ["from_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_number_log_index",
        "erc721_token_transfers",
        [sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_to_address_number_log_index_index",
        "erc721_token_transfers",
        ["to_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_token_address_from_index",
        "erc721_token_transfers",
        ["token_address", "from_address"],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_token_address_id_index",
        "erc721_token_transfers",
        ["token_address", "token_id"],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_token_address_number_log_index_index",
        "erc721_token_transfers",
        ["token_address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_token_address_to_index",
        "erc721_token_transfers",
        ["token_address", "to_address"],
        unique=False,
    )
    op.drop_column("erc721_token_transfers", "token_uri")
    op.alter_column("logs", "block_hash", existing_type=postgresql.BYTEA(), nullable=False)
    op.create_index(
        "logs_address_topic_0_number_log_index_index",
        "logs",
        ["address", "topic0", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "logs_block_number_log_index_index",
        "logs",
        [sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index("tokens_name_index", "tokens", ["name"], unique=False)
    op.create_index(
        "tokens_type_holders_index",
        "tokens",
        ["token_type", sa.text("holder_count DESC")],
        unique=False,
    )
    op.create_index(
        "tokens_type_on_chain_market_cap_index",
        "tokens",
        ["token_type", sa.text("on_chain_market_cap DESC")],
        unique=False,
    )
    op.drop_index("traces_address_block_timestamp_index", table_name="traces")
    op.create_index(
        "traces_block_number_index",
        "traces",
        [sa.text("block_number DESC")],
        unique=False,
    )
    op.create_index(
        "traces_from_address_block_number_index",
        "traces",
        ["from_address", sa.text("block_number DESC")],
        unique=False,
    )
    op.create_index(
        "traces_to_address_block_number_index",
        "traces",
        ["to_address", sa.text("block_number DESC")],
        unique=False,
    )
    op.add_column(
        "transactions",
        sa.Column(
            "method_id",
            sa.VARCHAR(),
            sa.Computed(
                "substr(input :: pg_catalog.varchar, 3, 8)",
            ),
            nullable=True,
        ),
    )
    op.drop_index("transactions_address_block_number_transaction_idx", table_name="transactions")
    op.drop_index("transactions_block_timestamp_block_number_index", table_name="transactions")
    op.create_index(
        "transactions_block_number_transaction_index",
        "transactions",
        [sa.text("block_number DESC"), sa.text("transaction_index DESC")],
        unique=False,
    )
    op.create_index(
        "transactions_block_timestamp_index",
        "transactions",
        ["block_timestamp"],
        unique=False,
    )
    op.create_index(
        "transactions_from_address_block_number_transaction_idx",
        "transactions",
        [
            sa.text("from_address ASC"),
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "transactions_to_address_block_number_transaction_idx",
        "transactions",
        [
            sa.text("to_address ASC"),
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "transactions_to_address_block_number_transaction_idx",
        table_name="transactions",
    )
    op.drop_index(
        "transactions_from_address_block_number_transaction_idx",
        table_name="transactions",
    )
    op.drop_index("transactions_block_timestamp_index", table_name="transactions")
    op.drop_index("transactions_block_number_transaction_index", table_name="transactions")
    op.create_index(
        "transactions_block_timestamp_block_number_index",
        "transactions",
        [sa.text("block_timestamp DESC"), sa.text("block_number DESC")],
        unique=False,
    )
    op.create_index(
        "transactions_address_block_number_transaction_idx",
        "transactions",
        [
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.drop_column("transactions", "method_id")
    op.drop_index("traces_to_address_block_number_index", table_name="traces")
    op.drop_index("traces_from_address_block_number_index", table_name="traces")
    op.drop_index("traces_block_number_index", table_name="traces")
    op.create_index(
        "traces_address_block_timestamp_index",
        "traces",
        ["from_address", "to_address", sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.drop_index("tokens_type_on_chain_market_cap_index", table_name="tokens")
    op.drop_index("tokens_type_holders_index", table_name="tokens")
    op.drop_index("tokens_name_index", table_name="tokens")
    op.drop_index("logs_block_number_log_index_index", table_name="logs")
    op.drop_index("logs_address_topic_0_number_log_index_index", table_name="logs")
    op.alter_column("logs", "block_hash", existing_type=postgresql.BYTEA(), nullable=True)
    op.add_column(
        "erc721_token_transfers",
        sa.Column(
            "token_uri",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_index(
        "erc721_token_transfers_token_address_to_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index(
        "erc721_token_transfers_token_address_number_log_index_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index(
        "erc721_token_transfers_token_address_id_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index(
        "erc721_token_transfers_token_address_from_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index(
        "erc721_token_transfers_to_address_number_log_index_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index("erc721_token_transfers_number_log_index", table_name="erc721_token_transfers")
    op.drop_index(
        "erc721_token_transfers_from_address_number_log_index_index",
        table_name="erc721_token_transfers",
    )
    op.create_index(
        "erc721_token_transfers_address_block_number_log_index_index",
        "erc721_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.alter_column(
        "erc721_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=True,
    )

    op.drop_index("erc721_detail_owner_address_id_index", table_name="erc721_token_id_details")
    op.drop_constraint("erc721_token_id_details_pkey", "erc721_token_id_details", type_="primary")
    op.alter_column("erc721_token_id_details", "token_address", new_column_name="address")
    op.create_index(
        "erc721_detail_owner_address_id_index",
        "erc721_token_id_details",
        [sa.text("token_owner DESC"), "address", "token_id"],
        unique=False,
    )
    op.create_primary_key(
        "erc721_token_id_details_pkey",
        "erc721_token_id_details",
        ["address", "token_id"],
    )

    op.drop_index(
        "erc721_change_address_id_number_desc_index",
        table_name="erc721_token_id_changes",
    )
    op.drop_constraint("erc721_token_id_changes_pkey", "erc721_token_id_changes", type_="primary")
    op.alter_column("erc721_token_id_changes", "token_address", new_column_name="address")
    op.create_index(
        "erc721_change_address_id_number_desc_index",
        "erc721_token_id_changes",
        ["address", "token_id", sa.text("block_number DESC")],
        unique=False,
    )
    op.create_primary_key(
        "erc721_token_id_changes_pkey",
        "erc721_token_id_changes",
        ["address", "token_id", "block_number"],
    )

    op.drop_index(
        "erc20_token_transfers_token_address_to_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index(
        "erc20_token_transfers_token_address_number_log_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index(
        "erc20_token_transfers_token_address_from_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index(
        "erc20_token_transfers_to_address_number_log_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index("erc20_token_transfers_number_log_index", table_name="erc20_token_transfers")
    op.drop_index(
        "erc20_token_transfers_from_address_number_log_index_index",
        table_name="erc20_token_transfers",
    )
    op.create_index(
        "erc20_token_transfers_block_timestamp_index",
        "erc20_token_transfers",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_address_block_number_log_index_index",
        "erc20_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.alter_column(
        "erc20_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=True,
    )
    op.drop_index(
        "erc1155_token_transfers_token_address_to_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_token_address_number_log_index_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_token_address_id_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_token_address_from_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_to_address_number_log_index_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index("erc1155_token_transfers_number_log_index", table_name="erc1155_token_transfers")
    op.drop_index(
        "erc1155_token_transfers_from_address_number_log_index_index",
        table_name="erc1155_token_transfers",
    )
    op.create_index(
        "erc1155_token_transfers_block_timestamp_index",
        "erc1155_token_transfers",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_address_block_number_log_index_index",
        "erc1155_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.alter_column(
        "erc1155_token_transfers",
        "block_hash",
        existing_type=postgresql.BYTEA(),
        nullable=True,
    )
    op.alter_column(
        "erc1155_token_transfers",
        "token_id",
        existing_type=sa.NUMERIC(precision=78, scale=0),
        nullable=True,
    )
    op.drop_index("erc1155_detail_desc_address_id_index", table_name="erc1155_token_id_details")
    op.drop_constraint("erc1155_token_id_details_pkey", "erc1155_token_id_details", type_="primary")
    op.alter_column("erc1155_token_id_details", "token_address", new_column_name="address")
    op.create_index(
        "erc1155_detail_desc_address_id_index",
        "erc1155_token_id_details",
        [sa.text("address DESC"), "token_id"],
        unique=False,
    )
    op.create_primary_key(
        "erc1155_token_id_details_pkey",
        "erc1155_token_id_details",
        ["address", "token_id"],
    )
    op.drop_index(
        "internal_transactions_to_address_number_transaction_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "internal_transactions_number_transaction_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "internal_transactions_from_address_number_transaction_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "internal_transactions_block_number_index",
        table_name="contract_internal_transactions",
    )
    op.create_index(
        "internal_transactions_block_timestamp_index",
        "contract_internal_transactions",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_index(
        "internal_transactions_address_number_transaction_index",
        "contract_internal_transactions",
        [
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.drop_index(
        "blocks_number_unique_when_not_reorg",
        table_name="blocks",
        postgresql_where=sa.text("reorg = false"),
    )
    op.drop_index(
        "blocks_hash_unique_when_not_reorg",
        table_name="blocks",
        postgresql_where=sa.text("reorg = false"),
    )
    op.drop_column("blocks", "internal_transactions_count")
    op.drop_column("blocks", "traces_count")
    op.drop_column("blocks", "excess_blob_gas")
    op.drop_column("blocks", "blob_gas_used")
    op.drop_index("token_balance_address_id_number_index", table_name="address_token_balances")
    op.drop_index("coin_balance_address_number_desc_index", table_name="address_coin_balances")
    op.create_table(
        "erc1155_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column(
            "token_id",
            sa.NUMERIC(precision=78, scale=0),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "balance_of",
            sa.NUMERIC(precision=100, scale=0),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "latest_call_contract_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("block_number", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "block_timestamp",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("create_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint(
            "token_address",
            "wallet_address",
            "token_id",
            name="erc1155_token_holders_pkey",
        ),
    )
    op.create_index(
        "erc1155_token_holders_token_address_balance_of_index",
        "erc1155_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.create_table(
        "wallet_addresses",
        sa.Column("address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column("ens_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("address", name="wallet_addresses_pkey"),
    )
    op.create_table(
        "erc20_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column(
            "balance_of",
            sa.NUMERIC(precision=100, scale=0),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("block_number", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "block_timestamp",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("create_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("token_address", "wallet_address", name="erc20_token_holders_pkey"),
    )
    op.create_index(
        "erc20_token_holders_token_address_balance_of_index",
        "erc20_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.create_table(
        "erc721_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column(
            "balance_of",
            sa.NUMERIC(precision=100, scale=0),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("block_number", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "block_timestamp",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("create_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("token_address", "wallet_address", name="erc721_token_holders_pkey"),
    )
    op.create_index(
        "erc721_token_holders_token_address_balance_of_index",
        "erc721_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.drop_index(
        "current_token_balances_token_address_id_balance_of_index",
        table_name="address_current_token_balances",
    )
    op.drop_index(
        "current_token_balances_token_address_balance_of_index",
        table_name="address_current_token_balances",
    )
    op.drop_table("address_current_token_balances")
    # ### end Alembic commands ###
