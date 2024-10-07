from extract import extract, request
from transform import transform, formatDT
from load import load

from time import time, sleep
from datetime import datetime
import subprocess
from os import environ

environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

def main():
    print(f'\nStrating data-pipeline: {datetime.now().strftime(formatDT)}')
    print('----------------------------------------\n')

    t0 = time()
    extract_data = extract()
    t1 = time()
    print(f'\nStep 1: Extract done ({str(t1-t0)} seconds)')
    print('----------------------------------------\n')

    t0 = time()
    transform_data = transform(extract_data)
    t1 = time()
    print(f'\nStep 2: Transform done ({str(t1-t0)} seconds)')
    print('----------------------------------------\n')

    t0 = time()
    _ = load(transform_data)
    t1 = time()
    print(f'\nStep 3: Load done ({str(t1-t0)} seconds)')
    print('----------------------------------------\n')

if __name__ == '__main__':
    try:
        request('tracks') # ping the API to see if it is online
        
    except:
        # the API is not online: reload it
        subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--reload"], cwd="src/moovitamix_fastapi") 
        timeout = time() + 60*5 # 5 minutes from now

        while True:
            if time() > timeout:
                raise Exception('API connexion timeout')

            try:
                sleep(1)
                request('tracks') # ping the API to see if it is online
            
            except:
                print('API not yet online. Retrying...')
                continue
            
            else:
                main() # execute the ETL data pipeline
                break

    else:
        main() # execute the ETL data pipeline