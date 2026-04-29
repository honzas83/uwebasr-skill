#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import argparse
import logging
from pprint import pprint
import requests
import subprocess
from queue import Queue
import threading
import time
import json

UWEBASR_URL = "https://uwebasr.zcu.cz"
N_TRIES = 5

SPEECHCLOUD_JSON = "speechcloud_json"
FORMATS = {
    "json": SPEECHCLOUD_JSON, # special handling in format saving
    "txt": "plaintext",
    "s.txt": "plaintext&sp=0.3&pau=2.0",
    "vtt": "webvtt",
    "s.vtt": "sentvtt&sp=0.3&pau=2.0",
    "jsonl": "json",
}

parser = argparse.ArgumentParser(description='UWebASR client library')
parser.add_argument('model', metavar='MODEL', type=str, help='SpeechCloud app_id')
parser.add_argument('fns', metavar='FN', type=str, nargs="+", help='Input files')
parser.add_argument('--uwebasr-url', metavar='URL', type=str, default=UWEBASR_URL, help=f'UWEBASR_URL (default {UWEBASR_URL})')
parser.add_argument('--no-ffmpeg', action="store_true", help="Do not use ffmpeg, submit input files directly")
parser.add_argument('--no-cookies', action="store_true", help="Do not use cookies")
parser.add_argument('--overwrite', action="store_true", help="Allow overwrite of output files")
parser.add_argument('--output-dir', type=str, help="Optional output directory for saving output files")
parser.add_argument('--suffix', type=str, help="Optional suffix inserted after basename and before output file extension")
parser.add_argument('--n-workers', type=int, default=1, help="Number of parallel workers. Defaults to 1.")
parser.add_argument('--format', type=str, action="append", help="Generate only this format (can be used many times). Defaults to all formats.")

logger = logging.getLogger('uwebasr')


def get_model_url(model, uwebasr_url=None):
    if uwebasr_url is None:
        uwebasr_url = UWEBASR_URL

    return uwebasr_url+"/api/v2/"+model

def get_convert_url(uwebasr_url=None):
    if uwebasr_url is None:
        uwebasr_url = UWEBASR_URL

    return uwebasr_url+"/utils/v2/convert-speechcloud-json"

def recognize(model_url, fn, cookies=None, no_ffmpeg=False):
    if no_ffmpeg:
        fr = open(fn, "rb")
    else:
        command = ["ffmpeg", "-xerror", "-hide_banner", "-loglevel", "error", "-i", fn, "-ar", "16000", "-ac", "1", "-vn", "-c:a", "libvorbis", "-q:a", "10", "-f", "ogg", "-"]
        ffmpeg = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
        fr = ffmpeg.stdout

    r = requests.post(model_url+"?format=speechcloud_json", data=fr, cookies=cookies)
    fr.close()

    r.raise_for_status()
    logger.info("Used SpeechCloud-SessionID: %s", r.headers.get("SpeechCloud-SessionID"))

    data_json = r.json()
    cookie_jar = r.cookies
    if cookies is not None:
        return data_json, cookie_jar
    else:
        return data_json


def convert(convert_url, data_json, format):
    r = requests.post(convert_url+"?format="+format, json=data_json)
    r.raise_for_status()

    return r.text


def _process_queue(model_url, convert_url, queue, cmdline_args):
    cookie_jar = requests.cookies.RequestsCookieJar()

    while True:
        fn = queue.get()

        try:
            logger.info("Recognizing file: %s", fn)

            retry_count = 0
            while True:
                try:
                    if args.no_cookies:
                        data_json = recognize(model_url, fn, no_ffmpeg=cmdline_args.no_ffmpeg)
                    else:
                        data_json, cookie_jar = recognize(model_url, fn, cookies=cookie_jar, no_ffmpeg=cmdline_args.no_ffmpeg)

                    # Break the cycle
                    break
                except requests.HTTPError as e:
                    if e.response.status_code == 503:
                        retry_count += 1
                        if retry_count == N_TRIES:
                            raise
                        else:
                            time.sleep(1)
                            logger.info("    Trying again: %s", fn)
                            continue
                    else:
                        raise

            base_fn = os.path.splitext(fn)[0]

            for ext, format in FORMATS.items():
                if cmdline_args.format and ext not in cmdline_args.format:
                    # This format is not requested to be generated
                    continue

                if cmdline_args.output_dir:
                    # Replace the output directory
                    base_fn = os.path.join(cmdline_args.output_dir, os.path.basename(base_fn))

                if not cmdline_args.suffix:
                    out_fn = base_fn+"."+ext
                else:
                    # Insert the suffix before file extension
                    out_fn = base_fn+"."+cmdline_args.suffix+"."+ext

                if os.path.exists(out_fn) and not cmdline_args.overwrite:
                    logger.error("File already exists: %s, terminating... (use --overwrite to force file overwrite)", out_fn)
                    os._exit(-1)

                logger.info("Writing file %s (format %s)", out_fn, format)
                with open(out_fn, "w", encoding="utf-8") as fw:
                    if format == SPEECHCLOUD_JSON:
                        output = json.dumps(data_json, indent=4)
                    else:
                        output = convert(convert_url, data_json, format) 

                    fw.write(output)
        except:
            logger.exception("Error while processing file: %s", fn)
        else:
            logger.info("Successfully recognized file: %s", fn)

        queue.task_done()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)

    args = parser.parse_args()

    args.uwebasr_url = args.uwebasr_url.rstrip("/")

    model_url = get_model_url(args.model, args.uwebasr_url)
    convert_url = get_convert_url(args.uwebasr_url)

    logger.info("Using model: %s", model_url)

    file_queue = Queue()

    for idx in range(args.n_workers):
        threading.Thread(target=_process_queue, daemon=True, args=(model_url, convert_url, file_queue, args)).start()

    for fn in args.fns:
        file_queue.put(fn)

    logger.info("Waiting for processing of all files")
    file_queue.join()
    logger.info("All file processed")
