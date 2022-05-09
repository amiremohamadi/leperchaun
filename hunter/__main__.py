from pipeline import build_pipeline
from template import module_generate
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pipeline runner')
    parser.add_argument('--config',
                        '-c',
                        action='store',
                        type=str,
                        default='pipeline.json',
                        help='pipeline config file')
    required = parser.add_mutually_exclusive_group(required=True)
    required.add_argument('--domain',
                          '-d',
                          action='store',
                          type=str,
                          help='domain to be hunted')
    required.add_argument('--new-module',
                          '-n',
                          action='store',
                          type=str,
                          help='create new leperchaun module')
    args = parser.parse_args()

    # to prevent 'finally' from throwing another exception
    pipeline = None
    try:
        if args.domain:
            pipeline = build_pipeline(args.config, args.domain)
            pipeline.run()
        elif args.new_module:
            module_generate(args.new_module)
    except KeyboardInterrupt:
        print('bye bye')
    except Exception as err:
        print('error happened: {}'.format(err))
    finally:
        if pipeline:
            pipeline.teardown()
