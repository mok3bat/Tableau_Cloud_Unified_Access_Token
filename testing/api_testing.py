"""API testing functions for JWT tokens."""

import requests
import jwt as pyjwt


def test_tcm_connection(cm_jwt_login_url, results):
    """Test connection to Tableau Cloud Manager API."""
    jwt_token = results.get("jwt", {}).get("token", "")
    if not jwt_token: 
        return "❌ Please run the workflow first."
    try:
        r = requests.post(cm_jwt_login_url, json={"token": jwt_token})
        return "✅ TCM API connection successful!" if r.status_code == 200 else f"❌ Failed: {r.status_code} - {r.text}"
    except Exception as e: 
        return f"❌ Error: {str(e)}"


def test_tableau_connection(tc_pod_url, results):
    """Test connection to Tableau Cloud REST API."""
    if results["tableau_login"]["status"] ==  "skipped":
        return "🌐 No sites configured"

    jwt_token = results.get("jwt", {}).get("token", "")
    if not jwt_token: 
        return "❌ Please run the workflow first."
    
    # Get site_id from the JWT scopes or use the first configured site
    scopes = results.get("jwt", {}).get("scopes", [])
    site_id = "default"
    
    # Try to extract site_id from the workflow results
    if "debug_info" in results and "request_body_sent" in results["debug_info"]:
        site_id = results["debug_info"]["request_body_sent"]["credentials"]["site"]["contentUrl"]
    
    try:
        url = f"{tc_pod_url}/api/3.27/auth/signin"
        body = {"credentials": {"jwt": jwt_token, "isUat": True, "site": {"contentUrl": site_id}}}
        r = requests.post(url, json=body)
        return "✅ Tableau REST API connection successful!" if r.status_code == 200 else f"❌ Failed: {r.status_code} - {r.text}"
    except Exception as e: 
        return f"❌ Error: {str(e)}"


def list_uat_configurations(cm_pat_secret, cm_pat_login_url, cm_uat_configs_url):
    """List all UAT configurations from Cloud Manager."""
    if not cm_pat_secret or not cm_pat_login_url or not cm_uat_configs_url:
        return {"error": "Please configure Cloud Manager settings first"}, ""
    
    try:
        # Step 1: Login with PAT to get session token
        login_response = requests.post(
            cm_pat_login_url,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json={"token": cm_pat_secret}
        )
        
        if login_response.status_code != 200:
            return {
                "error": f"Failed to login to Cloud Manager: {login_response.status_code}",
                "details": login_response.text
            }, "", []
        
        session_token = login_response.json().get('sessionToken')
        if not session_token:
            return {"error": "No session token received from Cloud Manager"}, ""
        
        # Step 2: Get UAT configurations
        configs_response = requests.get(
            cm_uat_configs_url,
            headers={
                'Accept': 'application/json',
                'x-tableau-session-token': session_token
            }
        )
        
        # Generate cURL command for display
        curl_cmd = f"""curl --location '{cm_uat_configs_url}' \\
--header 'Accept: application/json' \\
--header 'x-tableau-session-token: {session_token[:20]}...'"""
        
        if configs_response.status_code == 200:
                    configs_data = configs_response.json()
                    
                    # Extract config IDs for radio button choices
                    config_ids = []
                    if isinstance(configs_data, list):
                        for config in configs_data:
                            # Handle nested structure: config might have 'id' as an object with 'configId'
                            if isinstance(config.get('id'), dict):
                                config_id = config['id'].get('configId', '')
                            else:
                                config_id = config.get('configId', config.get('id', ''))
                            
                            if config_id:
                                config_ids.append(config_id)
                        
                        result = {
                            "total_configurations": len(configs_data),
                            "configurations": configs_data
                        }
                    else:
                        result = configs_data
                    
                    return result, curl_cmd, config_ids
        else:
            return {
                "error": f"Failed to retrieve configurations: {configs_response.status_code}",
                "details": configs_response.text
            }, curl_cmd, []
            
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}, "", []


def revoke_uat_configuration(config_id, cm_pat_secret, cm_pat_login_url, cm_uat_configs_url):
    """Revoke a specific UAT configuration"""
    if not config_id:
        return {"error": "Please select a configuration to revoke"}, ""
    
    if not cm_pat_secret or not cm_pat_login_url or not cm_uat_configs_url:
        return {"error": "Please configure Cloud Manager settings first"}, ""
    
    try:
        # Step 1: Login with PAT to get session token
        login_response = requests.post(
            cm_pat_login_url,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json={"token": cm_pat_secret}
        )
        
        if login_response.status_code != 200:
            return {
                "error": f"Failed to login to Cloud Manager: {login_response.status_code}",
                "details": login_response.text
            }, ""
        
        session_token = login_response.json().get('sessionToken')
        if not session_token:
            return {"error": "No session token received from Cloud Manager"}, ""
        
        # Step 2: Delete UAT configuration
        delete_url = f"{cm_uat_configs_url}/{config_id}"
        delete_response = requests.delete(
            delete_url,
            headers={
                'Accept': 'application/json',
                'x-tableau-session-token': session_token
            }
        )
        
        # Generate cURL command for display
        curl_cmd = f"""curl --location --request DELETE '{delete_url}' \\
--header 'Accept: application/json' \\
--header 'x-tableau-session-token: {session_token[:20]}...'"""
        
        if delete_response.status_code in [200, 204]:
            return {
                "success": True,
                "message": f"Configuration '{config_id}' successfully revoked",
                "status_code": delete_response.status_code
            }, curl_cmd
        else:
            return {
                "error": f"Failed to revoke configuration: {delete_response.status_code}",
                "details": delete_response.text
            }, curl_cmd
            
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}, ""

def update_curl_commands(results):
    """Update cURL commands for display."""
    tcm_cmd, tc_cmd = "Run the workflow first to generate the cURL command", "Run the workflow first to generate the cURL command"
    if results and "curl_commands" in results:
        if "tcm" in results["curl_commands"]:
            if  results["tcm_login"]["status"] ==  "success":
                tcm_cmd = results["curl_commands"]["tcm"]
            else:
                tcm_cmd = "Fix the workflow errors first to generate the cURL command"
        if "tableau" in results["curl_commands"]:
            if results["tableau_login"]["status"] ==  "success":
                tc_cmd = results["curl_commands"]["tableau"]
            else:
                tc_cmd = "Fix the workflow errors first to generate the cURL command"
    return tcm_cmd, tc_cmd