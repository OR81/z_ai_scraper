from flask import Flask, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import uuid
import threading
import hashlib
import os
import re
import logging
from datetime import datetime, timedelta

app = Flask(__name__)

# Driver storage
drivers = {}
log_lock = threading.Lock()
LOG_FILE = 'response_log.jsonl'
TEMP_HTML_DIR = "temp_htmls"

os.makedirs(TEMP_HTML_DIR, exist_ok=True)


logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("selenium").setLevel(logging.CRITICAL)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def write_log(entry: dict):
    logging.info(entry)

    line = json.dumps(entry, ensure_ascii=False)
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def create_chrome_driver(headless=True):
    options = Options()

    if headless:
        options.add_argument("--headless=new")

        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")

    options.add_argument("--window-size=1280,1024")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    options.add_experimental_option("useAutomationExtension", False)

    return webdriver.Chrome(
        service=Service("chromedriver.exe"),
        options=options
    )



def apply_cookies(driver, file_path="cookies.json"):
    if not os.path.exists(file_path):
        logging.warning(f"Cookies file not found: {file_path}")
        return False
    with open(file_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    applied_count = 0
    for cookie in cookies:
        for field in ["sameSite", "hostOnly", "storeId", "session"]:
            cookie.pop(field, None)
        if "expiry" in cookie:
            try:
                cookie["expiry"] = int(cookie["expiry"])
            except:
                cookie.pop("expiry", None)
        if "domain" in cookie and isinstance(cookie["domain"], str) and cookie["domain"].startswith("."):
            cookie["domain"] = cookie["domain"].lstrip(".")
        if "name" in cookie and "value" in cookie:
            try:
                driver.add_cookie(cookie)
                applied_count += 1
            except Exception as e:
                logging.warning(f"Failed to add cookie '{cookie.get('name')}': {e}")
    write_log({"message": f"{applied_count} cookies applied out of {len(cookies)}"})
    try:
        driver.refresh()
        time.sleep(2)
    except:
        pass
    return True


def apply_storage(driver, session_file="session.json", local_file="local.json"):
    if os.path.exists(session_file):
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            for key, val in session_data.items():
                driver.execute_script("sessionStorage.setItem(arguments[0], arguments[1]);", key, val)
        except Exception as e:
            logging.warning(f"Failed to apply session storage: {e}")
    if os.path.exists(local_file):
        try:
            with open(local_file, "r", encoding="utf-8") as f:
                local_data = json.load(f)
            for key, val in local_data.items():
                driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", key, val)
        except Exception as e:
            logging.warning(f"Failed to apply local storage: {e}")


def normalize_prompt_cards(p: str):
    if not p:
        return None
    valid_cards = ["Al Slides", "Full-Stack", "Magic Design", "Deep Research", "Write code"]
    return p if p in valid_cards else None


def select_prompt_cards(driver, prompt_card: str):
    xpath_map = {
        "Al Slides": '//button[normalize-space(.//div[text()="AI Slides"])]',
        "Full-Stack": '//button[.//div[@class="truncate" and normalize-space(text())="Full-Stack"]]',
        "Magic Design": '//button[.//div[@class="truncate" and normalize-space(text())="Magic Design"]]',
        "Deep Research": '//button[.//div[@class="truncate" and normalize-space(text())="Deep Research"]]',
        "Write code": '//button[.//div[@class="truncate" and normalize-space(text())="Write code"]]'
    }
    if prompt_card not in xpath_map:
        logging.warning(f"Prompt card '{prompt_card}' not recognized")
        return False
    try:
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath_map[prompt_card]))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.3)
        element.click()
        write_log({"action": "select_prompt_cards", "status": "success", "card": prompt_card})
        return True
    except Exception as e:
        logging.error(f"Error selecting prompt card '{prompt_card}': {e}")
        write_log({"action": "select_prompt_cards", "status": "error", "card": prompt_card, "error": str(e)})
        return False


def cleanup_old_html_files():
    
    while True:
        if not (check_driver_alive() for driver in drivers.items()):
            return jsonify({"status":"error", "message":"driver closed"})
            
        now = datetime.now()
        for fname in os.listdir(TEMP_HTML_DIR):
            fpath = os.path.join(TEMP_HTML_DIR, fname)
            if os.path.isfile(fpath):
                creation_time = datetime.fromtimestamp(os.path.getctime(fpath))
                if now - creation_time > timedelta(minutes=30):
                    try:
                        os.remove(fpath)
                        logging.info(f"Deleted old temporary file: {fpath}")
                    except Exception as e:
                        logging.warning(f"Failed to delete {fpath}: {e}")
        time.sleep(300)  # check every 5 minutes


threading.Thread(target=cleanup_old_html_files, daemon=True).start()

