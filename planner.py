from tkinter import *
import os
import datetime


class Urnik():
	def __init__(self, master):
		self.master = master
		self.danes = datetime.datetime.today().weekday() #današnji dan od 0 do 6
		self.vceraj = (self.danes - 1) % 7
		
		menu = Menu(self.master)
		master.config(menu=menu)
		
		current_points = "0 T"    # nekje se morajo poračunati te točke
		possible_points = "0 T"   # nekje se morajo poračunati te točke
		
		file_menu = Menu(menu)
		menu.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Home", command=self.home)
		file_menu.add_separator()
		file_menu.add_command(label="Quit", command=self.master.destroy)
		
		options_menu = Menu(menu)
		menu.add_cascade(label="Options", menu=options_menu)
		options_menu.add_command(label="Vnesi nov urnik", command=self.set_urnik)
		options_menu.add_command(label="Poglej moj urnik", command=self.print_urnik)
		options_menu.add_command(label="Poglej napredek", command=self.check_progress)
		options_menu.add_command(label="DANAŠNJE DELO", command=self.daily_task)
		
		self.new_frame()

		Label(self.main, text="Preostale obveznosti: "+possible_points).grid(row=0, column=0)
		Label(self.main, text="Vaše točke: "+current_points).grid(row=0, column=1)
		Button(self.main, text="Shrani", command=self.save_changes).grid(row=0, column=2)
		Label(self.main, text="VČERAJ").grid(row=1, column=0)
		Label(self.main, text="DANES").grid(row=1, column=1)
		Label(self.main, text="JUTRI").grid(row=1, column=2)
		Label(self.main, text="tukaj pridejo obveznosti").grid(row=2, column=0)
		Label(self.main, text="tukaj pridejo obveznosti").grid(row=2, column=1)
		Label(self.main, text="tukaj pride urnik").grid(row=2, column=2)
		
	def set_urnik(self):
		self.new_frame()
		self.urnik_entry = [[[None, StringVar(self.master), None] for i in range(13)] for i in range(7)]
		self.predmeti_check = []
		self.predmeti = [None] #seznam predmetov, ki se prikaže v OptionMenu-ju

		
		def izberi_predmet(i=0):
			if i > 0:
				self.gumb_plus.destroy()
				self.gumb_naprej.destroy()
			Label(self.main, text="Vnesi predmet:").grid(row=i, column=0)
			self.predmeti_check.append(Entry(self.main))
			self.predmeti_check[i].grid(row=i, column=1)
			self.gumb_plus = Button(self.main, text="+", command=lambda:izberi_predmet(i+1))
			self.gumb_plus.grid(row=i, column=2)
			self.gumb_naprej = Button(self.main, text="Naprej", command=self.enter_urnik)
			self.gumb_naprej.grid(row=i+1, column=2)
	
		izberi_predmet()	
		
	def enter_urnik(self):
		teden = ["PON", "TOR", "SRE", "ČET", "PET", "SOB", "NED"]
		if self.predmeti == [None]:
			for i in range(len(self.predmeti_check)):
				tmp = self.predmeti_check[i].get()
				if tmp != "":
					self.predmeti.append(tmp)
			
		self.new_frame()
		for i in range(len(teden)):
			Label(self.main, text=teden[i]).grid(row=0, column=i+1)
		for i in range(0, 13):
			Label(self.main, text="{}.00 ".format(7+i)).grid(row=i+1, column=0, sticky="e")
			for j in range(7):
				self.urnik_entry[j][i][0] = OptionMenu(self.main, self.urnik_entry[j][i][1], *self.predmeti)
				self.urnik_entry[j][i][0].grid(row=i+1, column=j+1)
				
		self.master.bind("<Return>", self.preberi_urnik)	
		
	def preberi_urnik(self, event):
		check_days = [0 for i in range(7)]
		for i in range(0,13):
			for j in range(7):
				self.urnik_entry[j][i][2] = self.urnik_entry[j][i][1].get()
				if self.urnik_entry[j][i][2] != "" and j < 5:
					check_days[j] = 1
					
		self.new_frame()
		if sum(check_days) < 5:
			teden = ["PON", "TOR", "SRE", "ČET", "PET"]
			self.prosti_dnevi = []
			for i in range(5):
				if check_days[i] == 0:
					self.prosti_dnevi.append(teden[i])
			string = "Si prepričan, da imaš prosto v "
			for i in range(len(self.prosti_dnevi)):
				if i+1 == len(self.prosti_dnevi):
					string += self.prosti_dnevi[i] + '?'
				else:
					string += self.prosti_dnevi[i] + ', '
			Label(self.main, text=string).grid(row=0, column=0)
			Button(self.main, text="Da", command=self.save_urnik).grid(row=1, column=1)
			Button(self.main, text="Ne", command=self.enter_urnik).grid(row=1, column=2)
		else:
			self.save_urnik()
		
	def save_urnik(self):
		#Shrani urnik v datoteko.
		try:
			os.remove("urnik.txt")
		except: pass
		urnik = open("urnik.txt", 'w')
		
		for i in range(13):
			string = ""
			for j in range(7):
				if j < 6:
					if self.urnik_entry[j][i][2] == None or self.urnik_entry[j][i][2] == "":
						string += ","
					else:
						string += self.urnik_entry[j][i][2] + ","
				else:
					if self.urnik_entry[j][i][2] == None or self.urnik_entry[j][i][2] == "":
						pass
					else:
						string += self.urnik_entry[j][i][2]
			string += "\n"
			urnik.write(string)
		urnik.close()
		
		self.new_frame()
		Label(self.main, text="Vaš urnik je bil uspešno shranjen :).").grid(column=0)
		Button(self.main, text="Domov", command=self.home).grid(column=1)
					
	
	def get_urnik(self):
		urnik = open("urnik.txt", 'r')
		self.real_urnik = [[],[],[],[],[],[],[]]
		for vrstica in urnik:
			pon,tor,sre,cet,pet,sob,ned = vrstica.split(",")
			self.real_urnik[0].append(pon)
			self.real_urnik[1].append(tor)
			self.real_urnik[2].append(sre)
			self.real_urnik[3].append(cet)
			self.real_urnik[4].append(pet)
			self.real_urnik[5].append(sob)
			self.real_urnik[6].append(ned.strip())
		urnik.close()
		print(self.real_urnik)
				
		
	def print_urnik(self):
		self.new_frame()
		Label(self.main, text="To je urnik.").grid(row=0, column=0)
		print("Printing...")
		
	def check_progress(self):
		print("Checking progress...")
		
	def daily_task(self):
		self.new_frame()
		Label(self.main, text=str(self.real_urnik[self.danes])).grid(row=0, column=0)
		print("Daily task...")
		
	def home(self):
		self.main.destroy()
		self.__init__(self.master)
		
	def new_frame(self):
		try:
			self.main.destroy()
		except:
			pass
		finally:
			self.main = Frame()
			self.main.grid()
	def save_changes(self):
		print("Saving...")
	
		
root = Tk()
root.title("Ultimate Planner Beta")

app = Urnik(root)

root.mainloop()		
