import argparse
import browser
import sys


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('browser', choices=['firefox', 'chrome', 'servo'],
                        help='name of web browser product')
    parser.add_argument('component', choices=['browser', 'webdriver'],
                        help='name of component')
    parser.add_argument('--channel', choices=['stable', 'beta', 'nightly', 'dev'],
                        default="nightly", help='name of browser release channel')
    parser.add_argument('-d', '--destination',
                        help='filesystem directory to place the component')
    return parser


def run(venv, **kwargs):
    browser = kwargs["browser"]
    destination = kwargs["destination"]
    channel = kwargs["channel"]
    if browser == "chrome" and channel == "nightly":
        # For chrome we don't support nightly
        channel = "dev"
    if browser in ("firefox", 'servo') and channel == "dev":
        # Not sure how to support dev edition
        channel = "nightly"

    if destination is None:
        if venv:
            if kwargs["component"] == "browser":
                destination = venv.path
            else:
                destination = venv.bin_path
        else:
            raise argparse.ArgumentError(None,
                                         "No --destination argument, and no default for the environment")

    install(browser, kwargs["component"], destination, channel)


def install(name, component, destination, channel="nightly"):
    if component == 'webdriver':
        method = 'install_webdriver'
    else:
        method = 'install'

    subclass = getattr(browser, name.title())
    sys.stdout.write('Now installing %s %s...\n' % (name, component))
    kwargs = {"dest": destination}
    if component == "browser":
        kwargs["channel"] = channel
    getattr(subclass(), method)(**kwargs)
