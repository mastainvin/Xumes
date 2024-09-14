
def main():
    import sys
    import os

    sys.path.insert(0, os.getcwd())
    from xumes.core.xumes_cli import cli
    cli()


if __name__ == '__main__':
    main()
