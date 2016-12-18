import six
import argparse
import subprocess


def install_salt():
    """
    Install the salt minion
    """
    from six.moves import urllib
    import tempfile
    response = urllib.request.urlopen('https://bootstrap.saltstack.com')
    bootstrap_script = response.read()
    handler, bootstrap_path = tempfile.mkstemp(suffix='.sh')
    with open(bootstrap_path, 'wb') as bootstrap_file:
        bootstrap_file.write(bootstrap_script)

    subprocess.check_call(['sudo', 'sh', bootstrap_path])

def main():
    parser = argparse.ArgumentParser(
        description='Relentlessly hammer away until your software runs.'
    )
    parser.add_argument(
        'command',
        metavar='COMMAND',
        nargs='+',
        help='Command that you want to run successfully.'
    )

    args = parser.parse_args()

    ## Detect if Salt is installed, otherwise install salt
    try:
        import salt.client
    except ImportError:
        install_salt()
        import salt.client

    mopts = salt.config.minion_config('')
    mopts.update({
        'file_client': 'local',
        'master': 'localhost',
    })

    caller = salt.client.Caller(mopts=mopts)
    output = caller.cmd('test.ping')
    print(output)


if __name__ == "__main__":
    main()
