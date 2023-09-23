ZOOM = 3

class Translator():
    def __init__(self):
        self.variables = {}
        self.console = None
        self.character = None
        self.reps = []
        self.ifs = []

    def execute_npc(self, npc):
        inst = 1
        current_code = [npc.code]
        while True:
            if npc.read_stage[inst] >= len(current_code[-1]):
                if inst == 1:
                    return True
                if npc.read_stage[inst]:
                    a = current_code[-2][npc.read_stage[inst-1]][0][0](*current_code[-2][npc.read_stage[inst-1]][0][1:],
                                                            stage=npc.read_stage[inst])
                else:
                    a = True
                if a:
                    npc.read_stage = npc.read_stage[:-1]
                    npc.read_stage[-1] += 1
                    current_code = current_code[:-1]
                    inst -= 1
                    if npc.read_stage[1] == len(npc.code):
                        return True
                else:
                    npc.read_stage[inst] = 0
                    npc.read_stage[0] = 0
                continue
            if current_code[-1][npc.read_stage[inst]][1] == None:
                current_code.append(current_code[-1][npc.read_stage[inst]][0][0](*current_code[-1][npc.read_stage[inst]][0][1:],
                                                                      stage=0))
                inst += 1
                if len(npc.read_stage) == inst:
                    npc.read_stage.append(0)
                    if current_code[-2][npc.read_stage[inst]][0][0] == self.repeter:
                        self.reps.append(0)
                    elif current_code[-2][npc.read_stage[inst]][0][0] == self.si_sinon:
                        self.ifs.append(current_code[-1][npc.read_stage[inst]][0][0](*current_code[-1][npc.read_stage[inst]][0][1:],
                                                                                     stage=-1))
                    elif current_code[-2][npc.read_stage[inst]][0][0] == self.tant_que:
                        a = current_code[-1][npc.read_stage[inst]][0][0](*current_code[-1][npc.read_stage[inst]][0][1:],
                                                                         stage=1)
                        if a:
                            npc.read_stage[inst] = len(current_code[-1])
                continue
            elif current_code[-1][npc.read_stage[inst]][1] == 0:
                current_code[-1][npc.read_stage[inst]][0][0](*current_code[-1][npc.read_stage[inst]][0][1:])
            elif current_code[-1][npc.read_stage[inst]][1] > npc.read_stage[0]:
                current_code[-1][npc.read_stage[inst]][0][0](*current_code[-1][npc.read_stage[inst]][0][1:])
                npc.read_stage[0] += 1
                return False
            elif current_code[-1][npc.read_stage[inst]][1] == npc.read_stage[0]:
                npc.read_stage[0] = 0
            npc.read_stage[inst] += 1
            

    def log(self, text, end_line=True):
        self.console.log_console(str(text), end_line=end_line)

    def bouger(self, command):
        command()

    def creer_var(self, nom, valeur):
        """Crée une variable entière"""
        self.variables[nom] = valeur

    def translate(self, string, only_var=False):
        for var in self.variables:
            string = string.replace(var, f"self.variables[\"{var}\"]")
        if not only_var:
            string = string.replace("^", "**")
        return string

    def operation_simple(self, nom_var, operation):
        """Effectue un calcul et l'assigne à une variable donnée"""
        if operation == "":
            return "Il manque un calcul pour le bloc Affecter"
        try:
            operation = self.translate(operation)
            eval(operation)
        except:
            return f"Calcul invalide: {operation}"
        if nom_var not in self.variables:
            return f"La variable {nom_var} n'existe pas!"
        self.variables[nom_var] = eval(operation)
        self.variables[nom_var] = self.entier_si_possible(float(self.variables[nom_var]))

    def repeter(self, times, trucs_a_rep, stage=None):
        """Répète une suite d'instructions un certain nombre de fois"""
        if stage == None:
            for i in range(times):
                for instruction in trucs_a_rep:
                    if instruction[1] in (0, None):
                        instruction[0][0](*instruction[0][1:])
        elif stage == 0:
            return trucs_a_rep
        elif self.reps[-1] == times - 1:
            self.reps = self.reps[:-1]
            return True
        else:
            self.reps[-1] += 1
            

    def tant_que(self, cond, trucs_a_rep, stage=None):
        """Répète une suite d'instructions tant qu'une certaine condition
        est vérifiée"""
        if stage == None:
            try:
                cond = self.lire_condition(cond)
                while eval(cond):
                    for instruction in trucs_a_rep:
                        if instruction[1] in (0, None):
                            instruction[0][0](*instruction[0][1:])
            except:
                return "Condition invalide pour la boucle tant que!"
        else:
            cond = self.lire_condition(cond)
            if stage == 0:
                return trucs_a_rep
            elif not eval(cond):
                return True

    def si_sinon(self, cond, inst_si, inst_sinon, stage=None):
        """Reproduit un bloc "Si Sinon" """
        if stage == None:
            try:
                cond = self.lire_condition(cond)
                if eval(cond):
                    for instruction in inst_si:
                        if instruction[1] in (0, None):
                            instruction[0][0](*instruction[0][1:])
                else:
                    for instruction in inst_sinon:
                        if instruction[1] in (0, None):
                            instruction[0][0](*instruction[0][1:])
            except:
                return "Condition invalide pour le si!"
        else:
            cond = self.lire_condition(cond)
            if stage == 0:
                if eval(cond):
                    return inst_si
                else:
                    return inst_sinon
            elif stage == -1:
                if eval(cond):
                    return True
                else:
                    return False
            else:
                return True

    def afficher(self, affichage):
        """Affiche des variables dans le terminal"""
        try:
            affichage = affichage.split(",")
            for i in range(len(affichage)):
                if not (affichage[i].startswith("\"") or\
                affichage[i].startswith("\'")):
                    affichage[i] = self.translate(affichage[i])
            for elem_to_log in affichage[:-1]:
                eval("self.log(" + elem_to_log + ", False)")
            eval("self.log(" + affichage[-1] + ")")
        except:
            return "Element(s) à afficher incorrect(s) (pensez à mettre des virgules"\
                "pour séparer les éléments et des guillemets s'ils sont du texte)"
        
            
        

    def entier_si_possible(self, float_nb):
        """Transforme un flottant en entier si ce dernier est un entier"""
        if float_nb.is_integer():
            float_nb = int(float_nb)
        return float_nb

    def lire_condition(self, cond):
        cond = cond.replace("est égal à", "==")
        cond = cond.replace("est différent de", "!=")
        cond = cond.replace("est supérieur ou égal à", ">=")
        cond = cond.replace("est inférieur ou égal à", "<=")
        cond = cond.replace("est strictement supérieur à", ">")
        cond = cond.replace("est strictement inférieur à", "<")
        cond = cond.replace("ou", "or")
        cond = cond.replace("et", "and")
        for var in self.variables:
            cond = cond.replace(var, f"self.variables['{var}']")
        return cond

    def interpreter(self, instruction, block, index=None):
        instruction = instruction.split()
        if instruction[0] == "Créer":
            nom_var = block.inputs[0].text[:-1]
            if nom_var == "":
                return "Il manque un nom pour votre variable!"
            val_var = block.inputs[1].text[:-1]
            if val_var == "":
                return f"Il manque une valeur à la variable {nom_var}"
            try:
                val_var = float(val_var)
                val_var = self.entier_si_possible(val_var)
            except:
                return f"Valeur incorrecte pour la variable {nom_var} (doit être un réel)"
            return (self.creer_var, nom_var, val_var), 0
        elif instruction[0] == "Affecter":
            calcul = block.inputs[0].text[:-1]
            nom_var = block.inputs[1].text[:-1]
            if nom_var == "":
                return f"Il manque une variable à laquelle assigner l'opération {calcul}!"
            return (self.operation_simple, nom_var, calcul), 0
        elif instruction[0] == "Afficher":
            trucs_a_aff = block.input.text[:-1]
            return (self.afficher, trucs_a_aff), 0
        elif instruction[0] == "Répéter":
            try:
                boucle, times = [], int(block.input.text[:-1])
            except:
                return "Nomble invalide de répétions (pas un réel ou inexistant)"
            for block_bis in block.rep_code:
                temp = self.interpreter(block_bis.inst, block_bis)
                if isinstance(temp, str):
                    return temp
                command, frames = temp
                boucle.append((command, frames))
            return (self.repeter, times, boucle), None
        elif instruction[0] == "Tant":
            if len(block.rep_code) == 0 or "Condition" not in block.rep_code[0].inst:
                return "Il manque une condition pour la boucle tant que!"
            boucle, cond = [], block.rep_code[0].input.text[:-1]
            for block_bis in block.rep_code[1:]:
                temp = self.interpreter(block_bis.inst, block_bis)
                if isinstance(temp, str):
                    return temp
                command, frames = temp
                boucle.append((command, frames))
            return (self.tant_que, cond, boucle), None
        elif instruction[0] == "Si:":
            if len(block.if_code) == 0 or "Condition" not in block.if_code[0].inst:
                return "Il manque une condition pour le si!"
            cond = block.if_code[0].input.text[:-1]
            inst_si, inst_sinon = [], []
            for block_bis in block.if_code[1:]:
                temp = self.interpreter(block_bis.inst, block_bis)
                if isinstance(temp, str):
                    return temp
                command, frames = temp
                inst_si.append((command, frames))
            if "Sinon" in block.inst:
                for block_bis in block.else_code:
                    temp = self.interpreter(block_bis.inst, block_bis)
                    if isinstance(temp, str):
                        return temp
                    command, frames = temp
                    inst_sinon.append((command, frames))
            return (self.si_sinon, cond, inst_si, inst_sinon), None
        elif instruction[0] == "Condition:":
            return "Les conditions ne sont pas des blocs d'instruction"
        elif instruction[0] == "Bouger":
            if "gauche" in instruction:
                command = self.character.move_left
            elif "droite" in instruction:
                command = self.character.move_right
            elif "bas" in instruction:
                command = self.character.move_down
            elif "haut" in instruction:
                command = self.character.move_up
            try:
                frames = 18*ZOOM*int(block.input.text[:-1])
            except:
                return "Le nombre de blocs doit être entiers naturel!"
            return (self.bouger, command), frames
            
    def lire_instructions(self, instructions, console_, Character = None):
        self.character = Character
        self.variables, self.console = {}, console_
        instructions_bis = []
        for i in range(len(instructions)):
            instructions_bis.append((instructions[i].inst, instructions[i]))
        i = 0
        fonctions = []
        for i in range(len(instructions)):
            details = self.interpreter(instructions_bis[i][0], instructions_bis[i][1])
            if isinstance(details, str):
                self.log(details)
                return None
            fonctions.append(details)
        return fonctions

    def executer(self, fonctions):
        for fonction in fonctions:
            if fonction[1] in (0, None):
                temp = fonction[0][0](*fonction[0][1:])
                if isinstance(temp, str):
                    self.log(temp)
                    return "Erreur"