import argparse
import subprocess
import os
import shlex
from pathlib import Path

current_directory = Path(".").absolute().resolve()
user_id = 1000


def create_bench_args(args=None):
    bench_app_location = "/usr/local/bin/bench"

    s = [
        bench_app_location,
    ]

    if args:
        s.extend(args)

    return s


if os.environ["mysql_change_password"] == "y":
    mysql_password = os.environ["mysql_new_password"]
else:
    mysql_password = os.environ["mysql_current_password"]


admin_site_password = os.environ["frappe_bench_admin_password"]

def main():
    parser = argparse.ArgumentParser(prog="Frappe installer using bench CLI")
    parser.add_argument(
        "--init-dir",
        help="Set installation directory for frappe bench",
        required=True,
    )
    parser.add_argument("--bench-version", help="Set version for frappe bench")
    parser.add_argument("--new-site", help="Create new site in bench", action="append")
    parser.add_argument(
        "--get-app",
        help="Get app for frappe bench. Syntax: app_name;branch;repository_url",
        action="append",
    )
    parser.add_argument(
        "--install-app",
        help="Install app for frappe bench. Syntax: site;app_name",
        action="append",
    )
    parser.add_argument("--use", help="Set default site for frappe bench")

    args = parser.parse_args(shlex.split(os.environ["install_frappe_py_args"]))

    # bench init
    bench_args = create_bench_args(["init"])
    if args.bench_version:
        bench_args.extend(["--frappe-branch", args.bench_version])
    bench_args.append(args.init_dir)
    proc = subprocess.Popen(bench_args, stdin=subprocess.PIPE, user=user_id)
    proc.communicate(input=mysql_password.encode())

    os.chdir(current_directory / args.init_dir)

    # bench new-site
    for site in args.new_site:
        bench_args = create_bench_args(["new-site", site])
        proc = subprocess.Popen(bench_args, stdin=subprocess.PIPE, user=user_id)

        proc_input = ""
        # MariaDB root password
        proc_input += mysql_password + "\n"
        # Administrator password for new site
        proc_input += admin_site_password + "\n"
        # Confirmation admin new password
        proc_input += admin_site_password + "\n"

        proc.communicate(input=proc_input.encode())

    # bench get-app
    for app in args.get_app:
        app_name, branch, repo_url = app.split(";")

        bench_args = create_bench_args(["get-app"])
        bench_args.extend(["--branch", branch, app_name, repo_url])

        subprocess.run(bench_args, user=user_id)

    # bench install-app
    for app in args.install_app:
        site, app_name = app.split(";")

        bench_args = create_bench_args()
        bench_args.extend(["--site", site])
        bench_args.extend(["install-app", app_name])

        subprocess.run(bench_args, user=user_id)

    if args.use:
        subprocess.run(create_bench_args(["use", args.use]), user=user_id)


if __name__ == "__main__":
    main()
