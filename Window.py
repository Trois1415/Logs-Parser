from tkinter import *

class MOVE_WINDOW():
	def __init__(self, window, element):
		self.root = window
		self.element = element

		self.bind_wait()

	def bind_wait(self):
		self.element.bind('<B1-Motion>', lambda event: self.get_pos(event))

	def get_pos(self, event):
		global maximized
		if maximized:	maximize()

		global quarter
		global half
		if quarter or half:
			global past_size
			self.root.geometry(past_size)
			quarter = half = False

		self.xwin = self.root.winfo_x() - event.x_root
		self.ywin = self.root.winfo_y() - event.y_root

		self.element.bind('<B1-Motion>', lambda event: self.move_window(event))

	def move_window(self, event):
		self.root.config(cursor='cross')

		self.new_pos = f'+{event.x_root + self.xwin}+{event.y_root + self.ywin}'
		self.root.geometry(self.new_pos)

		global past_size
		if event.y_root + self.ywin < 0:
			past_size = self.root.geometry(f'+{event.x_root + self.xwin}+0')
		else:
			past_size = self.root.geometry()
		
		self.element.bind('<ButtonRelease-1>', lambda event: self.release_window(event))

	def release_window(self, event):
		self.root.config(cursor='arrow')

		self.width = self.root.winfo_screenwidth()
		self.height = self.root.winfo_screenheight()

		if event.x_root < 3 and event.y_root < 3:
			default_up_left(self.width, self.height)
		elif event.x_root > self.width - 3 and event.y_root < 3:
			default_up_right(self.width, self.height)
		elif event.x_root < 3 and event.y_root > self.height - 3:
			default_bottom_left(self.width, self.height)
		elif event.x_root > self.width - 3 and event.y_root > self.height - 3:
			default_bottom_right(self.width, self.height)
		elif event.x_root < 3 :
			default_full_left(self.width, self.height)
		elif event.x_root > self.width - 3 :
			default_full_right(self.width, self.height)
		elif event.y_root < 3:
			maximize()
		
		self.bind_wait()

def default_up_left(width, height):
	global past_size
	global quarter
	if not quarter:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height/2)}+0+0')
	else:
		root.geometry(past_size)
	quarter = not quarter

def default_up_right(width, height):
	global past_size
	global quarter
	if not quarter:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height/2)}+{int(width/2)}+0') 
	else:
		root.geometry(past_size)
	quarter = not quarter

def default_bottom_left(width, height):
	global past_size
	global quarter
	if not quarter:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height/2)}+0+{int(height/2)}') 
	else:
		root.geometry(past_size)
	quarter = not quarter

def default_bottom_right(width, height):
	global past_size
	global quarter
	if not quarter:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height/2)}+{int(width/2)}+{int(height/2)}') 
	else:
		root.geometry(past_size)
	quarter = not quarter

def default_full_left(width, height):
	global past_size
	global half
	if not half:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height)}+0+0')
	else:
		root.geometry(past_size)
	half = not half

def default_full_right(width, height):
	global past_size
	global half
	if not half:
		past_size = root.geometry()
		root.geometry(f'{int(width/2)}x{int(height)}+{int(width/2)}+0')
	else:
		root.geometry(past_size)
	half = not half


def hover(button, bg):
	button.config(bg=bg) 

def not_hover(button):
	button.config(bg='black') 

def minimize(event):
	root.update_idletasks()
	root.overrideredirect(False)
	root.iconify()

def maximize(event=None):
	global maximized
	global past_size
	if not maximized:
		past_size = root.geometry()
		root.overrideredirect(False)
		root.attributes('-fullscreen', True)
		maximize_button.config(text='◱')
	else:
		root.attributes('-fullscreen', False)
		root.overrideredirect(True)
		root.geometry(past_size)
		maximize_button.config(text='◻')
	maximized = not maximized

def _map(event):
	root.update_idletasks()
	root.overrideredirect(True)
	root.state('normal')

def close_app(event):
	root.destroy()

def hover_resize(area, vector : str):
	match vector:
		case 'h':
			root.config(cursor=f'sb_{vector}_double_arrow')
			area.bind('<B1-Motion>', resize_x)
		case 'v':
			root.config(cursor=f'sb_{vector}_double_arrow')
			area.bind('<B1-Motion>', resize_y)
		case 'bottom_right_corner':
			root.config(cursor='bottom_right_corner')
			area.bind('<B1-Motion>', resize_xy_br)


def not_hover_resize(event):
	root.config(cursor='arrow') 

