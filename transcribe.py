import argparse
import os
import utilss
import json

# audio_file='D:\\audio_path\\resources_sample1_2_people_conversation_sample_1.mp3'
# '2b8629f5c4374a5db94a4fbb0d2e4b37'2b8629f5c4374a5db94a4fbb0d2e4b37

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file', help='url to file or local audio filename')
    parser.add_argument('--local', action='store_true', help='must be set if audio_file is a local filename')
    parser.add_argument('--api_key', action='store', help='<YOUR-API-KEY>')

    args = parser.parse_args()

    if args.api_key is None:
        args.api_key = os.getenv("AAI_API_KEY")
        if args.api_key is None:
            raise RuntimeError("AAI_API_KEY environment variable not set. Try setting it now, or passing in your "
                               "API key as a command line argument with `--api_key`.")

    # Create header with authorization along with content-type
    header = {
        'authorization': args.api_key,
        'content-type': 'application/json'
    }

    if args.local:
        # Upload the audio file to AssemblyAI
        upload_url = utilss.upload_file(args.audio_file, header)
    else:
        upload_url = {'upload_url': args.audio_file}

    # Request a transcription
    transcript_response = utilss.request_transcript(upload_url, header)

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utilss.make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    utilss.wait_for_completion(polling_endpoint, header)

    # Request the paragraphs of the transcript
    paragraphs= utilss.get_paragraphs(polling_endpoint, header)

    # Save and print transcript
    # with open('transcript.txt', 'w') as f:
    #     for para in paragraphs:
    #         print(para['words'] + '\n')
    #         f.write(para['words'] + '\n' )

    with open('transcript.json', 'w') as f:
        # speaker_diarization=[]
        for para in paragraphs:
            # print(para)
            # speaker_diarization.append(para)
            json.dump(para,f)

    return


if __name__ == '__main__':
    main()
