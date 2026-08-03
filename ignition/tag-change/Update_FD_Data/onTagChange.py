def onTagChange(initialChange, newValue, previousValue, event, executionCount):
	
	try:
		basePath = "[default]sander_falldown/falldown"
		fdDataPath = "{}/FD_Data".format(basePath)
		classNames = ["ClassA", "ClassB", "ClassC", "ClassD", "ClassE"]

		loginTimePath = "{}/product/product_start_time".format(basePath)
		loginTime = system.tag.readBlocking([loginTimePath])[0].value

		if loginTime is not None:
			browseResults = system.tag.browse(fdDataPath)

			for item in browseResults.getResults():
				pointer = item["name"]

				for className in classNames:
					descPath = "{}/{}/Description".format(fdDataPath, pointer)
					docPath = "{}/{}/{}.Documentation".format(fdDataPath, pointer, className)
					resultPath = "{}/{}/Result{}".format(fdDataPath, pointer, className[-1])

					values = system.tag.readBlocking([descPath, docPath])
					desc = values[0].value
					doc = values[1].value

					if desc is None or doc is None:
						continue

					results = system.db.runNamedQuery(
						"falldown/2A",
						{
							"description": desc,
							"documentation": doc,
							"loginTime": loginTime
						}
					)

					count = results.getValueAt(0, "2A_Count") if results.getRowCount() > 0 else 0

					system.tag.writeBlocking([resultPath], [count])

	except Exception as e:
		system.util.getLogger("TagEvent").error(
			"Error in tag event script: {}".format(e)
		)