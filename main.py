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
__CHAT__ = "BaldanShopChat"

console = Console()

class CPMApiClient:
    def __init__(self): self.auth = None
    
    def login(self, e, p):
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", params={"api_key": API_KEY}, json={"account_email": e, "account_password": p}).json()
            msg = str(res.get('message', '')).upper()
            if res.get('ok') or msg == "SUCCESSFUL":
                self.auth = res.get('data', {}).get('auth') or res.get('auth')
                return 0, "SUCCESSFUL"
            return 1, res.get('message', 'Login Failed')
        except: return 1, "Connection Error"

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
    print(Colorate.Horizontal(Colors.rainbow, f' 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @{__CHANNEL__} Or @{__CHAT__}'.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, '='*60))

def main():
    while True:
        banner()
        e = Prompt.ask("[bold white][?] Account Email[/bold white]")
        p = Prompt.ask("[bold white][?] Account Password[/bold white]")
        k = Prompt.ask("[bold white][?] Access Key[/bold white]")

        db = load_db()
        user_id_ref, found_user = None, None
        is_unlimited = (k == ADMIN_KEY)

        if not is_unlimited:
            for uid, data in db.items():
                if str(data.get('key')) == str(k):
                    user_id_ref, found_user = uid, data
                    break

        # Блок болон Key шалгалт
        if not is_unlimited and (not found_user or found_user.get('is_blocked')):
            banner()
            print(f"Account Email    : {e}\nAccount Password : {p}\nAccess Key       : {k}\n")
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] Trying to Login: TRY AGAIN."))
            print(Colorate.Horizontal(Colors.red_to_white, "[!] Note: make sure you filled out the fields !"))
            time.sleep(4); continue

        # CPM Login
        cpm = CPMApiClient()
        l_status, l_msg = cpm.login(e, p)
        if l_status != 0:
            banner()
            print(f"Account Email    : {e}\nAccess Key       : {k}\n")
            print(Colorate.Horizontal(Colors.red_to_white, f"[✘] Trying to Login: TRY AGAIN."))
            print(Colorate.Horizontal(Colors.red_to_white, f"[!] Note: {l_msg}"))
            time.sleep(4); continue

        print(Colorate.Horizontal(Colors.green_to_white, "[√] Trying to Login: SUCCESSFUL.")); time.sleep(1)

        while True:
            banner()
            # Баланс шинэчлэх
            db = load_db()
            if not is_unlimited: found_user = db.get(user_id_ref, {})
            current_bal = 999999 if is_unlimited else int(found_user.get('balance', 0))
            bal_display = "Unlimited" if is_unlimited else f"{current_bal:,}"

            print(f"Account Email    : {e}")
            print(f"Account password : {p}")
            print(f"Balance          : {bal_display}")
            print(f"Access key       : {k}")
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            # Цэсийг тэгшлэх
            print(Colorate.Horizontal(Colors.rainbow, f"{{01}}: SET RANK".ljust(45) + "20.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{02}}: CHANGE EMAIL".ljust(45) + "15.5K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{03}}: CHANGE PASSWORD".ljust(45) + "10.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{04}}: REGISTER NEW ACCOUNT".ljust(45) + "1.0K"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{05}}: LOGOUT FROM ACCOUNT"))
            print(Colorate.Horizontal(Colors.rainbow, f"{{06}}: EXIT FROM TOOL"))
            print(Colorate.Horizontal(Colors.rainbow, '='*60))

            ch = Prompt.ask("\n[bold yellow][?] Select[/bold yellow]")

            if ch in ["5", "05"]: break
            if ch in ["6", "06"]: sys.exit()

            costs = {"01": 20500, "1": 20500, "02": 15500, "2": 15500, "03": 10000, "3": 10000, "04": 1000, "4": 1000}
            clean_choice = ch.zfill(2) if len(ch) == 1 else ch
            cost = costs.get(clean_choice, 0)

            if current_bal >= cost:
                success = False
                if clean_choice == "01": # Rank
                    console.print("[bold cyan][%] Hacking Rank...[/bold cyan]")
                    if cpm.make_req("set_rank", {"account_auth": cpm.auth}): success = True
                
                elif clean_choice == "02": # Email
                    new_e = Prompt.ask("[?] Enter New Email")
                    if cpm.make_req("change_email", {"account_auth": cpm.auth, "new_email": new_e}):
                        e = new_e; success = True
                
                elif clean_choice == "03": # Password
                    new_p = Prompt.ask("[?] Enter New Password")
                    if cpm.make_req("change_password", {"account_auth": cpm.auth, "new_password": new_p}):
                        p = new_p; success = True
                
                elif clean_choice == "04": # Register
                    re = Prompt.ask("[?] Reg Email")
                    rp = Prompt.ask("[?] Reg Pass")
                    if cpm.make_req("account_register", {"account_email": re, "account_password": rp}): success = True

                if success:
                    if not is_unlimited:
                        current_bal -= cost
                        update_bal(user_id_ref, current_bal)
                    print(Colorate.Horizontal(Colors.green_to_white, "SUCCESSFUL (√)"))
                    print(Colorate.Horizontal(Colors.rainbow, '='*40))
                    if Prompt.ask("[bold][?] Do You want to Exit ?", choices=["y", "n"], default="n") == "y":
                        sys.exit()
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "FAILED (✘)"))
            else:
                print(Colorate.Horizontal(Colors.red_to_white, "INSUFFICIENT BALANCE!"))
            time.sleep(2)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()

