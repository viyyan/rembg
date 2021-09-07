import logging
from app import factory
import os
import app
import argparse


def main():
    ap = argparse.ArgumentParser()
    log = "/usr/develop/rembg/log/rembg-server.log"
    # log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../log/rembg-server.log")
    logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    ap.add_argument(
        "-a",
        "--addr",
        default="0.0.0.0",
        type=str,
        help="The IP address to bind to.",
    )

    ap.add_argument(
        "-p",
        "--port",
        default=5000,
        type=int,
        help="The port to bind to.",
    )
    args = ap.parse_args()
    app.host = args.addr
    app.port = args.port
    appl = factory.create_app(celery=app.celery)
    appl.run()
    # serve(app, host=args.addr, port=args.port, threads=4)


if __name__ == "__main__":
    main()
