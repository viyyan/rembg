import logging
from app import factory
import os
import app


def main():
    log = "/usr/develop/rembg/log/rembg-server.log"
    # log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../log/rembg-server.log")
    logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    appl = factory.create_app(celery=app.celery)
    appl.run()
    # serve(app, host=args.addr, port=args.port, threads=4)


if __name__ == "__main__":
    main()
