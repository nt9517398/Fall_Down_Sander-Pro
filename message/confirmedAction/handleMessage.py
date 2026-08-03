def handleMessage(session, payload):
	
    # Execute the action when the user confirms
    system.perspective.print("User confirmed the action!")

    # (Optional) Add the actual action here
    # Example: system.db.runNamedQuery("myQuery")	