from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog, colorchooser, ttk, messagebox
import sqlite3

root = Tk()
root.title("MSFPA Helper - Database Manager")
root.iconbitmap('images/Database_Manager_Icon.ico')
root.geometry("525x375")

#Database
conn = sqlite3.connect('character_list.db')
c = conn.cursor()

'''
c.execute("""CREATE TABLE characters (
		id integer PRIMARY KEY AUTOINCREMENT,
		name text,
		tag text,
		userName text,
		initials text,
		removeQuirk text,
		replaceQuirk text,
		removeWord text,
		replaceWord text,
		caps text,
		capsSen integer,
		gamzeeQuirk integer,
		tavrosQuirk integer,
		prefix text,
		sufix text,
		color text,
		char_group text
	)""")
'''
'''
c.execute("SELECT *,oid FROM characters")
records = c.fetchall()
print(records)
'''

#functions
def color():
	global chaColor
	chaColor = "#fff"
	chaColor = colorchooser.askcolor()[1]

	color_button = Button(insert_frame, width=15, text=chaColor, bg=chaColor, command=color)
	color_button.grid(row=3, column=1)



def u_color():
	global u_chaColor
	u_chaColor = colorchooser.askcolor()[1]

	m_color_button = Button(update_frame_label, width=15, text=u_chaColor, bg=u_chaColor, command=u_color)
	m_color_button.grid(row=4, column=1)

def show_characters():
	sc_window = Toplevel()
	sc_window.title("Character List")
	sc_window.iconbitmap('images/Database_Manager_Icon.ico')
	sc_window.geometry("500x600")

	main_frame = Frame(sc_window)
	main_frame.pack(fill=BOTH, expand=1)

	my_canvas = Canvas(main_frame)
	my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

	my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
	my_scrollbar.pack(side=RIGHT, fill=Y)

	my_canvas.configure(yscrollcommand=my_scrollbar.set)
	my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

	second_frame = Frame(my_canvas)

	my_canvas.create_window((0,0), window=second_frame, anchor='nw')

	#Query
	conn = sqlite3.connect('character_list.db')
	c = conn.cursor()

	c.execute("SELECT * FROM characters")
	records = c.fetchall()
	print(records)

	#Loop through records
	print_records = ''
	for record in records:
		print_records += "ID | " + "\t" + str(record[0]) + "\n" + "Name | " + "\t" + str(record[1]) + "\n" + "Tag | " + "\t" + str(record[2]) + "\n" + "Username | " + "\t" + str(record[3]) + "\n" + "Initials | " + "\t" + str(record[4]) + "\n" + "Remove Quirk | " + "\t" + str(record[5]) + "\n" + "Replace Quirk | " + "\t" + str(record[6]) + "\n" + "Remove Word | " + "\t" + str(record[7]) + "\n" + "Replace Word | " + "\t" + str(record[8]) + "\n" + "Capitalisation | " + "\t" + str(record[9]) + "\n" + "Caps Sensitive | " + "\t" + str(record[10]) + "\n" + "Gamzee Quirk | " + "\t" + str(record[11]) + "\n" + "Tavros Quirk | " + "\t" + str(record[12]) + "\n" + "Prefix | " + "\t" + str(record[13]) + "\n" + "Sufix | " + "\t" + str(record[14]) + "\n" + "Text Color | " + "\t" + str(record[15]) + "\n" + "Group | " + "\t" + str(record[16]) + "\n" + "--------------------" + "\n"

	records_label = Label(second_frame, text=print_records, justify=LEFT)
	records_label.pack(pady=5, padx=5)

	conn.commit()
	conn.close()

