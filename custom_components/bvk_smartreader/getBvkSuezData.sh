#!/bin/bash

cd custom_components/bvk_smartreader

elog()
{

  DAT=`date "+%F %T"`
  TXT="$1"
  [ "$2" == "" ] && LEVEL="INFO" || LEVEL="$2"
  [ "$LOGF" == "" ] && export LOGF="logs/getBvkSuezData.log"
  echo "[$DAT] $LEVEL $0 ${TXT}" >> $LOGF
  [ "$3" != "" ] && { elog "STOP"; exit $3; }
}

elog "begin"

elog "workDirectory=$(pwd)"

[ "$1" == "" ] && [ "$2" == "" ] && [ ! -f ".credentials" ] && { echo "STOP: bvkUser and bvkpassword missing and also .credentials file not found"; exit 1; }

[ "$1" != "" ] && [ "$2" != "" ] && {
  bvkUser="$1"
  bvkPassword="$2"
  elog "apply credentials from command line arguments ( bvkUser=${bvkUser}, bvkPassword=***** )"
}
[ "$1" == "" ] && [ "$2" == "" ] && {
  . .credentials
  elog "apply credentials from .credentials file ( bvkUser=${bvkUser}, bvkPassword=***** )"
}

bvkUrl="https://zis.bvk.cz"

[ "$bvkUrl"      == "" ] && { echo "STOP: bvkUrl missing"; exit 1; }
[ "$bvkUser"     == "" ] && { echo "STOP: bvkUser missing"; exit 1; }
[ "$bvkPassword" == "" ] && { echo "STOP: bvkPassword missing"; exit 1; }

elog "bvkUser=${bvkUser} ; bvkUrl=${bvkUrl}"

rm -f ./response-*.html
rm -f ./cookie-*.txt

curlParm="-s -L -i --http1.1"

headerUserAgent='User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
headerAcceptLanguage='Accept-Language: en-US,en;q=0.5'
headerAcceptStd='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
headerAcceptAll='Accept: */*'
headerContentTypeApp='Content-Type: application/x-www-form-urlencoded; charset=utf-8'

setDotNetEnvFrom()
{
  VIEWSTATE=`cat $1 | sed -n 's/.*name="__VIEWSTATE" id="__VIEWSTATE" value="\([^"]*\)".*/\1/p'`
  EVENTVALIDATION=`cat $1 | sed -n 's/.*name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="\([^"]*\)".*/\1/p'`
  VIEWSTATEGENERATOR=`cat $1 | sed -n 's/.*name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="\([^"]*\)".*/\1/p'`
  PREVIOUSPAGE=`cat $1 | sed -n 's/.*name="__PREVIOUSPAGE" id="__PREVIOUSPAGE" value="\([^"]*\)".*/\1/p'`
}

###
### 01 HOMEPAGE
###

elog "01 HOMEPAGE"

curl -X GET \
$curlParm \
-c cookie-01.txt \
-o response-01.html \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptStd" \
"$bvkUrl/Default.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get HOMEPAGE failed"; exit 1; }


###
### 02 LOGIN
###

elog "02 LOGIN"

setDotNetEnvFrom response-01.html

curl -X POST \
$curlParm \
-o response-02.html \
-b cookie-01.txt \
-c cookie-02.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptAll" \
-H "Referer: $bvkUrl/Default.aspx" \
-H "X-Requested-With: XMLHttpRequest" \
-H "X-MicrosoftAjax: Delta=true" \
-H "$headerContentTypeApp" \
-H "Origin: $bvkUrl" \
--data-urlencode "ctl00\$ctl00\$ToolkitScriptManager1=ctl00\$ctl00\$lvLoginForm\$LoginDialog1\$updatePanellAddress|ctl00\$ctl00\$lvLoginForm\$LoginDialog1\$btnLogin" \
--data-urlencode "__LASTFOCUS=" \
--data-urlencode "__EVENTTARGET=" \
--data-urlencode "__EVENTARGUMENT=" \
--data-urlencode "__VIEWSTATE=$VIEWSTATE" \
--data-urlencode "__VIEWSTATEGENERATOR=$VIEWSTATEGENERATOR" \
--data-urlencode "__PREVIOUSPAGE=$PREVIOUSPAGE" \
--data-urlencode "__EVENTVALIDATION=$EVENTVALIDATION" \
--data-urlencode "ctl00\$ctl00\$lvLoginForm\$LoginDialog1\$edEmail=$bvkUser" \
--data-urlencode "ctl00\$ctl00\$lvLoginForm\$LoginDialog1\$edPassword=$bvkPassword" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$PageName=Default.aspx" \
--data-urlencode "__ASYNCPOST=true" \
--data-urlencode "ctl00\$ctl00\$lvLoginForm\$LoginDialog1\$btnLogin=Login" \
"$bvkUrl/Default.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get LOGIN failed"; exit 1; }


