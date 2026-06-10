# ⚡ ZAYROS - Lua Script Shield

## Features
- **Owner-Only Access**: Single password gate, no registration system
- **Luraph-Level Obfuscation**: XOR encryption + Base64 + VM-style loader + anti-tamper checksum + junk code injection + anti-debug hooks
- **Script Vault**: Store, edit, enable/disable, delete scripts
- **Loadstring Generator**: Auto-generates `loadstring(game:HttpGet("..."))()`
- **Anti-Leak**: Even if someone reads the protected code, they cannot modify it (checksum verification kills the script)
- **Executor Compatible**: Works with all Roblox Lua executors

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Change owner password (default: ZAYROS_LORD_2026)
# Edit app.py line: OWNER_PASSWORD_HASH = hashlib.sha256("YOUR_PASSWORD".encode()).hexdigest()

# 3. Run server
python app.py

# 4. Open browser
http://localhost:5000
```

## Default Owner Password
```
ZAYROS_LORD_2026
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth` | POST | Owner authentication |
| `/api/scripts` | GET | List all scripts |
| `/api/scripts` | POST | Create & protect new script |
| `/api/scripts/<id>` | PUT | Update script |
| `/api/scripts/<id>` | DELETE | Delete script |
| `/api/scripts/<id>/toggle` | POST | Enable/Disable script |
| `/api/scripts/<id>/raw` | GET | Get raw + protected code |
| `/api/execute/<id>` | GET | Execute protected script |

## Protection Layers
1. **String Encryption**: XOR with dynamic key derived from script ID
2. **Base64 Encoding**: Encrypted payload encoded
3. **VM Loader**: Custom decryption routine embedded in Lua
4. **Anti-Tamper Checksum**: SHA256 verification - script self-destructs if modified
5. **Junk Code Injection**: 50+ dummy functions to confuse decompilers
6. **String Table Obfuscation**: Variable names replaced with base64 lookups
7. **Anti-Debug Hooks**: Garbage collector hook to detect debuggers