def popup():
	conn = sqlite3.connect('character_list.db')
	c = conn.cursor()

	if m_id.get() == "":
		messagebox.showwarning(title="Attention!", message="Search ID not defined!")
		return

	c.execute("SELECT * FROM characters WHERE id=" + m_id.get())
	records = c.fetchall()
	cr_message = "You want to delete: \n\n"
	for record in records:
		cr_message += "ID | " + "\t" + str(record[0]) + "\n" + "Name | " + "\t" + str(record[1]) + "\n" + "Tag | " + "\t" + str(record[2]) + "\n" + "Username | " + "\t" + str(record[3]) + "\n" + "Initials | " + "\t" + str(record[4]) + "\n" + "Remove Quirk | " + "\t" + str(record[5]) + "\n" + "Replace Quirk | " + "\t" + str(record[6]) + "\n" + "Remove Word | " + "\t" + str(record[7]) + "\n" + "Replace Word | " + "\t" + str(record[8]) + "\n" + "Capitalisation | " + "\t" + str(record[9]) + "\n" + "Caps Sensitive | " + "\t" + str(record[10]) + "\n" + "Gamzee Quirk | " + "\t" + str(record[11]) + "\n" + "Tavros Quirk | " + "\t" + str(record[12]) + "\n" + "Prefix | " + "\t" + str(record[13]) + "\n" + "Sufix | " + "\t" + str(record[14]) + "\n" + "Text Color | " + "\t" + str(record[15]) + "\n" + "Group | " + "\t" + str(record[16])

	response = messagebox.askyesno(title="Delete Character Entry", message=cr_message)


	if response == True:
		#Delete
		print(response)
		c.execute("DELETE from characters WHERE id=" + m_id.get())
		conn.commit()
		conn.close()
		m_window.destroy()
	else:
		#Don't Delete
		return

	conn.commit()
	conn.close()

def update():
	conn = sqlite3.connect('character_list.db')
	c = conn.cursor()

	c.execute("""UPDATE characters SET
		name = :name,
		tag = :tag,
		userName = :userName,
		initials = :initials,
		removeQuirk = :removeQuirk,
		replaceQuirk = :replaceQuirk,
		removeWord = :removeWord,
		replaceWord = :replaceWord,
		caps = :caps,
		capsSen = :capsSen,
		gamzeeQuirk = :gamzeeQuirk,
		tavrosQuirk = :tavrosQuirk,
		prefix = :prefix,
		sufix = :sufix,
		color = :color,
		char_group = :char_group

		WHERE id = :id""",
		{
		'id': u_id.get(),
		'name': m_name.get(),
		'tag': m_tag.get(),
		'userName': m_username.get(),
		'initials': m_initials.get(),
		'removeQuirk': m_removeQ.get(),
		'replaceQuirk': m_replaceQ.get(),
		'removeWord': m_removeW.get(),
		'replaceWord': m_replaceW.get(),
		'caps': m_caps.get(),
		'capsSen': m_caps_sensitivity_var.get(),
		'gamzeeQuirk': m_gamzee_Quirk_var.get(),
		'tavrosQuirk': m_tavros_Quirk_var.get(),
		'prefix': m_prefix.get(),
		'sufix': m_sufix.get(),
		'color': str(u_chaColor),
		'char_group': m_group.get()
		})

	print(u_chaColor)

	u_id.delete(0, END)
	m_name.delete(0, END)
	m_tag.delete(0, END)
	m_username.delete(0, END)
	m_initials.delete(0, END)
	m_removeQ.delete(0, END)
	m_replaceQ.delete(0, END)
	m_removeW.delete(0, END)
	m_replaceW.delete(0, END)
	m_caps.set(m_caps_options[0])
	m_caps_sensitivity.deselect()
	m_gamzee_Quirk.deselect()
	m_tavros_Quirk.deselect()
	m_prefix.delete(0, END)
	m_sufix.delete(0, END)
	m_group.delete(0, END)

	conn.commit()
	conn.close()

	m_window.destroy()

