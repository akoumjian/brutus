from __future__ import print_function
import six
import argparse
import subprocess, shlex


class Brutus():

    def __init__(self, parser=None, **kwargs):
        self.parser = parser
        self.args = parser.parse_args()
        self.command = self.args.command[0]
        self.salt_client = self.load_salt_client()
        self.return_val = None
        self.error = None

    def handle_error(self):
        if self.error is None:
            return

        ## Detect error type and attempt to fix it

    def run(self):
        self.handle_error()
        try:
            self.return_val = self.run_command()
            self.error = None
        except subprocess.CalledProcessError as e:
            self.error = e
            self.run()

    def run_command(self):
        as_args = shlex.split(self.command)
        return subprocess.check_output(
            as_args,
            stderr=subprocess.STDOUT
        )

    def __install_salt(self):
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

    def load_salt_client(self):
        ## Detect if Salt is installed, otherwise install salt
        try:
            import salt.client
        except ImportError:
            self.__install_salt()
            import salt.client

        ## Use local only config
        mopts = salt.config.minion_config('')
        mopts.update({
            'file_client': 'local',
            'master': 'localhost',
        })

        caller = salt.client.Caller(mopts=mopts)
        return caller


def main():
    parser = argparse.ArgumentParser(
        description='Relentlessly hammer away until your software runs.'
    )
    parser.add_argument(
        'command',
        nargs=1,
        help='Command that you want to run successfully.'
    )

    brutus = Brutus(parser=parser)
    brutus.run()


if __name__ == "__main__":
    main()
