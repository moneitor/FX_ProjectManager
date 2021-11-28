	def copy_parameters(node1, node2):
		node1_parms = node1.parms()
		node2_parms = node2.parms()

		for parm in node1_parms:
			for old_parm in node2_parms:
				if parm.name() == old_parm.name():
					if parm.name() != "near" and parm.name() != "far":
						parm.set(old_parm)
						print (parm.name(), old_parm.name())