def send_prompt_text(chat_box, text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        chat_box.send_keys(line)
        if i < len(lines) - 1:
            chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
            
    chat_box.send_keys(Keys.ENTER)


def parse_cookie_table(cookie_str):
    cookies = []
    lines = cookie_str.strip().split("\n")

    for line in lines:
        parts = line.split("\t")
        if len(parts) < 7:
            continue
        name = parts[0]
        value = parts[1]
        domain = parts[2]
        path = parts[3]
        expires = parts[4]

        try:
            expiry_ts = int(datetime.strptime(expires, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        except:
            expiry_ts = None

        cookies.append({
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
            "expiry": expiry_ts,
            "secure": parts[6].strip() == "✓",
            "httpOnly": False,
            "sameSite": parts[9].strip() if len(parts) > 9 and parts[9].strip() else "Lax",
        })

    return cookies

def parse_local_storage(text):
    local = {}

    if not text:
        return local

    lines = text.strip().split("\n")

    for line in lines:
        if "\t" not in line:
            continue

        key, value = line.split("\t", 1)
        value = value.strip()

        try:
            value = json.loads(value)
        except:
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.isdigit():
                value = int(value)

        local[key.strip()] = value

    return local


def parse_session_storage(text):
    session = {}

    if not text:
        return session

    lines = text.strip().split("\n")

    for line in lines:
        if "\t" not in line:
            continue

        key, value = line.split("\t", 1)
        value = value.strip()

        try:
            value = json.loads(value)
        except:
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.isdigit():
                value = int(value)

        session[key.strip()] = value

    return session

def extract_section(text, section_name):
    """
    Extracts a section from raw text like:
    cookies:
    ....
    session:
    ....
    local:
    ....
    """
    pattern = rf"{section_name}\s*:\s*(.*?)(?=\n\w+\s*:|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


@app.route('/update_storage', methods=['POST'])
def update_storage():

    text = request.get_data(as_text=True)

    if not text:
        return jsonify({"error": "cookies text required"}), 400

    cookies_text = extract_section(text, "cookies")
    session_text = extract_section(text, "session")
    local_text = extract_section(text, "local")

    parsed_cookies = parse_cookie_table(cookies_text)
    parsed_session = parse_session_storage(session_text)
    parsed_local = parse_local_storage(local_text)

    try:
        # update cookies
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(parsed_cookies, f, indent=4, ensure_ascii=False)

        # update local
        with open("local.json", "w", encoding="utf-8") as f:
            json.dump(parsed_local, f, indent=4, ensure_ascii=False)

        # update session
        with open("session.json", "w", encoding="utf-8") as f:
            json.dump(parsed_session, f, indent=4, ensure_ascii=False)

        # log
        write_log({
            "action": "update_cookies",
            "status": "success",
            "cookies": len(parsed_cookies),
            "session": bool(parsed_session),
            "local": bool(parsed_local),
        })

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/login_with_cookies', methods=['POST'])
def login_with_cookies():
    data = request.get_json()
    prompt_card = normalize_prompt_cards(data.get('prompt_card'))

    if not prompt_card:
        return jsonify({"error": "Invalid or missing prompt_card"}), 400

    session_id = uuid.uuid4().hex

    try:
        driver = create_chrome_driver(headless=True)
        drivers[session_id] = driver

        driver.get("https://chat.z.ai/")
        write_log({"action": "open_website", "status": "success", "session_id": session_id})

        apply_cookies(driver)
        apply_storage(driver)
        driver.refresh()
        time.sleep(10)

        card_selected = select_prompt_cards(driver, prompt_card)
        if not card_selected:
            logging.error(f"[{session_id}] Failed to click prompt card '{prompt_card}'")
            write_log(
                {"action": "select_prompt_cards", "status": "failed", "card": prompt_card, "session_id": session_id})
            try:
                drivers[session_id].quit()
            except:
                pass
            drivers.pop(session_id, None)
            return jsonify({"status": "error", "message": f"Unable to click prompt card '{prompt_card}'",
                            "session_id": session_id}), 500

        write_log({"action": "login", "status": "success", "session_id": session_id})

        return jsonify({"status": "success", "session_id": session_id}), 200

    except Exception as e:
        logging.error(f"[{session_id}] Login error: {e}")
        write_log({"action": "login", "status": "error", "session_id": session_id, "error": str(e)})
        if session_id in drivers:
            try:
                drivers[session_id].quit()
            except:
                pass
            drivers.pop(session_id, None)
        return jsonify({"status": "error", "message": str(e), "session_id": session_id}), 500


def check_driver_alive(driver):
    try:
        driver.title
        return True
    except:
        return False



@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    session_id = data.get("session_id")

    if not prompt:
        return jsonify({"error": "prompt required"}), 400

    driver = drivers.get(session_id)
    if not driver:
        return jsonify({"error": "driver not active"}), 404

    all_results = []
    seen_slides = set()

    try:
        write_log({"action": "send_prompt", "status": "started", "prompt": prompt, "session_id": session_id})
        
        if not check_driver_alive(driver):
            return jsonify({"status": "error", "message": "driver closed manually", "session_id": session_id}), 410

        chat_box = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="chat-input"]'))
        )
        try:
            chat_box.clear()
        except:
            pass
        try:
            
         send_prompt_text(chat_box, prompt)
         
        except Exception as e:
                logging.warning(f"send_prompt_text minor issue: {e}")

       

        WAIT_ELEMENT_XPATH = '//button[contains(@class,"copy-response-button")]'
        while True:
            if not check_driver_alive(driver):
                return jsonify({"status": "error", "message": "driver closed manually", "session_id": session_id}), 410
            try:
                wait_elem = driver.find_element(By.XPATH, WAIT_ELEMENT_XPATH)
                if wait_elem.is_displayed():
                    break
            except:
                pass
            time.sleep(5)

        add_pages = driver.find_elements(By.XPATH, '//div[contains(@class,"mcpCard") and .//div[text()="Add Page"]]')

        if add_pages:
            first_page = add_pages[0]
            try:
                view_btn = first_page.find_element(By.XPATH, './/button[text()="View"]')
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", view_btn)
                driver.execute_script("arguments[0].click();", view_btn)
                time.sleep(2)

                iframes = driver.find_elements(By.TAG_NAME, 'iframe')

                for s_idx, iframe in enumerate(iframes, start=1):
                    try:
                        html_srcdoc = iframe.get_attribute("srcdoc")
                        slide_hash = hashlib.md5(html_srcdoc.encode("utf-8")).hexdigest()

                        if slide_hash not in seen_slides:
                            seen_slides.add(slide_hash)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            file_name = os.path.join(TEMP_HTML_DIR,
                                                     f"slide_{s_idx}_{timestamp}_{uuid.uuid4().hex}.html")
                            with open(file_name, "w", encoding="utf-8") as f:
                                f.write(html_srcdoc)
                            all_results.append(file_name)
                    except Exception as e:
                        logging.warning(f"Error processing slide {s_idx}: {e}")
            except Exception as e:
                logging.error(f"Error processing first view: {e}")

        # Merge کردن همه فایل ها
        merged_html_name = os.path.join(TEMP_HTML_DIR,
                                        f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.html")
        merged_content = ""
        for f in all_results:
            with open(f, "r", encoding="utf-8") as file:
                merged_content += file.read() + "\n"
        merged_content += ""

        logging.info(
            {"result": merged_content}
        )
        if merged_content == '':#todo this condition should be check
            return jsonify(
                {"status": "error", "file_name": "", "session_id": session_id, })

        with open(merged_html_name, "w", encoding="utf-8") as f:
            f.write(merged_content)

        for f in all_results:
            if f != merged_html_name and os.path.exists(f):
                try:
                    os.remove(f)
                except Exception as e:
                    logging.warning(f"Failed to delete {f}: {e}")


        write_log({"status": "success", "file_name": merged_html_name, "session_id": session_id})
        return jsonify(
            {"status": "success", "file_name": merged_html_name, "session_id": session_id, })



    except Exception as e:
        logging.exception(f"[{session_id}] send_prompt exception")
        return jsonify({"status": "error", "message": "internal error occurred, check logs", "session_id": session_id}), 500

@app.route('/active_driver', methods=['GET'])
def active_driver():
    active = []

    for session_id, driver in drivers.items():

        try:
            _ = driver.title

            active.append({"session_id": session_id, "status": "active"})

        except:
            active.append({"session_id": session_id, "status": "dead"})

    return jsonify({
        "count": len(active),
        "drivers": active
    })


@app.route('/download_file', methods=['GET'])
def download_file_by_path():
    file_path = request.args.get("file_path")
    if not file_path:
        write_log({"error": "file_path required"})
        return jsonify({"error": "file_path required"}), 400

    
    abs_path = os.path.abspath(file_path)
    temp_dir_abs = os.path.abspath(TEMP_HTML_DIR)
    if not abs_path.startswith(temp_dir_abs):
        write_log({"error": "access denied", "file_path": file_path})
        return jsonify({"error": "access denied"}), 403

    if not os.path.exists(abs_path):
        write_log({"error": "file not found", "file_path": file_path})
        return jsonify({"error": "file not found"}), 404

    try:
        write_log({"action": "download_file", "status": "success", "file_path": file_path})
        return send_file(
            abs_path,
            mimetype='text/html',
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
    except Exception as e:
        write_log({"error": str(e), "file_path": file_path})
        return jsonify({"error": str(e)}), 500



@app.route('/close_driver', methods=['POST'])
def close_driver():
    data = request.get_json()
    session_id = data.get("session_id")

    driver = drivers.get(session_id)
    if not driver:
        return jsonify({"error": "driver not active"}), 404

    try:
        driver.quit()
        drivers.pop(session_id, None)
        return jsonify({"status": "closed", "session_id": session_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    write_log({
        "action": "server_start",
        "status": "running",
        "message": "Server is up and ready to accept requests",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)


