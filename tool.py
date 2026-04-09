import os, requests, json, time, sys, random
from rich.console import Console
from rich.prompt import Prompt
from pystyle import Colors, Colorate

# --- ТОХИРГОО ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
FIREBASE_URL = "https://kayzen-1ff37-default-rtdb.firebaseio.com/users.json"
ADMIN_KEY = "Telmunn69"
__CHANNEL__ = "BaldanShopChannel"
_CHAT_="BaldanShopChat"

console = Console()

class CPMApiClient:
    def __init__(self): self.auth = None
    def login(self, e, p):
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", params={"api_key": API_KEY}, json={"account_email": e, "account_password": p}).json()
            if res.get('ok') or str(res.get('message', '')).upper() == "SUCCESSFUL":
                self.auth = res.get('data', {}).get('auth') or res.get('auth')
                return 0
            return 1
        except: return 1
    def make_req(self, end, data):
        try:
            res = requests.post(f"{API_BASE_URL}/{end}", params={"api_key": API_KEY}, json=data).json()
            return res.get('ok') or res.get('error') == 0
        except: return False

def load_db():
    try: return requests.get(FIREBASE_URL, timeout=10).json()
    except: return {}

def update_bal(uid, bal):
    url = f"https://kayzen-1ff37-default-rtdb.firebaseio.com/users/{uid}.json"
    requests.patch(url, json={"balance": bal})

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    brand = "Car Parking Multiplayer 1 Tool"
    print(Colorate.Horizontal(Colors.rainbow, brand.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))
    print(Colorate.Horizontal(Colors.rainbow, ' 𝐏𝐋𝐄𝐀𝐒𝐄 𝐋𝐎𝐆𝐎𝐔𝐓 𝐅𝐑𝐎𝐌 𝐂𝐏𝐌 𝐁𝐄𝐅𝐎𝐑𝐄 𝐔𝐒𝐈𝐍𝐆 𝐓𝐇𝐈𝐒 𝐓𝐎𝐎𝐋'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, ' 𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐓𝐇𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐊𝐄𝐘 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐀𝐍𝐃 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐁𝐋𝐎𝐂𝐊𝐄𝐃'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, f' 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL__}' @{__CHAT__}'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

def main():
    while True:
        banner()
        e = Prompt.ask("[?] Account Email")
        p = Prompt.ask("[?] Account Password")
        k = Prompt.ask("[?] Access Key")

        db = load_db()
        user_id, found = None, None
        if k != ADMIN_KEY:
            for uid, d in db.items():
                if str(d.get('key')) == str(k): user_id, found = uid, d; break
        
        if k != ADMIN_KEY and (not found or found.get('is_blocked')):
            banner()
            print(f"Account Email    : {e}\nAccount Password : {p}\nAccess Key       : {k}\n")
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] Trying to Login: TRY AGAIN.\n[!] Note: make sure you filled out the fields !"))
            time.sleep(4); continue

        cpm = CPMApiClient()
        if cpm.login(e, p) != 0:
            banner(); print(f"Account Email: {e}\nAccess Key: {k}\n\n[✘] Trying to Login: TRY AGAIN."); time.sleep(4); continue

        while True:
            banner()
            db = load_db()
            bal = 999999 if k == ADMIN_KEY else int(db.get(user_id, {}).get('balance', 0))
            
            print(f"Account Email    : {e}")
            print(f"Account password : {p}")
            print(f"Balance          : {bal if k!=ADMIN_KEY else 'Unlimited'}")
            print(f"Access key       : {k}")
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            print(Colorate.Horizontal(Colors.rainbow, f"{{01}}: SET RANK".ljust(45) + "20.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{02}}: CHANGE EMAIL".ljust(45) + "15.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{03}}: CHANGE PASSWORD".ljust(45) + "10.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{04}}: REGISTER NEW ACCOUNT".ljust(45) + "1.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{05}}: LOGOUT FROM ACCOUNT"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{06}}: EXIT FROM TOOL"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            ch = Prompt.ask("\n[?] Select")
            if ch in ["5", "05"]: break
            if ch in ["6", "06"]: sys.exit()

            costs = {"01":20500, "1":20500, "02":15500, "2":15500, "03":10000, "3":10000, "04":1000, "4":1000}
            cost = costs.get(ch.zfill(2) if len(ch)==1 else ch, 0)

            if bal >= cost:
                res = False
                if ch in ["1", "01"]: res = cpm.make_req("set_rank", {"account_auth": cpm.auth})
                elif ch in ["2", "02"]: 
                    ne = Prompt.ask("[?] New Email")
                    if cpm.make_req("change_email", {"account_auth": cpm.auth, "new_email": ne}): e = ne; res = True
                elif ch in ["3", "03"]:
                    np = Prompt.ask("[?] New Password")
                    if cpm.make_req("change_password", {"account_auth": cpm.auth, "new_password": np}): p = np; res = True
                elif ch in ["4", "04"]:
                    re, rp = Prompt.ask("[?] Reg Email"), Prompt.ask("[?] Reg Pass")
                    res = requests.post(f"{API_BASE_URL}/account_register", params={"api_key": API_KEY}, json={"account_email":re, "account_password":rp}).json().get('ok')

                if res:
                    if k != ADMIN_KEY: update_bal(user_id, bal-cost)
                    print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL (√)"))
                    if Prompt.ask("[bold][?] Do You want to Exit ?", choices=["y", "n"], default="n") == "y": sys.exit()
                else: print(Colorate.Horizontal(Colors.red_to_white, "FAILED (✘)"))
            else: print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
            time.sleep(2)

if __name__ == "__main__": main()

