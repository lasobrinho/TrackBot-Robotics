import machine
import time

class Stepper:

	def __init__(self, numberOfSteps, pins):
		self.pin1 = machine.Pin(pins[0], machine.Pin.OUT)
		self.pin2 = machine.Pin(pins[1], machine.Pin.OUT)
		self.pin3 = machine.Pin(pins[2], machine.Pin.OUT)
		self.pin4 = machine.Pin(pins[3], machine.Pin.OUT)
		self.stepNumber = 0
		self.direction = 0
		self.numberOfSteps = numberOfSteps
		self.stepDelay = 0

	def setSpeed(self, newSpeed):
		self.stepDelay = 60.0 / self.numberOfSteps / newSpeed

	def stepMotor(self, thisStep):
		if thisStep == 0:
			self.pin1.on()
			self.pin2.off()
			self.pin3.off()
			self.pin4.on()
		if thisStep == 1:
			self.pin1.off()
			self.pin2.on()
			self.pin3.off()
			self.pin4.on()
		if thisStep == 2:
			self.pin1.off()
			self.pin2.on()
			self.pin3.on()
			self.pin4.off()
		if thisStep == 3:
			self.pin1.on()
			self.pin2.off()
			self.pin3.on()
			self.pin4.off()

	def step(self, stepsToMove):
		stepsLeft = abs(stepsToMove)

		if stepsToMove > 0:
			self.direction = 1
		if stepsToMove < 0:
			self.direction = 0

		while stepsLeft > 0:
			if self.direction == 1:
				self.stepNumber += 1
				if self.stepNumber == self.numberOfSteps:
					self.stepNumber = 0
			else:
				if self.stepNumber == 0:
					self.stepNumber = self.numberOfSteps
				self.stepNumber -= 1
			stepsLeft -= 1

			self.stepMotor(self.stepNumber % 4)
			time.sleep(self.stepDelay)

