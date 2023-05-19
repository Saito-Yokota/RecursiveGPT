import openai
import os
from tqdm import tqdm
import sys


def process_chunk(prompt, chunk, output_path):
    with open(output_path, 'a') as output_file:
        messages = [{'role': 'system', 'content': 'I am a helpful assistant.'},
                {'role': 'user', 'content': (prompt + ' '.join(chunk))}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages)
        response = response['choices'][0]['message']['content']
        output_file.write(response + '\n\n')

def split_file_to_chunks(file_path, chunk_size):
    with open(file_path, 'r') as file:
        content = file.read()
        words = content.split()

        num_chunks = round(len(words)/chunk_size)
        cost_per_token = 0.0002/1000
        est_cost = len(words)/0.75*cost_per_token

        print(f'Estimated prompts required: {num_chunks:.1f} prompts ({chunk_size} words each)')
        print(f'Estimated cost: between ${est_cost:.2f}-${est_cost*2:.2f}')
        print(f'Press RETURN to continue or exit (Ctrl+Z) to cancel.')
        input()

        print(f'Writing full output to file {output_path}...')

        for i in tqdm(range(0, len(words), chunk_size)):
            chunk = words[i:i+chunk_size]
            process_chunk(prompt, chunk, output_path)


if __name__ == '__main__':
    api_key = input('Enter your OpenAI API key: ')
    openai.api_key = api_key
    # TODO: add checks for key validity

    input_path = input('Enter the input path to the text file to process: ')
    if os.path.exists(input_path) == False:
        print(f'`{input_path}` can\'t be found.')
        exit()

    prompt = input('Enter the prompt to be prepended to each chunk of text: ')
    if prompt == '':
        print('A prompt is required to use this script.')
        exit()

    output_path = input('Enter the output path to the text file to write to (default: output.txt): ')
    if output_path == '':
        output_path = 'output.txt'
        
    chunk_size = int(input('Enter the number of words per prompt (default: 2500): '))
    if chunk_size == '':
        chunk_size = 2500
    elif chunk_size < 1:
        print('Chunk size must be greater than 0.')
        exit()
    elif chunk_size > 3000:
        print('Chunk sizes greater than ~3000 are likely to fail due to model limitations. Continue? (y/n)')
        if input() != 'y':
            exit()
        
    split_file_to_chunks(prompt, input_path, output_path, chunk_size)