# https://gist.github.com/Kronopath/c94c93d8279e3bac19f2
# WeChat aud file converter to wav files
# Dependencies:
#   SILK audio codec decoder (available at https://github.com/gaozehua/SILKCodec)
#   ffmpeg
#
# By Gabriel B. Nunes (gabriel@kronopath.net)
# Adapted from another script by Nicodemo Gawronski (nico@deftlinux.net)
#

import os
import argparse
import subprocess
from datetime import datetime


def is_silk_file(file_path):
    # If the file has a SILK file header, we know it's a SILK file.
    # Otherwise, we assume it's the older AMR file format.
    input_file = open(file_path, 'rb')
    silk_header = str.encode('#!SILK_V3')
    header = input_file.read(len(silk_header))
    input_file.close()
    return header == silk_header


def convert_amr_file(input_dir, input_file_name, output_dir):
    # These files are AMR files without the AMR header, so they can be converted by just adding the
    # AMR file header and then converting from AMR to WAV.

    input_file_path = os.path.join(input_dir, input_file_name)
    input_file = open(input_file_path, 'rb')

    intermediate_file_name = input_file_name.replace(".aud", ".amr")
    intermediate_file_path = os.path.join(output_dir, intermediate_file_name)
    intermediate_file = open(intermediate_file_path, 'wb')

    amr_header = str.encode("#!AMR\n")
    intermediate_file.write(amr_header + input_file.read())

    input_file.close()
    intermediate_file.close()

    output_file_name = input_file_name.replace(".aud", ".wav")
    output_file_path = os.path.join(output_dir, output_file_name)

    black_hole_file = open("black_hole", "w")
    subprocess.call(["ffmpeg", "-i", intermediate_file_path, output_file_path],
                    stdout=black_hole_file,
                    stderr=black_hole_file)
    black_hole_file.close()

    # Delete the junk files
    os.remove("black_hole")
    os.remove(intermediate_file_path)


def convert_silk_file(input_dir, input_file_name: str, decoder_file_path,
                      output_dir):
    # These files are encoded with the SILK codec, originally developed by Skype.
    # They can be converted by stripping out the first byte
    # and then using the SILK decoder.

    assert input_file_name.endswith('.slik') is True

    input_file_path = os.path.join(input_dir, input_file_name)

    intermediate_file_pcm_name = input_file_name.replace(".slik", ".pcm")
    intermediate_file_pcm_path = os.path.join(output_dir,
                                              intermediate_file_pcm_name)
    intermediate_file_pcm = open(intermediate_file_pcm_path, 'wb')

    output_file_name = input_file_name.replace(".slik", ".wav")
    output_file_path = os.path.join(output_dir, output_file_name)

    black_hole_file = open("black_hole", "w")

    # Use the SILK decoder to convert it to PCM
    subprocess.call(
        [decoder_file_path, input_file_path, intermediate_file_pcm],
        stdout=black_hole_file,
        stderr=black_hole_file)

    # And then ffmpeg to convert that to wav
    subprocess.call([
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-i",
        intermediate_file_pcm, output_file_path
    ],
                    stdout=black_hole_file,
                    stderr=black_hole_file)

    black_hole_file.close()
    intermediate_file_pcm.close()

    # Delete the junk files
    os.remove("black_hole")
    os.remove(intermediate_file_pcm)


class Main(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        audio_src = values
        now = datetime.utcnow().strptime('%Y-%m-%d %H.%M.%S')
        converted = now + "_converted"
        os.mkdir(converted)

        try:
            # Decide which one of these are AMR files and
            # which are SILK, and then convert.
            for dirname, dirnames, filenames in os.walk(audio_src):
                for filename in filenames:
                    if filename[0] == '.':
                        continue
                    input_path = os.path.join(dirname, filename)
                    if (is_silk_file(input_path)):
                        convert_silk_file(dirname, filename,
                                          namespace.silk_decoder, converted)
                    else:
                        convert_amr_file(dirname, filename, converted)

            print("Done!")
        except Exception:
            print(
                "Something went wrong converting the audio files.\n"
                "Common problems:\n"
                "You may be missing the dependencies (ffmpeg and/or the SILK codec decoder).\n"
                "The decoder (and its dependencies) must be in the specified path.\n"
                "The SILK codec decoder also can't handle very large file paths.\n"
                "Try a shorter path to your input directory.")


parser = argparse.ArgumentParser(
    description="converter: convert qq .silk files into .wav",
    epilog=
    "This script is an open source tool under the GNU GPLv3 license. Uses content "
    "modified from a tool originally for DEFT 8.")
parser.add_argument("Folder", action=Main, help=".silk files root folder.")
parser.add_argument("-s",
                    "--silk-decoder",
                    nargs="?",
                    default="./decoder",
                    help="Path to the SILK codec decoder program.")

args = parser.parse_args()
# 用 ffmpeg 把 44100 采样率 单声道 16bts pcm 文件转 16000采样率 16bits 位深的单声道pcm文件
# ffmpeg -y -f s16le -ac 1 -ar 44100 -i test44.pcm -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm (获得pcm文件)
# ffmpeg -y -f s16le -ar 24000 -ac 1 -i /data/1.pcm -f wav -ar 16000 -b:a 16 -ac 1 /data/1.wav (获得wav文件)