def modify():
	global m_window
	m_window = Toplevel()
	m_window.title("Modify Entry")
	m_window.iconbitmap('images/Database_Manager_Icon.ico')
	m_window.geometry("525x600")

	#Delete Entry
	delete_frame_label = LabelFrame(m_window, text="Delete Entry", padx=5, pady=5)
	delete_frame_label.grid(row=0, column=0, pady=10, padx=10)

	m_id_label = Label(delete_frame_label, text="ID: ")
	m_id_label.grid(row=0, column=0)

	global m_id	

	global u_id
	global m_name
	global m_tag
	global m_username
	global m_initials
	global m_group
	global m_removeQ
	global m_replaceQ
	global m_removeW
	global m_replaceW
	global m_caps
	global m_caps_sensitivity_var
	global m_gamzee_Quirk_var
	global m_tavros_Quirk_var
	global m_prefix
	global m_sufix

	global m_caps_sensitivity
	global m_gamzee_Quirk
	global m_tavros_Quirk

	global m_caps_options

	m_id = Entry(delete_frame_label, width=5)
	#m_id.insert(0, "")
	m_id.grid(row=0, column=1)

	m_delete_button = Button(delete_frame_label, text="Delete", command=popup)
	m_delete_button.grid(row=0, column=2, pady=10, padx=10)

	#Update Entry
	global update_frame_label
	update_frame_label = LabelFrame(m_window, text="Update Entry", padx=5, pady=5)
	update_frame_label.grid(row=1, column=0, pady=10, padx=10)

	#Insert Frame
	u_id_label = Label(update_frame_label, text="ID: ")
	u_id_label.grid(row=0, column=0)

	m_name_Label = Label(update_frame_label, text="Name: ")
	m_name_Label.grid(row=1, column=0)

	m_tag_label = Label(update_frame_label, text="Tag: ")
	m_tag_label.grid(row=2, column=0)

	m_username_label = Label(update_frame_label, text="User Name: ")
	m_username_label.grid(row=3, column=0)

	m_initials_labels = Label(update_frame_label, text="Initials: ")
	m_initials_labels.grid(row=3, column=2)

	m_chooseColor_label = Label(update_frame_label, text="Choose Color: ")
	m_chooseColor_label.grid(row=4, column=0)

	m_group_label = Label(update_frame_label, text="Group: ")
	m_group_label.grid(row=4, column=2)

	m_removeQ_label = Label(update_frame_label, text="Quirk - Remove: ")
	m_removeQ_label.grid(row=5, column=0)

	m_replaceQ_label = Label(update_frame_label, text="Quirk - Replace: ")
	m_replaceQ_label.grid(row=5, column=2)

	m_removeW_label = Label(update_frame_label, text="Word - Remove: ")
	m_removeW_label.grid(row=6, column=0)

	m_replaceW_label = Label(update_frame_label, text="Word - Replace: ")
	m_replaceW_label.grid(row=6, column=2)

	m_caps_options =[
		"No Capitalisation",
		"All Capitalisation",
		"Normal Capitalisation"
	]

	m_caps = StringVar()
	m_caps.set(m_caps_options[0])

	m_caps_dropdown = OptionMenu(update_frame_label, m_caps, *m_caps_options)
	m_caps_dropdown.grid(row=7, column=0, columnspan=5)

	m_caps_sensitivity_var = IntVar()
	m_caps_sensitivity = Checkbutton(update_frame_label, text="Quirk is Cap Sensitive", variable=m_caps_sensitivity_var, onvalue=1, offvalue=0)
	m_caps_sensitivity.grid(row=8, column=0)

	m_gamzee_Quirk_var = IntVar()
	m_gamzee_Quirk = Checkbutton(update_frame_label, text="Gamzee Quirk", variable=m_gamzee_Quirk_var, onvalue=1, offvalue=0)
	m_gamzee_Quirk.grid(row=8, column=1)

	m_tavros_Quirk_var = IntVar()
	m_tavros_Quirk = Checkbutton(update_frame_label, text="Tavros Quirk", variable=m_tavros_Quirk_var, onvalue=1, offvalue=0)
	m_tavros_Quirk.grid(row=8, column=2)

	m_prefix_label = Label(update_frame_label, text="Prefix: ")
	m_prefix_label.grid(row=9, column=0)

	m_sufix_label = Label(update_frame_label, text="Sufix: ")
	m_sufix_label.grid(row=9, column=2)

	#Entries
	u_id = Entry(update_frame_label, width=5)
	u_id.grid(row=0, column=1)

	m_name = Entry(update_frame_label, width=20)
	m_name.grid(row=1, column=1)

	m_tag = Entry(update_frame_label, width=20)
	m_tag.grid(row=2, column=1)

	m_username = Entry(update_frame_label, width=20)
	m_username.grid(row=3, column=1)

	m_initials = Entry(update_frame_label, width=20)
	m_initials.grid(row=3, column=3)

	m_group = Entry(update_frame_label, width=20)
	m_group.grid(row=4, column=3)

	m_removeQ = Entry(update_frame_label, width=20)
	m_removeQ.grid(row=5, column=1)

	m_replaceQ = Entry(update_frame_label, width=20)
	m_replaceQ.grid(row=5, column=3)

	m_removeW = Entry(update_frame_label, width=20)
	m_removeW.grid(row=6, column=1)

	m_replaceW = Entry(update_frame_label, width=20)
	m_replaceW.grid(row=6, column=3)

	m_prefix = Entry(update_frame_label, width=20)
	m_prefix.grid(row=9, column=1)

	m_sufix = Entry(update_frame_label, width=20)
	m_sufix.grid(row=9, column=3)

	#Buttons	
	u_chaColor = "#fff"
	m_color_button = Button(update_frame_label, width=15, text=u_chaColor, bg=u_chaColor, command=u_color)
	m_color_button.grid(row=4, column=1)

	m_insert_button = Button(update_frame_label, text="Update", width=15, command=update)
	m_insert_button.grid(row=11, column=0, columnspan=5, pady=5, padx=5)

	m_update_button = Button(update_frame_label, text="Load", width=15, command=load_character)
	m_update_button.grid(row=0, column=3, columnspan=5, pady=5, padx=5)



