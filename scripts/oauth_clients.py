#!/usr/bin/env python2.7
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

    if stdin_json.get("tfe_token"):
        tfe_token = stdin_json.get("tfe_token")
    else:
        tfe_token = env_atlas_token()
    
    if not tfe_token:
        raise Exception("Must specify tfe_token either as ATLAS_TOKEN environment variable or by passing tfe_org as module input")
    

    if stdin_json.get('tfe_org'):
        tfe_org = stdin_json.get('tfe_org')
    else:
        tfe_org = env_tfe_org()
    
    if not tfe_org:
        raise Exception("Must specify tfe_org either as TFE_ORG environment variable or by passing tfe_org as module input")
    
    
    vcs_config = stdin_json.get('vcs_config')

    headers = {"Authorization": "Bearer {0}".format(tfe_token),
               'Content-Type': 'application/vnd.api+json'}

    vcs_config = json.loads(vcs_config)
    url = "https://{0}/api/v2/organizations/{1}/oauth-clients".format(tfe_api, tfe_org)

    try:
        
        resp = requests.post(url,
                        data=json.dumps(vcs_config),
                        headers=headers)

        data = resp.json()
        oauth_token = str(data.get('data').get('relationships').get('oauth-tokens').get('data')[0].get('id'))
        with open("/tmp/oauth_tokens.json", "a") as output:
            output.write(json.dumps(dict(oauth_token=oauth_token),
                            separators=(',', ':'),
                            indent=4,
                            sort_keys=True)
                        )
        print json.dumps(dict(oauth_token=oauth_token), 
                            separators=(',', ':'), 
                            indent=4, 
                            sort_keys=True)
        
    except Exception, e:
        vcs_config["headers"] = headers
        vcs_config["url"] =url
        vcs_config["token"] = tfe_token
        vcs_config["org"] = tfe_org
        vcs_config["return_data"] = data
        sys.stderr.write(json.dumps(vcs_config, 
                                    separators=(',', ':'), 
                                    indent=4, 
                                    sort_keys=True))
        sys.stderr.write(str(e))
        sys.exit(1)

    

if __name__ == '__main__':
    main()
