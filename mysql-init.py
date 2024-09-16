import subprocess
import os
import pexpect
from dotenv import load_dotenv

load_dotenv()


def verify_answer(answer="y"):
    if answer not in ["y", "n"]:
        raise Exception("invalid answer")

    return answer + "\n"


def create_mysql_init_answers(
    current_password=None,
    switch_unix_socket_auth=False,
    change_password=True,
    new_password=None,
    remove_anonymous_users=True,
    disallow_root_login_remotely=True,
    remove_test_database=True,
    reload_privilege_tables=True,
):
    string = ""

    # "Enter the current password (enter for none)"
    if current_password:
        string += current_password + "\n"
    else:
        string += "\n"

    # Switch to unix_socket authentication [Y/n] n
    string += verify_answer(switch_unix_socket_auth)

    # Change the root password ? [y/n]
    string += verify_answer(change_password)

    if change_password == "y":
        string += new_password + "\n"
        string += new_password + "\n"

    # Remove anonymous users ? [y/n]
    string += verify_answer(remove_anonymous_users)

    # Disallow root login remotely (y/n)
    string += verify_answer(disallow_root_login_remotely)

    # Remove test database and access to it ? [y/n]
    string += verify_answer(remove_test_database)

    # Reload privilege tables now? [y/n]
    string += verify_answer(reload_privilege_tables)

    return string


key_envs = [
    "mysql_current_password",
    "mysql_switch_unix_socket_auth",
    "mysql_change_password",
    "mysql_new_password",
    "mysql_remove_anonymous_users",
    "mysql_disallow_root_login_remotely",
    "mysql_remove_test_database",
    "mysql_reload_privilege_tables",
]


def main():
    # Start mariadb service
    subprocess.run(["service", "mariadb", "start"])

    env_values = {i.replace("mysql_", ""): os.environ[i] for i in key_envs}
    answers = create_mysql_init_answers(**env_values)
    proc = pexpect.spawn("mysql_secure_installation")
    for answer in answers.splitlines(keepends=False):
        proc.sendline(answer)

    output = proc.read()
    print(output)


if __name__ == "__main__":
    main()
