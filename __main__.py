import click


class Screener:
    def __init__(self, config_name):
        print(config_name)


@click.command()
@click.option('--config', '-c', prompt='You must input config', help='config for screener subclass of base config')
def run(config):
    Screener(config)


if __name__ == '__main__':
    run()