def resize_x(event):
	xwin = root.winfo_x()

	diff = (event.x_root - xwin) - root.winfo_width()

	if root.winfo_width() > 150:
		root.geometry(f'{root.winfo_width() + diff}x{root.winfo_height()}')
	else:
		if diff > 0:
			root.geometry(f'{root.winfo_width() + diff}x{root.winfo_height()}') 

def resize_y(event):
	ywin = root.winfo_y()

	diff = (event.y_root - ywin) - root.winfo_height()

	if root.winfo_height() > 150:
		root.geometry(f'{root.winfo_width()}x{root.winfo_height() + diff}')
	else:
		if diff > 0:
			root.geometry(f'{root.winfo_width()}x{root.winfo_height() + diff}') 
 
def resize_xy_br(event):
	ywin = root.winfo_y()
	xwin = root.winfo_x()

	diffx = (event.x_root - xwin) - root.winfo_width()
	diffy = (event.y_root - ywin) - root.winfo_height()

	if root.winfo_height() > 150 and root.winfo_width() > 150:
		root.geometry(f'{root.winfo_width() + diffx}x{root.winfo_height() + diffy}')
	elif diffx > 0 and diffy > 0:
		root.geometry(f'{root.winfo_width() + diffx}x{root.winfo_height() + diffy}')
	else:
		if root.winfo_width() > 150:
			root.geometry(f'{root.winfo_width() + diffx}x{root.winfo_height()}')
		else:
			if diffx > 0:
				root.geometry(f'{root.winfo_width() + diffx}x{root.winfo_height()}')

		if root.winfo_height() > 150:
			root.geometry(f'{root.winfo_width()}x{root.winfo_height() + diffy}')
		else:
			if diffy > 0:
				root.geometry(f'{root.winfo_width()}x{root.winfo_height() + diffy}') 


#Create app
root = Tk()
root.configure(bg='black')

#Hide default titlebar
root.overrideredirect(True)

#Init custom titlebar
title_bar = Frame(root, bg='black', relief='raised')
label = Label(title_bar, text='Hello world', fg='white', bg='black')

minimize_button = Button(root, bg='black', fg='white', text='⎯', borderwidth=0)
maximize_button = Button(root, bg='black', fg='white', text='◻', borderwidth=0)
maximized = False
quarter = False
half = False
past_size = root.geometry()

close_button = Button(root, bg='black', fg='white', text='🞩', borderwidth=0)

right_bar = Frame(root, bg = 'white', relief='raised')
bottom_bar = Frame(root, bg = 'white', relief='raised')
corner_br = Frame(root, bg='white', relief='raised')

#Default window content
window = Frame(root, bg='white', relief='raised')

#Grid objects
title_bar.grid(row=0, column=0, sticky='ew', ipadx=5, ipady=3)
label.grid()
root.grid_columnconfigure(0, weight=1)
close_button.grid(row=0, column=3, columnspan=3, sticky='nesw', ipadx=5, ipady=2)
maximize_button.grid(row=0, column=2, sticky='nes', ipadx=5, ipady=2)
minimize_button.grid(row=0, column=1, sticky='nes', ipadx=5, ipady=2)

root.grid_rowconfigure(1, weight=1)
right_bar.grid(row=1, column=5, sticky='wnes')
bottom_bar.grid(row=2, column=0, columnspan=5, sticky='nesw', ipady=3)
corner_br.grid(row=2, column=5, sticky='nwse', ipady=3)

window.grid(row=1, column=0, columnspan=5, sticky='ewns', ipadx=50, ipady=50)

#Events
MOVE_WINDOW(root, title_bar)
MOVE_WINDOW(root, label)

title_bar.bind('<Map>', _map)

close_button.bind('<Button-1>', close_app)
close_button.bind('<Enter>', lambda event: hover(close_button, 'red'))
close_button.bind('<Leave>', lambda event: not_hover(close_button))

maximize_button.bind('<Button-1>', maximize)
maximize_button.bind('<Enter>', lambda event: hover(maximize_button, 'grey'))
maximize_button.bind('<Leave>', lambda event: not_hover(maximize_button))

minimize_button.bind('<Button-1>', minimize)
minimize_button.bind('<Enter>', lambda event: hover(minimize_button, 'grey'))
minimize_button.bind('<Leave>', lambda event: not_hover(minimize_button))

right_bar.bind('<Enter>', lambda event: hover_resize(right_bar,'h'))
right_bar.bind('<Leave>', not_hover_resize)

bottom_bar.bind('<Enter>', lambda event: hover_resize(bottom_bar, 'v'))
bottom_bar.bind('<Leave>', not_hover_resize)

corner_br.bind('<Enter>', lambda event: hover_resize(corner_br, 'bottom_right_corner'))
corner_br.bind('<Leave>', not_hover_resize)

#Main
root.mainloop()
