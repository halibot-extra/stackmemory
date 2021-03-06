from halibot import HalModule


class StackMemory(HalModule):

	def init(self):

		self.memory = {}
		self.stm = ""


	def receive(self, msg):
		ls = msg.body.split(" ",1)
		cmd = ls[0]
		args = ls[1] if len(ls) == 2 else ""
		if cmd == "!mem":
			args = args.split(" ",1)
			if args[0] == "push":
				self.remember(msg, args[1])
			elif args[0] == "pop":
				self.forget(msg)
			elif args[0] == "repush":
				self.remember(msg, self.stm)


	def remember(self, msg, string):
		if not string:
			return
		if msg.author in self.memory.keys():
			self.memory[msg.author].append(string)
		else:
			self.memory[msg.author] = [string]
		c = len(self.memory[msg.author])
		self.reply(msg, body="You have {} memor{}".format(c, ("y","ies")[not not c-1]))

	def forget(self, msg):
		rep = self.memory.get(msg.author, None)
		if rep and len(rep):
			num = len(rep)
			self.stm = rep.pop(-1)
			self.reply(msg, body="Recalling memory {}: {}".format(num, self.stm))
		else:
			self.reply(msg, body="Alas, you have no memories")
