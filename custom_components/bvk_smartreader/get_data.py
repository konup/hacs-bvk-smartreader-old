import os
import sys
import requests
from bs4 import BeautifulSoup

def set_dot_net_env_from(content):
    soup = BeautifulSoup(content, 'html.parser')
    viewstate = soup.find('input', {'id': '__VIEWSTATE'}).get('value', '')
    eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'}).get('value', '')
    viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value', '')
    previouspage = soup.find('input', {'id': '__PREVIOUSPAGE'}).get('value', '')
    return viewstate, eventvalidation, viewstategenerator, previouspage

def main(bvk_user, bvk_password):
    if not bvk_user or not bvk_password:
        print("STOP: bvkUser or bvkPassword missing")
        sys.exit(1)

    bvk_url = "https://zis.bvk.cz"
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    # Step 01: HOMEPAGE
    response = session.get(f"{bvk_url}/Default.aspx", headers=headers)
    if response.status_code != 200:
        print("STOP: get HOMEPAGE failed")
        sys.exit(1)

    viewstate, eventvalidation, viewstategenerator, previouspage = set_dot_net_env_from(response.text)

    # Step 02: LOGIN
    login_data = {
        'ctl00$ctl00$ToolkitScriptManager1': 'ctl00$ctl00$lvLoginForm$LoginDialog1$updatePanellAddress|ctl00$ctl00$lvLoginForm$LoginDialog1$btnLogin',
        '__LASTFOCUS': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__PREVIOUSPAGE': previouspage,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ctl00$lvLoginForm$LoginDialog1$edEmail': bvk_user,
        'ctl00$ctl00$lvLoginForm$LoginDialog1$edPassword': bvk_password,
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$PageName': 'Default.aspx',
        '__ASYNCPOST': 'true',
        'ctl00$ctl00$lvLoginForm$LoginDialog1$btnLogin': 'Login'
    }

    headers.update({
        'Referer': f"{bvk_url}/Default.aspx",
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Origin': bvk_url
    })

    response = session.post(f"{bvk_url}/Default.aspx", headers=headers, data=login_data)
    if response.status_code != 200:
        print("STOP: get LOGIN failed")
        sys.exit(1)

    # Step 03: LOGIN-REDIR
    response = session.get(f"{bvk_url}/Default.aspx", headers=headers)
    if response.status_code != 200:
        print("STOP: get LOGIN-REDIR failed")
        sys.exit(1)

    viewstate, eventvalidation, viewstategenerator, previouspage = set_dot_net_env_from(response.text)

    # Step 04: LIST
    list_data = {
        'ctl00$ctl00$ToolkitScriptManager1': 'ctl00$ctl00$MainMenu1$UpdatePanelMenu|ctl00$ctl00$MainMenu1$btnCPSelect',
        '__EVENTTARGET': 'ctl00$ctl00$MainMenu1$btnCPSelect',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__PREVIOUSPAGE': previouspage,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$PageName': 'Default.aspx',
        '__ASYNCPOST': 'true'
    }

    response = session.post(f"{bvk_url}/Default.aspx", headers=headers, data=list_data)
    if response.status_code != 200:
        print("STOP: get LIST failed")
        sys.exit(1)

    if "0|error|500" in response.text:
        print("STOP: get LIST failed - 500")
        sys.exit(1)

    if "pageRedirect" not in response.text:
        print("STOP: get LIST failed - pageRedirect")
        sys.exit(1)

    # Step 05: LIST-REDIR
    response = session.get(f"{bvk_url}/ConsumptionPlaceList.aspx", headers=headers)
    if response.status_code != 200:
        print("STOP: get LIST-REDIR failed")
        sys.exit(1)

    viewstate, eventvalidation, viewstategenerator, previouspage = set_dot_net_env_from(response.text)
    bvk_customer_id = BeautifulSoup(response.text, 'html.parser').find('input', {'id': 'ctl00_ctl00_ContentPlaceHolder1Common_ContentPlaceHolder1_hfCA'}).get('value', '')
    bvk_row_id = 0

    if not bvk_customer_id:
        print("STOP: bvkCustomerID missing")
        sys.exit(1)

    # Step 06: PLACE
    place_data = {
        'ctl00$ctl00$ToolkitScriptManager1': 'ctl00$ctl00$FormPanel|ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$gvConsumptionPlaces',
        '__EVENTTARGET': f'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$gvConsumptionPlaces',
        '__EVENTARGUMENT': f'Show${bvk_row_id}',
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__VIEWSTATEENCRYPTED': '',
        '__PREVIOUSPAGE': previouspage,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$PageName': 'ConsumptionPlaceList.aspx',
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$hfCA': bvk_customer_id,
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$hfCP': '',
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$hfCH': '',
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$hfCW': '',
        'ctl00$ctl00$ContentPlaceHolder1Common$ContentPlaceHolder1$hfCSCPT': '',
        '__ASYNCPOST': 'true'
    }

    response = session.post(f"{bvk_url}/ConsumptionPlaceList.aspx", headers=headers, data=place_data)
    if response.status_code != 200:
        print("STOP: get PLACE failed")
        sys.exit(1)

    # Step 07: PLACE-REDIR
    response = session.get(f"{bvk_url}/UserData/MainInfo.aspx", headers=headers)
    if response.status_code != 200:
        print("STOP: get PLACE-PLACE failed")
        sys.exit(1)

    # Step 11: get SUEZ-VALUES
    suez_token = BeautifulSoup(response.text, 'html.parser').find('a', href=True, text=lambda x: 'token' in x).get('href').split('token=')[1].split('&amp;')[0]
    suez_url = f"https://cz-sitr.suezsmartsolutions.com/eMIS.SE_BVK/Login.aspx?token={suez_token}&langue=en-GB"

    if not suez_token or not suez_url:
        print("STOP: suezToken or suezUrl missing")
        sys.exit(1)

    response = session.get(suez_url, headers=headers)
    if response.status_code != 200:
        print("STOP: get SUEZ-VALUES failed")
        sys.exit(1)

    suez_value = BeautifulSoup(response.text, 'html.parser').find(text=lambda x: 'Index Base of' in x).split('val = ')[1].split(';')[0]
    suez_date_s = BeautifulSoup(response.text, 'html.parser').find(text=lambda x: 'TitreCouleur').split('>')[1].split('<')[0]
    suez_id = BeautifulSoup(response.text, 'html.parser').find('span', {'id': 'ctl00_PHTitre_LabelTitreSite'}).text

    if not suez_value or not suez_date_s or not suez_id:
        print("STOP: suezValue, suezDateS or suezID missing")
        sys.exit(1)

    # End
    print(f"[{{ \"value\": {suez_value} }}]")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <bvkUser> <bvkPassword>")
        sys.exit(1)
    bvk_user = sys.argv[1]
    bvk_password = sys.argv[2]
    main(bvk_user, bvk_password)

