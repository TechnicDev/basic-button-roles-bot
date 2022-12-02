import requests, json
from interactions import message

class interactions:
    def __init__(self, token, client_id):
        self.token=token
        self.client_id=client_id

    def dm_user(self, user_id, content, comp={}):
        url = "https://discord.com/api/users/@me/channels"
        data = {
          "recipient_id": int(user_id)
        }
        header = {
          "Authorization": u"Bot {}".format(self.token),
          "Content-Type": u"application/json"
        }
        resp = requests.post(url, json=data, headers=header)
        D = resp.json()

        if type(content)==message.embed: content=content.data
        if type(content)==str: content={"content": content}
        if type(comp)==message.components.action_row: content["components"]=comp.data

        url = "https://discord.com/api/channels/{}/messages".format(D.get("id"))
        data = content
        header = {
          "Authorization": u"Bot {}".format(self.token),
          "Content-Type": u"application/json"
        }
        resp = requests.post(url, json=data, headers=header)
        try:resp.raise_for_status()
        except:print("Discord Returned an error:", resp.text)
        return resp.json()

    def send_message(ctx, client, embed, components):
        url=f"https://discord.com/api/channels/{ctx.channel.id}/messages"
        re=requests.post(url, headers={"Authorization": "Bot "+client.http.token}, json={
            "embed": embed,
            "components": [
            {
                "type": 1,
                "components": components
            }
        ]
    })
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        return re.json()

    def edit_message(ctx, client, embed, components):
        url=f"https://discord.com/api/channels/{ctx.channel.id}/messages/{ctx.id}"
        re=requests.patch(url, headers={"Authorization": "Bot "+client.http.token}, json={
            "embed": embed,
            "components": [
            {
                "type": 1,
                "components": components
            }
        ]
    })
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        return re.json()

    def make_response(self, content, flags, token, iid, t=4):
        d=content
        d["flags"] = flags
        data = {
            "type": t,
            "data": d
        }
        
        url = "https://discord.com/api/interactions/{}/{}/callback".format(iid, token)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.post(url, json=data, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def edit_response(self, content, flags, token, iid, t=4):
        d=content
        d["flags"] = flags
        data = d
        
        url = "https://discord.com/api/webhooks/{}/{}/messages/@original".format(self.client_id, token)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.patch(url, json=data, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def make_modal(self, iid, token, data):
        data = {
            "type": 9,
            "data":data
        }
        
        url = "https://discord.com/api/interactions/{}/{}/callback".format(iid, token)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.post(url, json=data, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def delete_response(self,token):
        
        url = "https://discord.com/api/webhooks/{}/{}/messages/@original".format(self.client_id, token)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.delete(url, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def send_message(self, content, channel):
        
        url = "https://discord.com/api/channels/{}/messages".format(channel)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.post(url, json=content, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def webhook_send(self, data, token):
        
        url = "https://discord.com/api/webhooks/{}/{}".format(self.client_id, token)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.post(url, json=data, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def webhook_edit(self, data, token, mid):
        
        url = "https://discord.com/api/webhooks/{}/{}/messages/{}".format(self.client_id, token, mid)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.patch(url, json=data, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    def webhook_delete(self, token, mid):
        
        url = "https://discord.com/api/webhooks/{}/{}/messages/{}".format(self.client_id, token, mid)
        headers = {
            "Authorization": "Bot "+self.token
        }
        re = requests.delete(url, headers=headers)
        try:re.raise_for_status()
        except:print("Discord Returned an error:", re.text)
        try:
            return re.json()
        except:
            return re.text

    class interaction_response:
        def __init__(self, data, inte, dpy):
            self.channel=data["channel_id"]
            self.guild=data.get("guild_id")
            if data.get("member")!=None:
                self.user=data["member"]["user"]["id"]
                self.user_name=data["member"]["user"]["username"]+"#"+data["member"]["user"]["discriminator"]
            else:
                self.user=data["user"]["id"]
                self.user_name=data["user"]["username"]+"#"+data["user"]["discriminator"]
            self.token=data["token"]
            self.id=data["id"]
            self.type=data["type"]

            self.interact=interactions.responses(self.token, self.id, self.type, inte, data['channel_id'])

            self.raw=data
            self.dpy=dpy

            if data["type"]==3: # Button or select menu
                self.message_data=data["message"]
                self.custom_id=data["data"]["custom_id"]
                # cidd=data["data"]["custom_id"].split("-")
                #if not "=" in cidd[1]:
                #    self.custom_id=cidd[0]
                #    self.custom_state=cidd[1]
                #else:
                #    cidd1=cidd[1].split("=")
                #    self.custom_id=cidd[0]
                #    self.val=cidd1[1]
                #    self.custom_state=cidd1[0]

            if data["type"]==2: # Commands
                self.name=data["data"]["name"]

            if data["type"]==5: # Modals
                if not "-" in data["data"]["custom_id"]: data["data"]["custom_id"]="none-"+data["data"]["custom_id"]
                cidd=data["data"]["custom_id"].split("-")
                if not "=" in cidd[1]:
                    self.custom_id=cidd[0]
                    self.custom_state=cidd[1]
                else:
                    cidd1=cidd[1].split("=")
                    self.custom_id=cidd[0]
                    self.val=cidd1[1]
                    self.custom_state=cidd1[0]

                compo=data["data"]["components"]
                d={}
                d1=[]
                for x in compo:
                    y=x["components"][0]
                    d[y['custom_id']]=y["value"]
                    d1.append({"id": y['custom_id'], "value": y["value"], "type": y["type"]})

                self.response=d
                self.response_data=d1
            
            
    class responses:
        def __init__(self, t, i, ty, inte, chan):
            self.i=i
            self.t=t
            self.ty=ty
            self.initeraction=inte
            self.channel=chan
            #self.reply=self.reply()
            #if ty == 3:
            #    self.edit=self.edit()

        def load(self, f=64, t=5):
            return self.initeraction.make_response({}, f, self.t, self.i, t)

        def edit_response(self, content, hidden=False, comp={}):
            if hidden==True: flags=64
            else: flags=0
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            return self.initeraction.edit_response(content, flags, self.t, self.i)

        def reply(self, content, hidden=False, comp={}):
            if hidden==True: flags=64
            else: flags=0
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            return self.initeraction.make_response(content, flags, self.t, self.i)
        def edit(self, content, comp=[]):
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            else:content["components"]=comp
            return self.initeraction.make_response(content, 0, self.t, self.i, 7)

        def delete(self):return self.initeraction.delete_response(self.t)

        def send_message(self, content, comp=[]):
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            return self.initeraction.send_message(content, self.channel)

        def webhook_send(self, content, comp=[]):
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            return self.initeraction.webhook_send(content, self.t)
        def webhook_edit(self, content, mid, comp=[]):
            if type(content)==message.embed: content=content.data
            if type(content)==str: content={"content": content}
            if type(comp)==message.components.action_row: content["components"]=comp.data
            return self.initeraction.webhook_edit(content, self.t, mid)

        def webhook_delete(self, mid):return self.initeraction.webhook_delete(self.t, mid)
        def dm_user(self, user_id, content, comp={}):return self.initeraction.dm_user(user_id, content, comp)

        def create_modal(self, data): return self.initeraction.make_modal(self.i, self.t,data.data)