def load_character():
	conn = sqlite3.connect('character_list.db')
	c = conn.cursor()

	m_name.delete(0, END)
	m_tag.delete(0, END)
	m_username.delete(0, END)
	m_initials.delete(0, END)
	m_removeQ.delete(0, END)
	m_replaceQ.delete(0, END)
	m_removeW.delete(0, END)
	m_replaceW.delete(0, END)
	m_caps.set(m_caps_options[0])
	m_caps_sensitivity.deselect()
	m_gamzee_Quirk.deselect()
	m_tavros_Quirk.deselect()
	m_prefix.delete(0, END)
	m_sufix.delete(0, END)
	m_group.delete(0, END)

	c.execute("SELECT * FROM characters WHERE id=" + u_id.get())
	records = c.fetchall()
	for record in records:
		m_name.insert(0, str(record[1]))
		m_tag.insert(0, str(record[2]))
		m_username.insert(0, str(record[3]))
		m_initials.insert(0, str(record[4]))
		m_removeQ.insert(0, str(record[5]))
		m_replaceQ.insert(0, str(record[6]))
		m_removeW.insert(0, str(record[7]))
		m_replaceW.insert(0, str(record[8]))

		if record[9] == "No Capitalisation":
			m_caps.set(m_caps_options[0])
		elif record[9] == "All Capitalisation":
			m_caps.set(m_caps_options[1])
		elif record[9] == "Normal Capitalisation":
			m_caps.set(m_caps_options[2])

		if record[10] == 1:
			 m_caps_sensitivity.select() 
		else: 
			m_caps_sensitivity.deselect()
		
		if record[11] == 1:
			m_gamzee_Quirk.select()
		else:
			m_gamzee_Quirk.deselect()

		if record[12] == 1:
			m_tavros_Quirk.select()
		else:
			m_tavros_Quirk.deselect()

		m_prefix.insert(0, str(record[13]))
		m_sufix.insert(0, str(record[14]))

		u_chaColor = str(record[15])
		m_color_button = Button(update_frame_label, width=15, text=u_chaColor, bg=u_chaColor, command=u_color)
		m_color_button.grid(row=4, column=1)

		m_group.insert(0, str(record[16]))

	conn.commit()
	conn.close()

'''
"No Capitalisation",
"All Capitalisation",
"Normal Capitalisation"
'''

def submit():
	conn = sqlite3.connect('character_list.db')
	c = conn.cursor()

	c.execute("INSERT INTO characters VALUES(NULL, :name, :tag, :username, :initials, :removeQ, :replaceQ, :removeW, :replaceW, :caps, :caps_sensitivity, :gamzee_Quirk, :tavros_Quirk, :prefix, :sufix, :chaColor, :group)",
		{
			'name':name.get(),
			'tag':tag.get(),
			'username':username.get(),
			'initials':initials.get(),
			'removeQ':removeQ.get(),
			'replaceQ':replaceQ.get(),
			'removeW':removeW.get(),
			'replaceW':replaceW.get(),
			'caps':caps.get(),
			'caps_sensitivity':caps_sen_var.get(),
			'gamzee_Quirk':gamzee_Quirk_var.get(),
			'tavros_Quirk':tavros_Quirk_var.get(),
			'prefix':prefix.get(),
			'sufix':sufix.get(),
			'chaColor':str(chaColor),
			'group':group.get()
		})

	#c.execute("SELECT *,oid FROM characters")

	conn.commit()
	conn.close()

	#Clear Text boxes
	name.delete(0, END)
	tag.delete(0, END)
	username.delete(0, END)
	initials.delete(0, END)
	removeQ.delete(0, END)
	replaceQ.delete(0, END)
	removeW.delete(0, END)
	replaceW.delete(0, END)
	caps_sensitivity.deselect()
	gamzee_Quirk.deselect()
	tavros_Quirk.deselect()
	prefix.delete(0, END)
	sufix.delete(0, END)
	group.delete(0, END)