###
### 03 LOGIN-REDIR
###

elog "03 LOGIN-REDIR"

curl -X GET \
$curlParm \
-o response-03.html \
-b cookie-02.txt \
-c cookie-03.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptStd" \
-H "Referer: $bvkUrl/Default.aspx" \
"$bvkUrl/Default.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get LOGIN-REDIR failed"; exit 1; }


###
### 04 LIST
###

elog "04 LIST"

setDotNetEnvFrom response-03.html

curl -X POST \
$curlParm \
-o response-04.html \
-b cookie-03.txt \
-c cookie-04.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptAll" \
-H "Referer: $bvkUrl/Default.aspx" \
-H "X-Requested-With: XMLHttpRequest" \
-H "X-MicrosoftAjax: Delta=true" \
-H "$headerContentTypeApp" \
-H "Origin: $bvkUrl" \
--data-urlencode "ctl00\$ctl00\$ToolkitScriptManager1=ctl00\$ctl00\$MainMenu1\$UpdatePanelMenu|ctl00\$ctl00\$MainMenu1\$btnCPSelect" \
--data-urlencode "__EVENTTARGET=ctl00\$ctl00\$MainMenu1\$btnCPSelect" \
--data-urlencode "__EVENTARGUMENT=" \
--data-urlencode "__VIEWSTATE=$VIEWSTATE" \
--data-urlencode "__VIEWSTATEGENERATOR=$VIEWSTATEGENERATOR" \
--data-urlencode "__PREVIOUSPAGE=$PREVIOUSPAGE" \
--data-urlencode "__EVENTVALIDATION=$EVENTVALIDATION" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$PageName=Default.aspx" \
--data-urlencode "__ASYNCPOST=true" \
"$bvkUrl/Default.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get LIST failed"; exit 1; }

RES=`grep "0|error|500" response-04.html`
[ "$RES" != "" ] && { echo "STOP: get LIST failed - 500"; exit 1; }
RES=`grep "pageRedirect" response-04.html`
[ "$RES" == "" ] && { echo "STOP: get LIST failed - pageRedirect"; exit 1; }

###
### 05 LIST-REDIR
###

elog "05 LIST-REDIT"

curl -X GET \
$curlParm \
-o response-05.html \
-b cookie-04.txt \
-c cookie-05.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptStd" \
-H "Referer: $bvkUrl/Default.aspx" \
"$bvkUrl/ConsumptionPlaceList.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get LIST-REDIR failed"; exit 1; }


###
### 06 PLACE
###

elog "06 PLACE"

setDotNetEnvFrom response-05.html
bvkCustomerID=`cat response-05.html | grep ctl00_ctl00_ContentPlaceHolder1Common_ContentPlaceHolder1_hfCA | sed 's/.*value="\([0-9]*\)".*/\1/'`
bvkRowID=0

[ "$bvkCustomerID" == "" ] && { echo "STOP: bvkCustomerID missing"; exit 1; }

