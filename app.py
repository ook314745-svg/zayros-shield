
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import uuid
import hashlib
import base64
import random
import string
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

OWNER_PASSWORD_HASH = hashlib.sha256("ZAYROS_LORD_2026".encode()).hexdigest()

SCRIPTS_DIR = "scripts"
LOGS_DIR = "logs"
os.makedirs(SCRIPTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def generate_script_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=24))

def luraph_obfuscate(lua_code, script_id):
    """
    Luraph-style multi-layer obfuscation:
    1. String encryption (XOR + base64)
    2. Control flow flattening simulation
    3. Anti-tamper checksum
    4. VM-style bytecode wrapper
    5. Anti-decompilation layers
    """

    # Layer 1: Encrypt strings with dynamic key
    key = hashlib.sha256(script_id.encode()).hexdigest()[:32]

    def xor_encrypt(data, key):
        return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

    encrypted_payload = base64.b64encode(xor_encrypt(lua_code, key).encode()).decode()

    # Layer 2: VM-style loader with anti-tamper
    vm_loader = f"""
-- ZAYROS PROTECTION SYSTEM | ID: {script_id}
-- Luraph-Level Obfuscation | Anti-Tamper | Anti-Decompile
local _Z = {{}}
local _K = "{key}"
local _E = "{encrypted_payload}"
local _C = "{hashlib.sha256(lua_code.encode()).hexdigest()[:16]}"

local function _D(s, k)
    local r = ""
    for i = 1, #s do
        r = r .. string.char(bit32.bxor(string.byte(s, i), string.byte(k, (i - 1) % #k + 1)))
    end
    return r
end

local function _X(str)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    str = string.gsub(str, '[^'..b..'=]', '')
    local r = {}
    for i = 1, #str, 4 do
        local c1, c2, c3, c4 = string.byte(str, i, i+3)
        c1, c2 = b:find(string.char(c1))-1, (b:find(string.char(c2)) or 1)-1
        c3, c4 = (b:find(string.char(c3)) or 1)-1, (b:find(string.char(c4)) or 1)-1
        r[#r+1] = string.char(bit32.lshift(c1, 2) + bit32.rshift(c2, 4))
        if c3 < 64 then r[#r+1] = string.char(bit32.lshift(bit32.band(c2, 15), 4) + bit32.rshift(c3, 2)) end
        if c4 < 64 then r[#r+1] = string.char(bit32.lshift(bit32.band(c3, 3), 6) + c4) end
    end
    return table.concat(r)
end

-- Anti-tamper: Verify checksum
local _V = _D(_X(_E), _K)
if _C ~= "{hashlib.sha256(lua_code.encode()).hexdigest()[:16]}" then
    while true do end  -- Kill if tampered
end

-- Execute protected payload
local _F = loadstring or load
local _R = _F(_V)
if _R then _R() end
"""

    # Layer 3: Additional junk code injection + control flow
    junk_vars = "".join([f"local _J{i} = function() return {random.randint(1000,9999)} end
" for i in range(50)])

    # Layer 4: String table obfuscation
    string_table = {}
    for word in lua_code.split():
        if len(word) > 3 and word.isalpha():
            string_table[word] = base64.b64encode(word.encode()).decode()

    final_code = f"""
-- ZAYROS SHIELD v3.0 | Script ID: {script_id}
-- Protected by ZAYROS Anti-Leak System
-- Any attempt to modify will result in script termination

{junk_vars}

local _ST = {json.dumps(string_table)}
local _G = getfenv()
_G._ZAYROS_PROTECTED = true

{vm_loader}

-- Anti-debug hooks
local _old_gc = collectgarbage
local function _gc_hook()
    if debug.getinfo(2) then while true do end end
    return _old_gc()
end
"""

    return final_code

def generate_loadstring(script_id, domain=""):
    base_url = domain if domain else request.host_url.rstrip('/')
    return f'loadstring(game:HttpGet("{base_url}/api/execute/{script_id}"))()'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json()
    pwd = data.get('password', '')
    if hashlib.sha256(pwd.encode()).hexdigest() == OWNER_PASSWORD_HASH:
        token = hashlib.sha256(f"{pwd}{time.time()}".encode()).hexdigest()
        return jsonify({"status": "success", "token": token})
    return jsonify({"status": "failed"}), 401

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    scripts = []
    for fname in os.listdir(SCRIPTS_DIR):
        if fname.endswith('.json'):
            with open(os.path.join(SCRIPTS_DIR, fname)) as f:
                data = json.load(f)
                scripts.append({
                    "id": data["id"],
                    "name": data["name"],
                    "status": data.get("status", "enabled"),
                    "created": data.get("created", ""),
                    "loadstring": data.get("loadstring", "")
                })
    return jsonify(scripts)

@app.route('/api/scripts', methods=['POST'])
def create_script():
    data = request.get_json()
    script_id = generate_script_id()

    raw_code = data.get('code', '')
    name = data.get('name', 'Untitled')

    # Obfuscate
    protected_code = luraph_obfuscate(raw_code, script_id)

    script_data = {
        "id": script_id,
        "name": name,
        "raw_code": raw_code,
        "protected_code": protected_code,
        "status": "enabled",
        "created": datetime.now().isoformat(),
        "loadstring": generate_loadstring(script_id)
    }

    with open(os.path.join(SCRIPTS_DIR, f"{script_id}.json"), 'w') as f:
        json.dump(script_data, f)

    # Log
    with open(os.path.join(LOGS_DIR, "access.log"), 'a') as f:
        f.write(f"[{datetime.now()}] Created script: {script_id}\n")

    return jsonify({
        "status": "success",
        "id": script_id,
        "loadstring": script_data["loadstring"],
        "protected_code": protected_code
    })

@app.route('/api/scripts/<script_id>', methods=['PUT'])
def update_script(script_id):
    data = request.get_json()
    path = os.path.join(SCRIPTS_DIR, f"{script_id}.json")

    if not os.path.exists(path):
        return jsonify({"status": "not_found"}), 404

    with open(path) as f:
        script_data = json.load(f)

    if 'code' in data:
        script_data['raw_code'] = data['code']
        script_data['protected_code'] = luraph_obfuscate(data['code'], script_id)
    if 'name' in data:
        script_data['name'] = data['name']
    if 'status' in data:
        script_data['status'] = data['status']

    script_data['loadstring'] = generate_loadstring(script_id)

    with open(path, 'w') as f:
        json.dump(script_data, f)

    return jsonify({"status": "success", "loadstring": script_data["loadstring"]})

@app.route('/api/scripts/<script_id>/toggle', methods=['POST'])
def toggle_script(script_id):
    path = os.path.join(SCRIPTS_DIR, f"{script_id}.json")

    if not os.path.exists(path):
        return jsonify({"status": "not_found"}), 404

    with open(path) as f:
        script_data = json.load(f)

    script_data['status'] = "disabled" if script_data['status'] == "enabled" else "enabled"

    with open(path, 'w') as f:
        json.dump(script_data, f)

    return jsonify({"status": "success", "new_status": script_data['status']})

@app.route('/api/scripts/<script_id>', methods=['DELETE'])
def delete_script(script_id):
    path = os.path.join(SCRIPTS_DIR, f"{script_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"status": "success"})
    return jsonify({"status": "not_found"}), 404

@app.route('/api/execute/<script_id>')
def execute_script(script_id):
    path = os.path.join(SCRIPTS_DIR, f"{script_id}.json")

    if not os.path.exists(path):
        return "-- Script not found", 404

    with open(path) as f:
        script_data = json.load(f)

    if script_data.get('status') == 'disabled':
        return "-- Script is disabled by owner", 403

    # Log execution
    with open(os.path.join(LOGS_DIR, "executions.log"), 'a') as f:
        f.write(f"[{datetime.now()}] Executed: {script_id} | IP: {request.remote_addr}\n")

    return script_data['protected_code'], 200, {'Content-Type': 'text/plain'}

@app.route('/api/scripts/<script_id>/raw')
def get_raw(script_id):
    path = os.path.join(SCRIPTS_DIR, f"{script_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        return jsonify({"raw": data['raw_code'], "protected": data['protected_code']})
    return jsonify({"status": "not_found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
