#!/usr/bin/env python3
import subprocess
import time


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f'$ {cmd}')
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f'ERROR: {result.stderr.strip()}')
    return result.returncode == 0


def activate_node(name):
    print(f'\n--- Activating {name} ---')
    run(f'ros2 lifecycle set /{name} configure')
    time.sleep(2)
    run(f'ros2 lifecycle set /{name} activate')
    time.sleep(1)


if __name__ == '__main__':
    print('Waiting 5 seconds for nodes to initialize...')
    time.sleep(5)

    activate_node('map_server')
    activate_node('amcl')
    activate_node('planner_server')
    activate_node('controller_server')
    activate_node('bt_navigator')

    print('\nAll nodes activated!')
    print('Checking states...')
    for node in ['map_server', 'amcl', 'planner_server',
                 'controller_server', 'bt_navigator']:
        run(f'ros2 lifecycle get /{node}')
