import subprocess
import sys
import shlex
import os

try:
    bench_dir = os.environ["frappe_bench_dir"]
except KeyError:
    raise Exception(".env file is not initialized")

def main():
    # Start mariadb
    subprocess.run(["service", "mariadb", "start"])

    # Start redis-server
    subprocess.run(["service", "redis-server", "start"])

    cmdargs = " ".join(map(shlex.quote, sys.argv[1:]))

    os.chdir(bench_dir)

    subprocess.run(["su", "frappe-bench", "-c", "NVM_DIR=/usr/local/nvm; "
                                                "NODE_VERSION=v20.17.0; "
                                                "PATH=$NVM_DIR:$PATH; "
                                                "PATH=$NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH; "
                                                f"bench {cmdargs}"])


if __name__ == "__main__":
    main()