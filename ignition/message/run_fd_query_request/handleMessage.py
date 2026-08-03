def handleMessage(payload):
	
    """
    Gateway Message Handler triggered by Perspective sendRequest.
    'payload' contains all parameters.
    """
    params = payload

    # Call the Script Library function
    LabelUpdate.run_fd_query.run_fd_query(params)