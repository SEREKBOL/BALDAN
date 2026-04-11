import os, requests, json, time, sys

# Pystyle шалгах
try:
    from pystyle import Colors, Colorate
    PYSTYLE_AVAILABLE = True
except ImportError:
    PYSTYLE_AVAILABLE = False
    print("⚠️ pystyle not found! Installing...")
    os.system("pip install pystyle")
    from pystyle import Colors, Colorate

# --- ТОХИРГОО ---
API_BASE_URL = "https://kayzennv3-cpm.squareweb.app/api"
API_KEY = "APIKEY38"
FIREBASE_URL = "https://kayzen-1ff37-default-rtdb.firebaseio.com/users.json"
ADMIN_KEY = "Telmunn69"
__CHANNEL__ = "BaldanShopChannel"
__CHAT__ = "BaldanShopChat"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    brand = "Car Parking Multiplayer Tool"
    
    # Horizontal colours - SOLONGO
    print(Colorate.Horizontal(Colors.rainbow, "="*60))
    print(Colorate.Horizontal(Colors.rainbow, brand.center(60)))
    print(Colorate.Horizontal(Colors.rainbow, "="*60))
    print(Colorate.Horizontal(Colors.blue_to_red, " PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL".center(60)))
    print(Colorate.Horizontal(Colors.red_to_blue, " SHARING THE ACCESS KEY IS NOT ALLOWED".center(60)))
    print(Colorate.Horizontal(Colors.rainbow, f" Telegram: @{__CHANNEL__}  @{__CHAT__}".center(60)))
    print(Colorate.Horizontal(Colors.rainbow, "="*60))

class CPMApiClient:
    def __init__(self): 
        self.auth = None
        
    def login(self, e, p):
        try:
            res = requests.post(
                f"{API_BASE_URL}/account_login", 
                params={"api_key": API_KEY}, 
                json={"account_email": e, "account_password": p},
                timeout=10
            ).json()
            if res.get('ok') or str(res.get('message', '')).upper() == "SUCCESSFUL":
                self.auth = res.get('data', {}).get('auth') or res.get('auth')
                return True
            return False
        except:
            return False
            
    def make_req(self, end, data):
        try:
            res = requests.post(
                f"{API_BASE_URL}/{end}", 
                params={"api_key": API_KEY}, 
                json=data,
                timeout=10
            ).json()
            return res.get('ok') or res.get('error') == 0
        except:
            return False

