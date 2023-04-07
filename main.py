from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

def _gotstats(update,context):
    lmatch = 0
    f = open("logins.txt","r")
    data = f.read()
    f.close()
    datar = data.split("/")
    sender = str(update.effective_user.id)
    if sender in datar:
        pl = datar.index(sender) + 2
        password = datar[pl]
        name = datar[pl - 1]
        accname = name + "'s stats:\n" + "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        login_url = "https://www.sheepit-renderfarm.com/user/authenticate"
        login_data = {
            "login": name,
            "password": password
        }
        cookies = str(requests.post(login_url, data=login_data).cookies)
        cookies = cookies.split("Cookie ")
        phpsessid = cookies[1].replace(" for www.sheepit-renderfarm.com/>, <","")
        rememberme = cookies[2].replace(" for www.sheepit-renderfarm.com/>]>","")
        cookie = rememberme + "; " + phpsessid
        res = requests.get('https://www.sheepit-renderfarm.com/user/' + name + '/profile', headers = {'Cookie': cookie}).text
        res = res.split("\n")
        for idx, line in enumerate(res):
            if idx == lmatch + 1:
                if 'Points' in line:
                    Ar = line.split("span")
                    Ar = Ar[1].split("ul>")
                    Ar2 = line.split("dd>")
                    points = "Points: " + Ar[2] + "\n"
                    rendered = "Frames rendered: " + Ar2[5].replace("</","\n")
                    ordered = "Frames ordered: " + Ar2[3].replace("</","\n")
                    trendered = "Time rendered: " + Ar2[7].replace("</","\n")
                    rank = "Rank: " + Ar2[9].replace("</","\n")
                    usrpoints = points.replace('">','').replace('</','').replace(',','.')
            if '<div class="col-md-4">' in line:
                lmatch = idx
        text = accname + usrpoints + rendered + trendered + rank + ordered.replace("\n","")
        return text
    else:
        return "You aren't registered yet!\nRegister using the '/register Username Password: ...' command."

def _gotregister(update,context):
    f = open("logins.txt","r")
    data = f.read()
    f.close()
    datar = data.split("/")
    sender = str(update.effective_user.id)
    if sender in datar:
        text = 'You are already registered!\nRetrive your stats using the /stats command or unregister using the /unregister command'
        return text
    else:
        content = update.message.text
        f = open("logins.txt","r")
        data = f.read()
        f.close()
        arr = content.split(" ")
        if len(arr) == 4:
            verifier = content.split(":")
            password = content.replace("/register " + arr[1] + " Password: ", "")
            if verifier[0] == "/register " + arr[1] + " Password":
                login_url = "https://www.sheepit-renderfarm.com/user/authenticate"
                login_data = {
                    "login": arr[1],
                    "password": password
                }
                res = str(requests.post(login_url, data=login_data).text)
                if res == "OK":
                    if data == "":
                        mdata = str(update.effective_user.id) + "/" + arr[1] + "/" + password
                    else:
                        mdata = data + "/" + str(update.effective_user.id) + "/" + arr[1] + "/" + password
                    f = open("logins.txt","w")
                    data = f.write(mdata)
                    f.close()
                    text = 'You sucessfully registered, you can now delete the message for safety measures and retrieve your stats using /stats'
                    return text
                else:
                    text = 'Your Username or password isn\'t correct, the syntax of /register is "/register Username Password: ..."'
                    return text
            else:
                text = 'The syntax of /register is "/register Username Password: ..."'
                return text
        else:
            text = 'The syntax of /register is "/register Username Password: ..."'
            return text

def _gotunregister(update,context):
    f = open("logins.txt","r")
    data = f.read()
    f.close()
    datar = data.split("/")
    sender = str(update.effective_user.id)
    if sender in datar:
        cl = datar.index(sender)
        datar.pop(cl)
        datar.pop(cl)
        datar.pop(cl)
        data = str("/".join(datar))
        f = open("logins.txt","w")
        data = f.write(data)
        f.close()
        text = "Sucessfully unregistered!"
        return text
    else:
        text = 'You aren\'t registered yet, you can register using "/register Username Password: ..."'
        return text

async def gotstats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = _gotstats(update, context)
    await update.message.reply_text(text)

async def gotregister(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = _gotregister(update, context)
    await update.message.reply_text(text)

async def gotunregister(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = _gotunregister(update, context)
    await update.message.reply_text(text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Commands:\n /help: Show this message\n /register: Register to this bot, syntax: \"/register Username Password: ...\" \n /stats: Show your stats \n /unregister: Unregister from this bot\n NOTE: By registering here your login information WILL BE STORED, if you are uncomfortable with this (I can fully understand this), you can host your own bot with the code found here: https://github.com/usr577/Sheepit-stats-telegram-bot"
    await update.message.reply_text(text)

app = ApplicationBuilder().token("<YOUR_TOKEN_HERE>").build()

app.add_handler(CommandHandler("stats", gotstats))

app.add_handler(CommandHandler("register", gotregister))

app.add_handler(CommandHandler("unregister", gotunregister))

app.add_handler(CommandHandler("start", help))
app.add_handler(CommandHandler("help", help))

app.run_polling()