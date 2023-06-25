from drive import ContainerValuesDriver, ContainerSettingsDriver
import csv
from threading import Thread
from time import time, sleep
from pathlib import Path
import sched
from task import Task
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


SCHEDULE_FILE = './schedule.csv'


def create_schedule_file():
    container_values = ContainerValuesDriver().read_values()
    tasks = [Task(container.name) for container in container_values]

    with open(SCHEDULE_FILE, 'w', newline='') as schedule_file:
        csv_writer = csv.DictWriter(schedule_file, fieldnames=Task.fieldnames())
        csv_writer.writeheader()
        for task in tasks:
            csv_writer.writerow(task.written())


def set_temperature(container: str, temperature: str):
    try:
        ContainerSettingsDriver().set_temperature(
            container=container,
            temperature=temperature)
    except Exception as ex:
        print(f'{ex}')
        sleep(60)
        set_temperature(container, temperature)


def schedule_temperature_setting(task: Task):
    scheduler = sched.scheduler(time, sleep)
    kwargs = {'container': task.container, 'temperature': task.temperature}
    scheduler.enterabs(task.timestamp, 0, set_temperature, kwargs=kwargs)
    scheduler.run()


def read_schedule() -> list[Task]:
    with open(SCHEDULE_FILE, newline='') as schedule_file:
        schedule_reader = csv.DictReader(schedule_file)
        schedule = [Task(**row).being_read() for row in schedule_reader]
    return schedule


def run_schedule():
    tasks = read_schedule()
    processes = []
    for task in tasks:
        if time() < task.timestamp:
            process = Thread(target=schedule_temperature_setting, args=(task,))
            processes.append(process)
            process.start()
    for proc in processes:
        proc.join()


def create_file_if_not_run():
    schedule_file_path = Path(SCHEDULE_FILE)
    if not schedule_file_path.is_file():
        create_schedule_file()
        exit()
    run_schedule()


if __name__ == '__main__':
    create_file_if_not_run()
