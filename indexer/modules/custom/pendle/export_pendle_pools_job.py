import logging
from typing import List

from web3 import Web3

from common.utils.web3_utils import event_topic_to_address
from indexer.domain.log import Log
from indexer.domain.transaction import Transaction
from indexer.executors.batch_work_executor import BatchWorkExecutor
from indexer.jobs import FilterTransactionDataJob
from indexer.modules.custom.pendle.abi.event import *
from indexer.modules.custom.pendle.abi.function import *
from indexer.modules.custom.pendle.domains.market import PendlePoolD
from indexer.specification.specification import TopicSpecification, TransactionFilterByLogs
from indexer.utils.multicall_hemera import Call
from indexer.utils.multicall_hemera.multi_call_helper import MultiCallHelper

logger = logging.getLogger(__name__)


class PendlePoolsJob(FilterTransactionDataJob):
    dependency_types = [Transaction]
    output_types = [PendlePoolD]
    able_to_reorg = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._batch_work_executor = BatchWorkExecutor(
            kwargs["batch_size"],
            kwargs["max_workers"],
            job_name=self.__class__.__name__,
        )
        self._is_batch = kwargs["batch_size"] > 1
        self._filters = kwargs.get("filters", [])
        self.multicall_helper = MultiCallHelper(
            self._web3, {"batch_size": kwargs["batch_size"], "multicall": True, "max_workers": kwargs["max_workers"]}
        )

    def get_filter(self):
        return [
            TransactionFilterByLogs(
                [
                    TopicSpecification(
                        addresses=[
                            self.user_defined_config["pendle_market_factory_address"],
                            self.user_defined_config["pendle_market_factory_v3_address"],
                        ],
                        topics=[create_market_event.get_signature()],
                    )
                ]
            ),
        ]

    def _collect(self, **kwargs):
        pass

    def _process(self, **kwargs):
        logs: List[Log] = self._data_buff.get(Log.type(), [])
        if len(logs) == 0:
            return
        calls = []
        pools = {}
        for log in logs:
            if log.address not in [
                self.user_defined_config["pendle_market_factory_address"],
                self.user_defined_config["pendle_market_factory_v3_address"],
            ]:
                continue
            if log.topic0 not in [create_market_event.get_signature(), create_market_event_v3.get_signature()]:
                continue
            market_address = event_topic_to_address(log.topic1)

            pt_address = event_topic_to_address(log.topic2)
            pools[pt_address] = PendlePoolD(
                market_address=market_address,
                pt_address=pt_address,
                block_number=log.block_number,
                chain_id=self._chain_id,
                yt_address="",
                sy_address="",
                underlying_asset="",
            )
            calls.append(
                Call(
                    target=pt_address,
                    function_abi=get_sy_by_pt,
                    block_number=log.block_number,
                    parameters=[],
                )
            )
            calls.append(
                Call(
                    target=pt_address,
                    function_abi=get_yt_by_pt,
                    block_number=log.block_number,
                    parameters=[],
                )
            )

        if len(calls) == 0:
            return
        self.multicall_helper.execute_calls(calls)
        yield_asset_calls = []
        for call in calls:
            if "yt" in call.returns:
                pools[call.target].yt_address = call.returns["yt"]
            if "sy" in call.returns:
                pools[call.target].sy_address = call.returns["sy"]
                yield_asset_calls.append(
                    Call(
                        target=pools[call.target].sy_address,
                        function_abi=yield_token_function,
                        block_number=call.block_number,
                        parameters=[],
                    )
                )

        self.multicall_helper.execute_calls(yield_asset_calls)
        sy_to_yield = {}
        for call in yield_asset_calls:
            sy_to_yield[call.target.lower()] = call.returns["yield_token"]

        for pool in pools.values():
            pool.underlying_asset = sy_to_yield[pool.sy_address.lower()]
            self._collect_domain(pool)
