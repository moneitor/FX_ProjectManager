# Example given to my by Andy Nicholas from Framestore

node_ptg = node.parmTemplateGroup()

# If it's originating from a subnet node, delete the subnet labels
# (if they exist. Not all subnets have them.)
for i in xrange(4):
    label_parm_name = "label" + str(i + 1)

    # Check the label parameter exists
    if node.parm(label_parm_name) is not None:
        node_ptg.remove(label_parm_name)

# ----------------------------------------------------
# Add code to make your OTL here
# ----------------------------------------------------

# Add the spare parameters into the new OTL's definition
otl_node.type().definition().setParmTemplateGroup(node_ptg)
