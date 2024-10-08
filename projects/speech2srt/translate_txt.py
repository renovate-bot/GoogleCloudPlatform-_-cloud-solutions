# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ruff: noqa

"""Translates text file using Google Cloud Translation API.

Target language(s) can be specified with language code.
If multiple languages are provided, separate files will be created
for each target language.
"""

import argparse
from time import sleep
from google.cloud import translate_v3 as translate


def get_supported_languages(project_id):
    """Getting a list of supported language codes"""

    client = translate.TranslationServiceClient()
    parent = client.location_path(project_id, "global")
    response = client.get_supported_languages(parent=parent)

    # List language codes of supported languages
    print("Supported Languages: ", end="")
    for language in response.languages:
        print("{} ".format(language.language_code), end="")
    print("\n")


def batch_translate_text(input_uri, output_uri, project_id,
                         location, source_lang, target_lang, glossary_id=None):
    # call batch translate against orig.txt

    client = translate.TranslationServiceClient()

    target_language_codes = target_lang.split(",")
    gcs_source = {"input_uri": input_uri}
    mime_type = "text/plain"
    input_configs_element = {"gcs_source": gcs_source, "mime_type": mime_type}
    input_configs = [input_configs_element]
    gcs_destination = {"output_uri_prefix": output_uri}
    output_config = {"gcs_destination": gcs_destination}
    parent = f"projects/{project_id}/locations/{location}"

    # Add glossary_config if glossary_id is provided
    if glossary_id:
        print(f"Using glossary: {glossary_id}")
        glossary_resource_name = client.glossary_path(project_id, location,
                                                      glossary_id)

        # Create TranslateTextGlossaryConfig using the glossary resource name
        translate_text_glossary_config = translate.TranslateTextGlossaryConfig(
            glossary=glossary_resource_name,
        )
        # Modify the request to include translate_text_glossary_config
        operation = client.batch_translate_text(
            request={
                "parent": parent,
                "source_language_code": source_lang,
                "target_language_codes": target_language_codes,
                "input_configs": input_configs,
                "output_config": output_config,
                "glossaries": {target_lang: translate_text_glossary_config}
            }
        )
    else:
        operation = client.batch_translate_text(
            request={
                "parent": parent,
                "source_language_code": source_lang,
                "target_language_codes": target_language_codes,
                "input_configs": input_configs,
                "output_config": output_config,
            })

    # Initial delay
    total_wait_secs = 90
    print(f"Waiting for operation to complete... {total_wait_secs:.0f} secs")

    delay_secs = 10
    sleep(90)
    while not operation.done():
        # Exponential backoff
        delay_secs *= 1.1
        total_wait_secs += delay_secs
        print(f"Checking in: {delay_secs:.0f}s | total: {total_wait_secs:.0f}s")
        sleep(delay_secs)

    response = operation.result()
    print("Total Characters: {}".format(response.total_characters))
    print("Translated Characters: {}".format(response.translated_characters))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_id",
        type=str,
        required=True
    )
    parser.add_argument(
        "--location",
        type=str,
        default="us-central1"
    )
    parser.add_argument(
        "--source_lang",
        type=str,
        default="en",
    )
    parser.add_argument(
        "--target_lang",
        type=str,
        default="ko,fi",
    )
    parser.add_argument(
        "--input_uri",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output_uri",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--glossary_id",
        type=str,
        help="ID of the glossary to use for translation"
    )
    args = parser.parse_args()

    batch_translate_text(args.input_uri, args.output_uri, args.project_id,
                         args.location, args.source_lang, args.target_lang,
                         args.glossary_id)


if __name__ == "__main__":
    main()
