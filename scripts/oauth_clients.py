#!/usr/local/bin/python
import requests
import os
import json
import sys
import hcl

def sanitize_path(config):
    path = os.path.expanduser(config)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path


def env_tfe_org():
    return os.environ.get("TFE_ORG")

def env_atlas_token():
    return os.environ.get("ATLAS_TOKEN")

def main():
    stdin_json = json.loads(sys.stdin.read())
    tfe_api = stdin_json.get("tfe_api")

    if not env_atlas_token():
        tfe_token = stdin_json.get("tfe_token")
    else:
        tfe_token = env_atlas_token()

    if not env_tfe_org():
        tfe_org = stdin_json.get('tfe_org')
    else:
        tfe_org = env_tfe_org()
    
    vcs_config = stdin_json.get('vcs_config')

    headers = {"Authorization": "Bearer {0}".format(tfe_token),
               'Content-Type': 'application/vnd.api+json'}

    vcs_config = json.loads(vcs_config)

    try:
        resp = requests.post("https://{0}/api/v2/organizations/{1}/oauth-clients".format(tfe_api, tfe_org),
                        data=json.dumps(vcs_config),
                        headers=headers)

        resp.raise_for_status()
        data = resp.json()
        oauth_token = data.get('data').get('relationships').get('oauth-tokens').get('data')[0].get('id')
        print json.dumps(dict(oauth_token=oauth_token, 
                            separators=(',', ':'), 
                            indent=4, 
                            sort_keys=True))
    except Exception, e:
        sys.stderr.write(json.dumps(vcs_config, 
                                    separators=(',', ':'), 
                                    indent=4, 
                                    sort_keys=True))
        sys.stderr.write(str(e))
        sys.exit(1)

    

if __name__ == '__main__':
    main()
