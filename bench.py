import subprocess
import sys
import shlex

def main():
    # Start mariadb
    subprocess.run(["service", "mariadb", "start"])

    # Start redis-server
    subprocess.run(["service", "redis-server", "start"])

    cmdargs = " ".join(map(shlex.quote, sys.argv[1:]))

    subprocess.run(["su", "frappe-bench", "-c", "NVM_DIR=/usr/local/nvm; "
                                                "NODE_VERSION=v20.17.0; "
                                                "PATH=$NVM_DIR:$PATH; "
                                                "PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH; "
                                                f"bench {cmdargs}"])


if __name__ == "__main__":
    main()