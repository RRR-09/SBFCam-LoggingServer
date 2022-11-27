from argparse import ArgumentParser
from datetime import datetime
from json import load as load_json
from re import findall
from subprocess import CalledProcessError, Popen, check_output  # nosec
from time import sleep
from typing import Dict, Optional

from pytz import timezone


def get_est_time() -> str:
    """
    Gets the current time and converts it EST, and a readable string
    """
    desired_timezone = timezone("America/Toronto")
    output_datetime = datetime.now(desired_timezone)
    return output_datetime.strftime("%Y-%b-%d %I:%M:%S %p EST")


def do_log(message: str, tag: Optional[str] = None):
    """
    Prints a message with a formatted EST time and optional process tag
    """
    # TODO: Just use the logging library instead
    if tag:
        print(f"[{get_est_time()}] [{tag}] {message}")
    else:
        print(f"[{get_est_time()}] {message}")


def launch(config: Dict):
    do_log(f"Launching {config['process_name']}")
    bash_cmd = f'cd "{config["directory"]}";{config["launch_command"]}'
    screen_cmd = f'screen -A -m -d -S {config["process_name"]} bash -c "{bash_cmd}"'
    Popen(screen_cmd, shell=True)  # nosec


def check(config: Dict) -> bool:
    screens_list_output = ""
    try:
        process_output = check_output(["screen", "-list"])
        screens_list_output = process_output.decode().lower()
    except CalledProcessError as e:
        exception_output = e.output
        screens_list_output = exception_output.decode()

    running_processes = findall(r"[0-9]*\.(.*?)\t", screens_list_output.lower())

    if config["process_name"] not in running_processes:
        do_log(f"{config['process_name']} not running")
        return False
    return True


def main_loop(bot_config: Dict):
    do_log("Started monitoring")
    while True:
        bot_active = check(bot_config)
        if not bot_active:
            launch(bot_config)
        sleep(1)


def main_init():
    do_log("Initializing...")
    parser = ArgumentParser(description="Server watchdog arguments.")
    parser.add_argument(
        "--config",
        help="Filepath for the config JSON file",
        default="watchdog_config.json",
    )
    args = parser.parse_args()
    config_file_name = str(args.config)
    with open(config_file_name, "r", encoding="utf-8") as config_file:
        loaded_config = load_json(config_file)
    config = loaded_config
    config["service_vars"]["process_name"] = (
        config["service_vars"]["process_name"].replace(" ", "").lower()
    )
    config["watchdog_vars"]["process_name"] = (
        config["watchdog_vars"]["process_name"].replace(" ", "").lower()
    )

    watchdog_active = check(config["watchdog_vars"])
    if not watchdog_active:  # Check if we're running in a screen or not, easy launch
        launch(config["watchdog_vars"])
        exit()

    do_log("Initialized")
    bot_active = check(config["bot_vars"])
    do_log(f"Bot is {'active' if bot_active else 'inactive'}")

    main_loop(config["bot_vars"])


if __name__ == "__main__":
    main_init()
