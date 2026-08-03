def handleTimerEvent():
	import system
	logger = system.util.getLogger("GraderMonitor")
	
	# Config
	TARGET_IP = "10.55.25.23"   # 👈 Grading PC’s IP
	PROJECT_NAME = "Falldown_Sander"
	GLOBAL_TAG = "[default]sander_falldown/falldown/product/grader"
	
	try:
	    # Pull ALL sessions (no project filter for now)
	    sessions = system.perspective.getSessionInfo()
	    logger.info("Found %d sessions total" % len(sessions))
	
	    grader_user = None
	    for s in sessions:
	        proj = s.get("project")
	        ip   = s.get("clientAddress")
	        user = s.get("username")
	
	        # Log what we see
	        logger.info("Session check: project=%s, ip=%s, user=%s" % (proj, ip, user))
	
	        # Match both project + target IP
	        if proj == PROJECT_NAME and ip == TARGET_IP:
	            grader_user = user
	            break
	
	    if grader_user and grader_user != "Unauthenticated":
	        system.tag.writeBlocking([GLOBAL_TAG], [grader_user])
	        logger.info("Global grader updated to '%s' (IP=%s)" % (grader_user, TARGET_IP))
	    else:
	        system.tag.writeBlocking([GLOBAL_TAG], [None])
	        logger.info("Global grader reset to null (no valid session for IP=%s)" % TARGET_IP)
	
	except Exception as e:
	    logger.error("Error in GraderMonitor script: %s" % e)