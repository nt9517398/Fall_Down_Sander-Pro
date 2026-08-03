def handleMessage(session, payload):
	try:
    		for page in self.session.pages.values():
        # Blue-highlighted Label_0 (with extra FlexContainer_1 in the path)
        		label = page.getChild("C/root/FlexContainer/FlexContainer_1/FlexContainer_0/FlexContainer_10/FlexContainer_11/Label_0")
        		label.refreshBinding("props.text")

	except Exception as e:
    		system.util.getLogger("SessionMessage").warn("Could not refresh label: {}".format(e))