#GUI
#Frame
insert_frame = LabelFrame(root, padx=5, pady=5)
insert_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

#Labels
insert_frame_label = Label(root, text="Insert Character")
insert_frame_label.grid(row=0, column=0, pady=5, padx=5)

	#Insert Frame
name_Label = Label(insert_frame, text="Name: ")
name_Label.grid(row=0, column=0)

tag_label = Label(insert_frame, text="Tag: ")
tag_label.grid(row=1, column=0)

username_label = Label(insert_frame, text="User Name: ")
username_label.grid(row=2, column=0)

initials_labels = Label(insert_frame, text="Initials: ")
initials_labels.grid(row=2, column=2)

chooseColor_label = Label(insert_frame, text="Choose Color: ")
chooseColor_label.grid(row=3, column=0)

group_label = Label(insert_frame, text="Group: ")
group_label.grid(row=3, column=2)

removeQ_label = Label(insert_frame, text="Quirk - Remove: ")
removeQ_label.grid(row=4, column=0)

replaceQ_label = Label(insert_frame, text="Quirk - Replace: ")
replaceQ_label.grid(row=4, column=2)

removeW_label = Label(insert_frame, text="Word - Remove: ")
removeW_label.grid(row=5, column=0)

replaceW_label = Label(insert_frame, text="Word - Replace: ")
replaceW_label.grid(row=5, column=2)

caps_options =[
	"No Capitalisation",
	"All Capitalisation",
	"Normal Capitalisation"
]

caps = StringVar()
caps.set(caps_options[0])

caps_dropdown = OptionMenu(insert_frame, caps, *caps_options)
caps_dropdown.grid(row=6, column=0, columnspan=5)

#Checkboxes
caps_sen_var = IntVar()
caps_sensitivity = Checkbutton(insert_frame, text="Quirk is Cap Sensitive", variable=caps_sen_var, onvalue=1, offvalue=0)
caps_sensitivity.grid(row=7, column=0)

gamzee_Quirk_var = IntVar()
gamzee_Quirk = Checkbutton(insert_frame, text="Gamzee Quirk", variable=gamzee_Quirk_var, onvalue=1, offvalue=0)
gamzee_Quirk.grid(row=7, column=1)

tavros_Quirk_var = IntVar()
tavros_Quirk = Checkbutton(insert_frame, text="Tavros Quirk", variable=tavros_Quirk_var, onvalue=1, offvalue=0)
tavros_Quirk.grid(row=7, column=2)

prefix_label = Label(insert_frame, text="Prefix: ")
prefix_label.grid(row=8, column=0)

sufix_label = Label(insert_frame, text="Sufix: ")
sufix_label.grid(row=8, column=2)

#Entries
name = Entry(insert_frame, width=20)
name.grid(row=0, column=1)

tag = Entry(insert_frame, width=20)
tag.grid(row=1, column=1)

username = Entry(insert_frame, width=20)
username.grid(row=2, column=1)

initials = Entry(insert_frame, width=20)
initials.grid(row=2, column=3)

group = Entry(insert_frame, width=20)
group.grid(row=3, column=3)

removeQ = Entry(insert_frame, width=20)
removeQ.grid(row=4, column=1)

replaceQ = Entry(insert_frame, width=20)
replaceQ.grid(row=4, column=3)

removeW = Entry(insert_frame, width=20)
removeW.grid(row=5, column=1)

replaceW = Entry(insert_frame, width=20)
replaceW.grid(row=5, column=3)

prefix = Entry(insert_frame, width=20)
prefix.grid(row=8, column=1)

sufix = Entry(insert_frame, width=20)
sufix.grid(row=8, column=3)

#Buttons
color_button = Button(insert_frame, width=15, text="#fff", bg='white', command=color)
color_button.grid(row=3, column=1)

insert_button = Button(insert_frame, text="Insert", width=15, command=submit)
insert_button.grid(row=10, column=0, columnspan=5, pady=5, padx=5)

show_characters_button = Button(root, text="Show Character List", command=show_characters)
show_characters_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

modify_characters_button = Button(root, text="Modify Entry", command=modify)
modify_characters_button.grid(row=2, column=1, columnspan=2, pady=10, padx=10)

conn.commit()

conn.close()

root.mainloop()