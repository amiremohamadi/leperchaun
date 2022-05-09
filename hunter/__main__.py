from pipeline import build_pipeline
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pipeline runner')
    parser.add_argument('--config',
                        '-c',
                        action='store',
                        type=str,
                        default='pipeline.json',
                        help='pipeline config file')
    parser.add_argument('--domain',
                        '-d',
                        action='store',
                        type=str,
                        required=True,
                        help='domain to be hunted')
    args = parser.parse_args()

    # to prevent 'finally' from throwing another exception
    pipeline = None
    try:
        pipeline = build_pipeline(args.config, args.domain)
        pipeline.run()
    except KeyboardInterrupt:
        print('bye bye')
    except Exception as err:
        print('error happened: {}'.format(err))
    finally:
        if pipeline:
            pipeline.teardown()
