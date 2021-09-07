from flask import Blueprint, Flask, request
import os
from .tasks import make_file
bp = Blueprint("all", __name__)
from datetime import datetime
from urllib.parse import unquote_plus
from urllib.request import urlopen
import logging
import glob
from rembg.bg import remove
from PIL import Image
import io



# @bp.route("/")
# def index():
#     return "Hello!"

# @bp.route("/<string:fname>/<string:content>")
# def makefile(fname, content):
#     fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/" + fname)
#     print("fname: "+fpath+" | queued: "+str(datetime.now()))
#     make_file.delay(fpath, content)
#     return f"Find your file @ <code>{fpath}</code>"


@bp.route("/", methods=["GET", "POST"])
def index():
    file_content = ""

    if request.method == "POST":
        if "file" not in request.files:
            return {"error": "missing post form param 'file'"}, 400

        file_content = request.files["file"].read()

    if request.method == "GET":
        url = request.args.get("url", type=str)
        if url is None:
            return {"error": "missing query param 'url'"}, 400

        file_content = urlopen(unquote_plus(url)).read()

    if file_content == "":
        return {"error": "File content is empty"}, 400

    name_timestr = datetime.utcnow().strftime("%Y%m%d_%H%M%S.%f.png")
    logging.info("task: "+name_timestr)
    alpha_matting = "a" in request.values
    af = request.values.get("af", type=int, default=240)
    ab = request.values.get("ab", type=int, default=10)
    ae = request.values.get("ae", type=int, default=10)
    az = request.values.get("az", type=int, default=1000)

    model = request.args.get("model", type=str, default="u2net")
    model_path = os.environ.get(
        "U2NETP_PATH",
        os.path.expanduser(os.path.join("~", ".u2net")),
    )
    model_choices = [os.path.splitext(os.path.basename(x))[0] for x in set(glob.glob(model_path + "/*"))]
    if len(model_choices) == 0:
        model_choices = ["u2net", "u2netp", "u2net_human_seg"]

    if model not in model_choices:
        return {"error": f"invalid query param 'model'. Available options are {model_choices}"}, 400

    try:
        fpath = store_tmp(file_content, name_timestr)
        remove.delay(fpath,
                model,
                alpha_matting,
                af,
                ab,
                ae,
                az,
                name_timestr
                )
        return {"success": "Success!", "filename": name_timestr}, 200
    except Exception as e:
        logging.exception(e, exc_info=True)
        return {"error": "oops, something went wrong!"}, 500


def store_tmp(byte, name):
    fpath = "/Users/user/Developments/rembg/images/"+name
    f = Image.open(io.BytesIO(byte))
    f.save(fpath, "PNG")
    return fpath
