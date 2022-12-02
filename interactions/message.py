

class embed:
    def __init__(self, title="", description="", color=0):
        self.data={"embeds":[{"title": title, "description": description, "color": color}]}

class components:
    def __init__(self):
        self.data={}
    class action_row:
        def __init__(self, buttons, s=True):
            childeren=[]
            for x in buttons:
                childeren.append(x.data)
            if s==True:
                self.data=[{"type":1, "components": childeren}]
            else: self.data={"type":1, "components": childeren}
    class button:
        def __init__(self, style, label, emoji, custom_id, disabled=False, link=""):
            self.data={"type": 2, "style": style, "label": label, "emoji": emoji.data, "custom_id": custom_id, "disabled": disabled, "url": link}
    class emoji:
        def __init__(self, emoji):
            if emoji==None:
                self.data={}
            elif emoji.startswith("<:"):
                e=emoji.replace("<:", "").replace(">","").split(":")
                self.name=e[0]
                self.id=e[1]
                self.animated=False
                self.data={"name": self.name, "id": self.id, "animated": self.animated}
            elif emoji.startswith("<a:"):
                e=emoji.replace("<a:", "").replace(">","").split(":")
                self.name=e[0]
                self.id=e[1]
                self.animated=True
                self.data={"name": self.name, "id": self.id, "animated": self.animated}
            else:
                self.data={"name": emoji, "id": None, "animated": False}

    class select:
        def __init__(self, placeholder, custom_id, op, disabled=False, min=1, max=1):
            options=[]
            for x in op: options.append(x.data)
            self.data={"type": 3, "placeholder": placeholder, "custom_id": custom_id, "disabled": disabled, "min_values": min, "max_values": max, "options": options}

    class select_option:
        def __init__(self, label, value, description, emoji=None, defualt=False):
            if emoji!=None: e=emoji.data
            else: e=None
            self.data={"label": label, "value": value, "description": description, "emoji": e, "defualt": defualt}

    class modal:
        def __init__(self, custom_id, title, comp):
            c=[]
            for x in comp: 
                if type(x)==components.modal.text:c.append(x.data)
                elif type(x)==components.select:c.append(x.data)
                else: c.append(x)

            self.data={"title": title, "custom_id": custom_id, "components": c}
        class text:
            def __init__(self, custom_id, label,placeholder,required=True,style=1, min_length=0, max_length=200, value=""):
                # Type 4 for texts
                self.data={"type":1, "components":[{"type": 4,"required":required, "custom_id": custom_id, "style": style, "label": label, "placeholder": placeholder, "min_length": min_length, "max_length": max_length, "value": value}]}

class response:
    class autocomplete:
        def __init__(self):
            self.data=[]
        def add_option(self, name, value):self.data.append({"name": name, "value": value})