curl -X POST \
$curlParm \
-o response-06.html \
-b cookie-05.txt \
-c cookie-06.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptAll" \
-H "Referer: $bvkUrl/ConsumptionPlaceList.aspx" \
-H 'X-Requested-With: XMLHttpRequest' \
-H 'X-MicrosoftAjax: Delta=true' \
-H "$headerContentTypeApp" \
-H "Origin: $bvkUrl" \
--data-urlencode "ctl00\$ctl00\$ToolkitScriptManager1=ctl00\$ctl00\$FormPanel|ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$gvConsumptionPlaces" \
--data-urlencode "__EVENTTARGET=ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$gvConsumptionPlaces" \
--data-urlencode "__EVENTARGUMENT=Show\$$bvkRowID" \
--data-urlencode "__VIEWSTATE=$VIEWSTATE" \
--data-urlencode "__VIEWSTATEGENERATOR=$VIEWSTATEGENERATOR" \
--data-urlencode "__VIEWSTATEENCRYPTED=" \
--data-urlencode "__PREVIOUSPAGE=$PREVIOUSPAGE" \
--data-urlencode "__EVENTVALIDATION=$EVENTVALIDATION" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$PageName=ConsumptionPlaceList.aspx" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$hfCA=$bvkCustomerID" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$hfCP=" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$hfCH=" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$hfCW=" \
--data-urlencode "ctl00\$ctl00\$ContentPlaceHolder1Common\$ContentPlaceHolder1\$hfCSCPT=" \
--data-urlencode "__ASYNCPOST=true" \
"$bvkUrl/ConsumptionPlaceList.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get PLACE failed"; exit 1; }


###
### 07 PLACE-REDIR
###

elog "07 PLACE-REDIR"

curl -X GET \
$curlParm \
-o response-07.html \
-b cookie-06.txt \
-c cookie-07.txt \
-H "$headerUserAgent" \
-H "$headerAcceptLanguage" \
-H "$headerAcceptStd" \
-H "Referer: $bvkUrl/ConsumptionPlaceList.aspx" \
"$bvkUrl/UserData/MainInfo.aspx"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get PLACE-PLACE failed"; exit 1; }


###
### 11 get SUEZ-VALUES
###

elog "11 SUEZ-VALUES"

suezToken=`cat response-07.html | grep "https://cz-sitr.suezsmartsolutions.com/eMIS.SE_BVK/Login.aspx?token" | sed 's/.*token=\(.*\)&amp;.*/\1/'`
suezUrl="https://cz-sitr.suezsmartsolutions.com/eMIS.SE_BVK/Login.aspx?token=$suezToken&amp;langue=en-GB"

[ "$suezToken" == "" ] && { echo "STOP: suezToken missing"; exit 1; }
[ "$suezUrl"   == "" ] && { echo "STOP: suezUrl missing"; exit 1; }

elog "suezUrl=${suezUrl} ; suezToken=${suezToken}"

curl -X GET \
$curlParm \
-o response-11.html \
-c cookie-11.txt \
"$suezUrl"
rCode=$?
[ $rCode -ne 0 ] && { echo "STOP: get SUEZ-VALUES failed"; exit 1; }

suezValue=`cat response-11.html | grep "Index Base of" | sed 's/.* val = \([0-9]*\.[0-9]*\);.*/\1/'`
suezDateS=`cat response-11.html | grep "Index Base of" | sed 's/.*TitreCouleur.>//' | cut -d "<" -f 1`
suezID=`cat response-11.html | grep ctl00_PHTitre_LabelTitreSite | sed 's/.*ctl00_PHTitre_LabelTitreSite">\(.*\)<\/span>.*/\1/'`

[ "$suezValue" == "" ] && { echo "STOP: suezValue missing"; exit 1; }
[ "$suezDateS" == "" ] && { echo "STOP: suezDateS missing"; exit 1; }
[ "$suezID" == "" ]    && { echo "STOP: suezID missing"; exit 1; }

elog "suezID=${suezID} ; suezDateS=${suezDateS} ; suezValue=${suezValue}"


###
### 99 end
###

elog "99 end"

rm -f ./response-*.html
rm -f ./cookie-*.txt

elog "echo suezValue=${suezValue}"

echo "[ { \"value\": $suezValue } ]"

elog "finish"

exit 0