def load_db():
    try:
        response = requests.get(FIREBASE_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def update_bal(uid, bal):
    try:
        url = f"https://kayzen-1ff37-default-rtdb.firebaseio.com/users/{uid}.json"
        requests.patch(url, json={"balance": bal}, timeout=10)
        return True
    except:
        return False

def main():
    while True:
        banner()
        
        # Horizontal colours - INPUT
        print(Colorate.Horizontal(Colors.cyan_to_blue, "[?] Enter your account details".center(60)))
        
        e = input(Colorate.Horizontal(Colors.green_to_white, "[?] Account Email: ")).strip()
        p = input(Colorate.Horizontal(Colors.green_to_white, "[?] Account Password: ")).strip()
        k = input(Colorate.Horizontal(Colors.green_to_white, "[?] Access Key: ")).strip()
        
        if not e or not p or not k:
            banner()
            print(Colorate.Horizontal(Colors.red_to_white, "[✘] All fields are required!"))
            time.sleep(2)
            continue

        db = load_db()
        user_id_ref, found_user = None, None
        
        if k != ADMIN_KEY:
            for uid, data in db.items():
                if data and str(data.get('key', '')) == str(k):
                    user_id_ref, found_user = uid, data
                    break
        
        # Unlimited эсэхийг шалгах
        is_unlimited = (k == ADMIN_KEY) or (found_user and found_user.get('is_unlimited') == True)
        
        if k != ADMIN_KEY and (not found_user or found_user.get('is_blocked')):
            banner()
            print(Colorate.Horizontal(Colors.red_to_white, f"[✘] Invalid or blocked Access Key: {k}"))
            time.sleep(3)
            continue

        cpm = CPMApiClient()
        if not cpm.login(e, p):
            banner()
            print(Colorate.Horizontal(Colors.red_to_white, f"[✘] Login failed for: {e}"))
            time.sleep(3)
            continue

        # Main menu loop
        while True:
            banner()
            db = load_db()
            
            if not is_unlimited:
                current_bal = int(db.get(user_id_ref, {}).get('balance', 0))
            else:
                current_bal = 999999
            
            # Horizontal colours - Мэдээлэл
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"Account Email: {e}"))
            print(Colorate.Horizontal(Colors.green_to_white, f"Balance: {'Unlimited' if is_unlimited else f'{current_bal:,}'}"))
            print(Colorate.Horizontal(Colors.yellow_to_red, f"Access Key: {k}"))
            print(Colorate.Horizontal(Colors.rainbow, "="*60))

            # Menu - Horizontal colours
            print(Colorate.Horizontal(Colors.rainbow, "{01}: SET RANK".ljust(45) + "20.5K"))
            print(Colorate.Horizontal(Colors.orange_to_red, "{02}: CHANGE EMAIL".ljust(45) + "15.5K"))
            print(Colorate.Horizontal(Colors.yellow_to_green, "{03}: CHANGE PASSWORD".ljust(45) + "10.0K"))
            print(Colorate.Horizontal(Colors.green_to_blue, "{04}: REGISTER NEW ACCOUNT".ljust(45) + "1.0K"))
            print(Colorate.Horizontal(Colors.purple_to_red, "{05}: LOGOUT FROM ACCOUNT"))
            print(Colorate.Horizontal(Colors.red_to_black, "{06}: EXIT FROM TOOL"))
            print(Colorate.Horizontal(Colors.rainbow, "="*60))

            ch = input(Colorate.Horizontal(Colors.white_to_cyan, "\n[?] Select: ")).strip()
            
            if ch in ["5", "05"]:
                break
            if ch in ["6", "06"]:
                print(Colorate.Horizontal(Colors.green_to_white, "[✓] Goodbye!"))
                sys.exit()

            costs = {"01":20500, "1":20500, "02":15500, "2":15500, 
                    "03":10000, "3":10000, "04":1000, "4":1000}
            cost = costs.get(ch.zfill(2) if len(ch) == 1 else ch, 0)

            if current_bal >= cost:
                success = False
                
                if ch in ["1", "01"]:
                    print(Colorate.Horizontal(Colors.blue_to_cyan, "[*] Setting rank..."))
                    success = cpm.make_req("set_rank", {"account_auth": cpm.auth})
                    
                elif ch in ["2", "02"]:
                    ne = input(Colorate.Horizontal(Colors.green_to_white, "[?] New Email: ")).strip()
                    if ne:
                        success = cpm.make_req("change_email", {"account_auth": cpm.auth, "new_email": ne})
                        if success:
                            e = ne
                    
                elif ch in ["3", "03"]:
                    np = input(Colorate.Horizontal(Colors.green_to_white, "[?] New Password: ")).strip()
                    if np:
                        success = cpm.make_req("change_password", {"account_auth": cpm.auth, "new_password": np})
                        if success:
                            p = np
                    
                elif ch in ["4", "04"]:
                    re = input(Colorate.Horizontal(Colors.cyan_to_blue, "[?] Reg Email: ")).strip()
                    rp = input(Colorate.Horizontal(Colors.cyan_to_blue, "[?] Reg Pass: ")).strip()
                    if re and rp:
                        try:
                            resp = requests.post(
                                f"{API_BASE_URL}/account_register", 
                                params={"api_key": API_KEY}, 
                                json={"account_email": re, "account_password": rp},
                                timeout=10
                            ).json()
                            success = resp.get('ok', False)
                        except:
                            success = False

                if success:
                    if not is_unlimited:
                        new_balance = current_bal - cost
                        update_bal(user_id_ref, new_balance)
                        print(Colorate.Horizontal(Colors.green_to_white, f"[✓] New balance: {new_balance:,}"))
                    
                    print(Colorate.Horizontal(Colors.green_to_white, "✓ SUCCESSFUL!"))
                    
                    exit_choice = input(Colorate.Horizontal(Colors.yellow_to_white, "[?] Do you want to Exit? (y/n): ")).strip().lower()
                    if exit_choice == "y":
                        sys.exit()
                else:
                    print(Colorate.Horizontal(Colors.red_to_white, "✘ FAILED!"))
            else:
                print(Colorate.Horizontal(Colors.red_to_white, f"✘ INSUFFICIENT BALANCE! Need {cost:,}, you have {current_bal:,}"))
            
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colorate.Horizontal(Colors.yellow_to_white, "\n[!] Interrupted by user"))
        sys.exit()

