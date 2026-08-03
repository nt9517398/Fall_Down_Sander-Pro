def onStartup(session):
	
    userObj = session.props.auth.user
    username = getattr(userObj, "userName", None) if userObj else None
    if username:
        system.tag.writeAsync(
            ["[default]sander_falldown/falldown/product/grader"],
            [username]
        )