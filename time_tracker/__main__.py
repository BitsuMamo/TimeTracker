from time import sleep
from time_tracker.activity import Activity


def app_change() -> None:
    global a
    print(f"Now running {a.current_app}. Changed at: {a.current_app_start_time}")


def infinite_loop_2():
    while True:
        print("Loop isn't blocked")
        sleep(0.2)


a = Activity()

if __name__ == "__main__":
    a.subscribe(app_change)
    infinite_loop_2()

