import os
import requests
import shutil
import time
import re


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_canvas_files(api_key, domain, course_ids, output_dir):
    headers = {'Authorization': 'Bearer ' + api_key}

    for course_id in course_ids:
        print(f"Processing course {course_id}...")

        # Get the modules in the course
        r = requests.get(f"https://{domain}/api/v1/courses/{course_id}/modules", headers=headers, params={'include': ['items']})
        r.raise_for_status()
        modules = r.json()
        print(modules)

        # Create a directory for this course
        course_dir = os.path.join(output_dir, str(course_id))
        os.makedirs(course_dir, exist_ok=True)

        for module in modules:
            for item in module.get('items', []):
                if(item.get('url', None) != None):
                    if('files' in item.get('url', None)):
                    # print("THERHEHJRERJKEJRKKRJKEJ")
                    # print(item)
                    # print(item.get('url', None))
                    # if True: #item['type'] == 'File':
                        # Get information about the file
                        # r = requests.get(f"https://{domain}/api/v1/files/{item['content_id']}", headers=headers)
                        r = requests.get(item.get('url', None), headers=headers)
                        r.raise_for_status()
                        file_info = r.json()

                        # print(file_info)

                        # Download the file
                        print(f"Downloading file {file_info['display_name']}...")
                        r = requests.get(file_info['url'], stream=True)
                        r.raise_for_status()
                        sanitized_filename = sanitize_filename(file_info['display_name'])
                        with open(os.path.join(course_dir, sanitized_filename), 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    
                    # Pause execution to respect rate limit
                    time.sleep(1)

    print("Done.")

# Usage:


api_key = ''
domain = 'caltech.instructure.com'
# course_ids = ['3821','3395','3849','4290','2802','4607','2401','2498','4650','3471','4409', '4595','5212', '1055', '2517','2870', '1059','2513','2875', '3183','2910','4129','3434','3810','4241','3329','3729','5337','4779','3448','3780','4264','983']
course_ids = ['5452']
output_dir = 'output/'
# download_files_from_courses(api_key, domain, course_ids, output_dir)
download_canvas_files(api_key, domain, course_ids, output_dir)