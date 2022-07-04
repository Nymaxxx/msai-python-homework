import asyncio
from os import stat
import re
import time
import json
import sys
import aiohttp
import random

from typing import List, Tuple
from itertools import chain

from loadtest_classes import RequestDescriptor, StageDescriptor


def read_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


async def do_timed_request(
    session: aiohttp.ClientSession, 
    request_desc: RequestDescriptor,
    timeout: int,
    max_rng_delay: float = 0.5,
) -> Tuple[int, float]:
    """Returns the async request time"""
    await asyncio.sleep(random.random() * max_rng_delay)

    status_code: int = 0
    before_request = time.time()
    try:
        async with session.request(
            request_desc.method,
            request_desc.url,
            headers=request_desc.headers,
            data=(request_desc.body if request_desc.body else "").encode(),
            timeout=timeout
        ) as resp:
            status_code = resp.status
    except asyncio.TimeoutError as timeout_err:
        return 408, time.time() - before_request
    return status_code, time.time() - before_request


def process_stage_results(stage_stats):
    processed_stage_stats = {
        "success": 0,
        "failure": 0,
        "timeout": 0,
        "avg_time": 0.0,
        "req_num": 0
    }

    sum_times = 0
    for status, req_time in chain.from_iterable(stage_stats):
        sum_times += req_time
        if 200 <= status <= 299:
            processed_stage_stats["success"] += 1
        elif status == 408:
            processed_stage_stats["timeout"] += 1
        else:
            processed_stage_stats["failure"] += 1

    requests_number = (
        processed_stage_stats["success"] 
        + processed_stage_stats["timeout"] 
        + processed_stage_stats["failure"]
    )
    processed_stage_stats["avg_time"] = sum_times / requests_number
    processed_stage_stats["success"] /= requests_number
    processed_stage_stats["timeout"] /= requests_number
    processed_stage_stats["failure"] /= requests_number

    processed_stage_stats["req_num"] = requests_number


    return processed_stage_stats


async def do_requests_with_stage(stage: StageDescriptor, requests: List[RequestDescriptor]):
    print("Starting stage...")
    rps_min, rps_max = (stage.rps_from, stage.rps_to) \
        if stage.rps_from <= stage.rps_to \
        else (stage.rps_to, stage.rps_from)

    len_requsts = len(requests)

    stage_stats = []

    for sec in range(stage.duration):
        actual_rps = random.randint(rps_min, rps_max + 1)
        print(f"Second {sec + 1}... Actual rps: {actual_rps}")
        async with aiohttp.ClientSession() as session:
            stats_futures = [do_timed_request(
                session, 
                requests[i % len_requsts],
                stage.timeout,
            ) for i in range(actual_rps)]
            await asyncio.sleep(1)  # 1 second wait to be closer to a perfect rpc score
            stage_stats.append(await asyncio.gather(*stats_futures))

    return process_stage_results(stage_stats)


async def do_section(requests: List[RequestDescriptor], stages: List[StageDescriptor]):
    for num_stage, stage in enumerate(stages):
        for repeat in range(stage.repeats):
            stats = await do_requests_with_stage(stage, requests)
            print(f"STAGE {num_stage}, REPEAT {repeat}, STATS:")
            print(f"\t#REQUESTS: {stats['req_num']}")
            print(f"\t%SUCCESS: {stats['success'] * 100:4f}," +
                f" %TIMEOUTS: {stats['timeout'] * 100:4f}," +
                f" %FAILURES: {stats['failure'] * 100:4f}")
            print(f"AVG TIME: {stats['avg_time']}")


async def main(cfg: dict):
    for section in cfg:
        requests_cfg = section["requests"]
        stages_cfg = section["stages"]

        parsed_requests: List[RequestDescriptor] = []
        for request in requests_cfg:
            parsed_requests.append(RequestDescriptor.from_cfg(request))

        parsed_stages: List[StageDescriptor] = []
        for stage in stages_cfg:
            parsed_stages.append(StageDescriptor.from_cfg(parsed_requests, stage))

        await do_section(parsed_requests, parsed_stages)


if __name__ == "__main__":
    cfg = read_config(sys.argv[1])
    asyncio.run(main(cfg))