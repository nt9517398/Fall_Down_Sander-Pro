def onTagChange(initialChange, newValue, previousValue, event, executionCount):
	

	logger = system.util.getLogger("HitachiUX2")

	if not initialChange:

		messageTagPath = "[default]Hitachi_UX2/_L15_GradeInfoToPrinter"

		messageTag = system.tag.readBlocking(
			[messageTagPath]
		)[0]

		if not messageTag.quality.isGood():

			logger.error(
				"Could not read _L15_GradeInfoToPrinter. Quality: %s"
				% str(messageTag.quality)
			)

		else:

			try:
				messageNumber = int(messageTag.value)

				if messageNumber not in [1, 2, 3, 4]:

					logger.warn(
						"_L15_GradeInfoToPrinter must be 1, 2, 3 or 4. "
						"Current value: %s"
						% str(messageNumber)
					)

				else:

					line1Path = (
						"[default]Hitachi_UX2/message%s/line1"
						% messageNumber
					)

					line2Path = (
						"[default]Hitachi_UX2/message%s/line2"
						% messageNumber
					)

					lineValues = system.tag.readBlocking(
						[
							line1Path,
							line2Path
						]
					)

					line1 = str(lineValues[0].value)
					line2 = str(lineValues[1].value)

					result = hitachi_ux2.write_message_from_tags(
						messageNumber
					)

					if result is None:

						logger.error(
							"No result returned when sending message %s."
							% str(messageNumber)
						)

					elif result.get("success"):

						logger.info(
							"Message %s loaded into the Hitachi UX2. "
							"Line 1: %s | Line 2: %s"
							% (
								str(messageNumber),
								line1,
								line2
							)
						)

					else:

						logger.error(
							"Failed to load message %s into the Hitachi UX2. "
							"Line 1: %s | Line 2: %s | Result: %s"
							% (
								str(messageNumber),
								line1,
								line2,
								str(result)
							)
						)

			except Exception as error:

				logger.error(
					"Unable to process _L15_GradeInfoToPrinter value %s. "
					"Error: %s"
					% (
						str(messageTag.value),
						str(error)
					)
				)