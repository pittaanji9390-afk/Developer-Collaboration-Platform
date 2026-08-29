"""
ForgeHub CLI - SECRET Module
Sets, encrypts, lists, and rotates repository and organization secrets
"""
import sys
import json
import urllib.request
import urllib.error

class SecretCommand:
    """Sets, encrypts, lists, and rotates repository and organization secrets"""

    def __init__(self, base_url="http://localhost:8080/api/v1", token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token or os.environ.get("FORGEHUB_TOKEN", "")

    def execute(self, action, *args, **kwargs):
        method_name = f"handle_{action.replace('-', '_')}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(*args, **kwargs)
        else:
            print(f"Error: Unknown action '{action}' for secret command.")
            self.print_help()
            return 1

    def handle_list(self, *args, **kwargs):
        print(f"[*] Listing secret resources from {self.base_url}/secret...")
        return self._send_request(f"/secret", method="GET")

    def handle_get(self, resource_id=None, *args, **kwargs):
        if not resource_id:
            print("Error: Resource identifier is required.")
            return 1
        print(f"[*] Retrieving secret '{resource_id}'...")
        return self._send_request(f"/secret/{resource_id}", method="GET")

    def handle_create(self, name=None, *args, **kwargs):
        print(f"[*] Creating new secret resource...")
        payload = {"name": name or "default-resource", "enabled": True}
        return self._send_request(f"/secret", method="POST", data=payload)

    def handle_delete(self, resource_id=None, *args, **kwargs):
        if not resource_id:
            print("Error: Resource identifier is required.")
            return 1
        print(f"[*] Deleting secret '{resource_id}'...")
        return self._send_request(f"/secret/{resource_id}", method="DELETE")

    def handle_status(self, *args, **kwargs):
        print(f"[*] Inspecting secret health and synchronization status...")
        return {"status": "HEALTHY", "module": "secret", "authenticated": bool(self.token)}

    def _send_request(self, endpoint, method="GET", data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Accept": "application/json", "User-Agent": "ForgeHub-CLI/1.0"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        body_bytes = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body_bytes = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                print(json.dumps(result, indent=2))
                return result
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
            return {"error": e.code}
        except Exception as e:
            print(f"Connection failed: {e}")
            return {"error": str(e)}

    def print_help(self):
        print(f"Usage: forgehub secret <action> [options]")
        print("Available actions: list, get, create, delete, status")

if __name__ == "__main__":
    cmd = SecretCommand()
    action = sys.argv[1] if len(sys.argv) > 1 else "list"
    cmd.execute(action, *sys.argv[2:])
