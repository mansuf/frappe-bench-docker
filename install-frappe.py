import subprocess
import pexpect
import os
from pathlib import Path

current_directory = Path(".").absolute().resolve()
user_id = 1000
user_name = "frappe-bench"


def create_bench_args(args=None):
    bench_app_location = "/usr/local/bin/bench"

    s = [
        bench_app_location,
    ]

    if args:
        s.extend(args)

    return s

try:
    if os.environ["mysql_change_password"] == "y":
        mysql_password = os.environ["mysql_new_password"]
    else:
        mysql_password = os.environ["mysql_current_password"]
except KeyError:
    raise Exception(".env file is not initialized")

def main():
    # Init mariadb
    subprocess.run(["python3", "mysql-init.py"])

    # Start mariadb
    subprocess.run(["service", "mariadb", "start"])

    # Start redis-server
    subprocess.run(["service", "redis-server", "start"])

    # Create mysql user
    # mysql -u <user> -p -e 'select * from schema.table'
    proc = pexpect.spawn("mysql", ["-u", "root", "-p", "-e", f"CREATE USER '{user_name}@localhost' IDENTIFIED BY '{mysql_password}';"])
    proc.sendline(mysql_password)
    print(proc.read())

    proc = pexpect.spawn("mysql", ["-u", "root", "-p", "-e", f"GRANT ALL PRIVILEGES ON *.* TO '{user_name}@localhost' WITH GRANT OPTION;"])
    proc.sendline(mysql_password)
    print(proc.read())

    subprocess.run(["su", "frappe-bench", "-c", "NVM_DIR=/usr/local/nvm; "
                                                "NODE_VERSION=v20.17.0; "
                                                "PATH=$NVM_DIR:$PATH; "
                                                "PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH; "
                                                "python3 _entry_installer_frappe.py"])

if __name__ == "__main__":
    main()