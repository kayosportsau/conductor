import os
import time

import requests

payload = {"task2Name": "task_5"}

default_conductor_api = 'http://conductor-server.netflix-conductor-pr-108.jx.gitops-prod.streamotion.gitops.com.au/api'
default_workflow_count = 50
default_expect_spawning_time_secs = 5
default_expect_completion_time_secs = 60

conductor_api = default_conductor_api
workflow_count = int(os.getenv('EXPECT_WORKFLOW_COUNT', default_workflow_count))
expect_spawning_time_secs = float(os.getenv('EXPECT_WORKFLOW_CREATION_TIME_SECS', default_expect_spawning_time_secs))
expect_completion_time_secs = float(os.getenv('EXPECT_WORKFLOW_COMPLETION_TIME_SECS', default_expect_completion_time_secs))
print("****************************************")
print("* conductor_api:[{}]  ".format(conductor_api))
print("* workflow_count:[{}] ".format(workflow_count))
print("* expect_spawning_time_secs:[{}] ".format(expect_spawning_time_secs))
print("* expect_completion_time_secs:[{}] ".format(expect_completion_time_secs))
print("****************************************")

def count_running_worklow():
    res = requests.get('{0}/workflow/running/kitchensink?version=1'.format(conductor_api))
    return len(res.json())


def spawn():
    print("**** spawning workflow .... ****\n")
    for x in range(1, workflow_count):
        r = requests.post(
            url='{0}/workflow/kitchensink'.format(conductor_api),
            json=payload,
            headers={'content-type': 'application/json'},
            verify=False
        )
        print("{} -> {}".format(x, r.text))


start_time = time.time()

spawn()
time_to_spawn = time.time() - start_time
print(" - spawning time [{}]".format(time_to_spawn))
assert expect_spawning_time_secs > time_to_spawn, 'TIME TO CREATE WORK FLOWS MUST BE LOWER THAN [{}] secs'.format(
    expect_spawning_time_secs)

current_elapsed = time.time() - start_time

while ( count_running_worklow() > 0 ):
    time.sleep(1)
    current_elapsed = time.time() - start_time
    print("waiting until all workflow completed...")
    print("total time so far [{}]".format(current_elapsed))

assert expect_completion_time_secs > current_elapsed, 'TIME TO COMPLETE WORKLOWS MUST BE LOWER THAN [{}] secs'.format(
    expect_completion_time_secs)
