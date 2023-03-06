from flet import *
import bluetooth
import subprocess

# YOU MUST INSTALL obexftp with command apt install obexftp 

def main(page:Page):
	nearby_devices = bluetooth.discover_devices()
	result_scan = Text(value="",weight="bold")
	filename = TextField(label="you file here")
	device_mac = TextField(label="you device mac address here")


	# AND FIND DEVICE NEARBY YOU 
	def find_devices():
		for i , addr in enumerate(nearby_devices):
			name = bluetooth.lookup_name(addr)
			# AND I PRINT DEVICES FOUND NEAR YOU
			print("%d. %s(%s) "  % (i+1,name,addr))
			result_scan.value += "%d. %s(%s)\n "  % (i+1,name,addr)

	find_devices()


	def sendfilenow(e):
		device_number = int(device_mac.value)
		addr = nearby_devices[device_number-1]
		try:
			result = subprocess.run(["bt-obex","-p",addr,filename.value],capture_output=True)
			if result.returncode == 0:
				# IF SUCCESS THEN SHOW SNACKBAR SUCCESS
				print("you file succes send !!!")
				page.snack_bar = SnackBar(
				Text("Success send Guys !!",size=30),
				bgcolor="blue"

					)
				page.snack_bar.open = True
				page.update()
			else:
				print("Failed to send !!!")
		except FileNotFoundError:
			print("Commnad bt-obex is not found GUYS !!")

		

	page.add(
	Column([
	Text("Choices Decvices",weight="bold"),
	result_scan,
	filename,
	device_mac,
	ElevatedButton("send File now",
		bgcolor="blue",color="white",
		on_click=sendfilenow

		)

		])
		)


flet.app(target=main)
	