#!/usr/bin/python3

import os

try:
	import tkinter
	import tkinter.ttk
	import tkinter.colorchooser
	import tkinter.messagebox
except ImportError:
	print('Error: Python 3.X is required. Please upgrade in order to use this converter.')

try:
	from pydub import AudioSegment
	from pydub.utils import mediainfo
except ImportError:
	print('Error: PyDub is required. Please install via pip: ' + 'sudo pip install pydub')
	print('Make sure PyDub is installed for Python 3.')

# TODO
# str() all strings
# Make code more Pythonic
# Keep metadata on export (checkbox)
# Delete original files after convert (checkbox)
# Debug output box in advanced tab
# Stop conversion button (deletes current file being converted)
# Clean up code naming convention
# Command line tool
# Reset settings to default button
# Background colour setting
# Toolbar open file
# Just edit song metadata functionality maybe? (edit -> dialog box? Could use Mutagen)
# Metadata loading (XML, JSON?)
# Save inputted fields (except metadata possibly)

class AudioConverter(tkinter.Frame):

	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)

		self.parent = parent

		self.width = 480
		self.height = 640

		self.window_width = self.parent.winfo_screenwidth()
		self.window_height = self.parent.winfo_screenheight()

		self.extensions = ['mp3', 'ogg', 'wav', 'aac', 'flac', 'flv']
		self.themes = ['default', 'classic', 'clam', 'alt']

		self.default_dir_found_colour = 'green'
		self.default_dir_not_found_colour = 'red'

		self.dir_found_colour = 'green'
		self.dir_not_found_colour = 'red'

		self.default_lib = AudioSegment.converter

		self.init_UI()

	def init_UI(self):
		self.parent.title('Pyverter')
		self.pack(fill=tkinter.BOTH, expand=1)

		self.style = tkinter.ttk.Style()
		self.style.theme_use('default')

		# Notebook
		self.tabbed_frame = tkinter.ttk.Notebook(self)

		# Notebook tabs
		self.basic_tab = tkinter.ttk.Frame(self.tabbed_frame)
		self.metadata_tab = tkinter.ttk.Frame(self.tabbed_frame)
		self.advanced_tab = tkinter.ttk.Frame(self.tabbed_frame)

		# Basic tab
		self.input_dir_text = tkinter.StringVar()
		self.input_dir_text.trace('w', self.check_for_input_filename)
		self.input_dir_label = tkinter.Label(self.basic_tab, text='Input Directory: ')
		self.input_dir_textbox = tkinter.Entry(self.basic_tab, textvariable=self.input_dir_text)

		self.dropdown_option = tkinter.StringVar(self.basic_tab)
		self.dropdown_option.set(self.extensions[0])
		self.export_format_label = tkinter.Label(self.basic_tab, text='Export Format: ')
		self.export_format_dropdown = tkinter.OptionMenu(self.basic_tab, self.dropdown_option, 'mp3', 'ogg', 'wav', 'aac', 'flac', 'flv')

		self.export_filename_text = tkinter.StringVar()

		self.export_filename_label = tkinter.Label(self.basic_tab, text='Output Filename: ')
		self.export_filename_textbox = tkinter.Entry(self.basic_tab, textvariable=self.export_filename_text)

		self.export_filename_label.config(state='disabled')
		self.export_filename_textbox.config(state='disabled')

		self.output_dir_text = tkinter.StringVar()
		self.output_dir_text.trace('w', self.check_for_outputdir_filename)

		self.output_dir_label = tkinter.Label(self.basic_tab, text='Output Directory: ')
		self.output_dir_textbox = tkinter.Entry(self.basic_tab, textvariable=self.output_dir_text)

		self.close_on_convert_num = tkinter.IntVar()
		self.close_on_convert_label = tkinter.Label(self.basic_tab, text='Close when finished')
		self.close_on_convert_checkbox = tkinter.Checkbutton(self.basic_tab, variable=self.close_on_convert_num)

		self.delete_original_files_num = tkinter.IntVar()
		self.delete_original_files_label = tkinter.Label(self.basic_tab, text='Delete original files')
		self.delete_original_files_checkbox = tkinter.Checkbutton(self.basic_tab, variable=self.delete_original_files_num)


		self.input_dir_label.grid(row=0, sticky=tkinter.W, padx=10, pady=10)
		self.input_dir_textbox.grid(row=0, column=1, padx=10, pady=10)

		self.export_format_label.grid(row=1, sticky=tkinter.W, padx=10, pady=10)
		self.export_format_dropdown.grid(row=1, column=1, sticky=tkinter.W, padx=10, pady=10)

		self.export_filename_label.grid(row=2, sticky=tkinter.W, padx=10, pady=10)
		self.export_filename_textbox.grid(row=2, column=1, padx=10, pady=10)

		self.output_dir_label.grid(row=3, sticky=tkinter.W, padx=10, pady=10)
		self.output_dir_textbox.grid(row=3, column=1, padx=10, pady=10)

		self.close_on_convert_label.grid(row=4, sticky=tkinter.W, padx=10, pady=10)
		self.close_on_convert_checkbox.grid(row=4, column=1, sticky=tkinter.W, padx=5, pady=10)

		self.delete_original_files_label.grid(row=5, sticky=tkinter.W, padx=10, pady=10)
		self.delete_original_files_checkbox.grid(row=5, column=1, sticky=tkinter.W, padx=5, pady=10)


		# Metadata tab
		self.song_title_text = tkinter.StringVar()
		self.song_title_label = tkinter.Label(self.metadata_tab, text='Title: ')
		self.song_title_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_title_text)

		self.song_artist_text = tkinter.StringVar()
		self.song_artist_label = tkinter.Label(self.metadata_tab, text='Artist: ')
		self.song_artsit_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_artist_text)

		self.song_album_artist_text = tkinter.StringVar()
		self.song_album_artist_label = tkinter.Label(self.metadata_tab, text='Album Artist: ')
		self.song_album_artist_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_album_artist_text)

		self.song_album_text = tkinter.StringVar()
		self.song_album_label = tkinter.Label(self.metadata_tab, text='Album: ')
		self.song_album_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_album_text)

		self.song_genre_text = tkinter.StringVar()
		self.song_genre_label = tkinter.Label(self.metadata_tab, text='Genre: ')
		self.song_genre_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_genre_text)

		self.song_year_text = tkinter.StringVar()
		self.song_year_label = tkinter.Label(self.metadata_tab, text='Year: ')
		self.song_year_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_year_text)

		self.song_track_text = tkinter.StringVar()
		self.song_track_label = tkinter.Label(self.metadata_tab, text='Track: ')
		self.song_track_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_track_text)

		self.song_disc_text = tkinter.StringVar()
		self.song_disc_label = tkinter.Label(self.metadata_tab, text='Disc: ')
		self.song_disc_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_disc_text)

		self.song_composer_text = tkinter.StringVar()
		self.song_composer_label = tkinter.Label(self.metadata_tab, text='Composer(s): ')
		self.song_composer_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_composer_text)

		self.song_bitrate_text = tkinter.StringVar()
		self.song_bitrate_label = tkinter.Label(self.metadata_tab, text='Bitrate: ')
		self.song_bitrate_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_bitrate_text)

		self.song_comment_text = tkinter.StringVar()
		self.song_comment_label = tkinter.Label(self.metadata_tab, text='Comment: ')
		self.song_comment_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_comment_text)

		self.song_total_tracks_text = tkinter.StringVar()
		self.song_total_tracks_label = tkinter.Label(self.metadata_tab, text='Total Tracks: ')
		self.song_total_tracks_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_total_tracks_text)

		self.song_total_discs_text = tkinter.StringVar()
		self.song_total_discs_label = tkinter.Label(self.metadata_tab, text='Total Discs: ')
		self.song_total_discs_textbox = tkinter.Entry(self.metadata_tab, textvariable=self.song_total_discs_text)

		self.song_explicit_num = tkinter.IntVar()
		self.song_explicit_label = tkinter.Label(self.metadata_tab, text='Explicit: ')
		self.song_explicit_checkbox = tkinter.Checkbutton(self.metadata_tab, variable=self.song_explicit_num)


		self.song_title_label.grid(row=0, sticky=tkinter.W, padx=10, pady=5)
		self.song_title_textbox.grid(row=0, column=1, padx=10, pady=5)

		self.song_artist_label.grid(row=1, sticky=tkinter.W, padx=10, pady=5)
		self.song_artsit_textbox.grid(row=1, column=1, padx=10, pady=5)

		self.song_album_artist_label.grid(row=2, sticky=tkinter.W, padx=10, pady=5)
		self.song_album_artist_textbox.grid(row=2, column=1, padx=10, pady=5)

		self.song_album_label.grid(row=3, sticky=tkinter.W, padx=10, pady=5)
		self.song_album_textbox.grid(row=3, column=1, padx=10, pady=5)

		self.song_genre_label.grid(row=4, sticky=tkinter.W, padx=10, pady=5)
		self.song_genre_textbox.grid(row=4, column=1, padx=10, pady=5)

		self.song_year_label.grid(row=5, sticky=tkinter.W, padx=10, pady=5)
		self.song_year_textbox.grid(row=5, column=1, padx=10, pady=5)

		self.song_track_label.grid(row=6, sticky=tkinter.W, padx=10, pady=5)
		self.song_track_textbox.grid(row=6, column=1, padx=10, pady=5)

		self.song_disc_label.grid(row=8, sticky=tkinter.W, padx=10, pady=5)
		self.song_disc_textbox.grid(row=8, column=1, padx=10, pady=5)

		self.song_composer_label.grid(row=9, sticky=tkinter.W, padx=10, pady=5)
		self.song_composer_textbox.grid(row=9, column=1, padx=10, pady=5)

		self.song_bitrate_label.grid(row=10, sticky=tkinter.W, padx=10, pady=5)
		self.song_bitrate_textbox.grid(row=10, column=1, padx=10, pady=5)

		self.song_comment_label.grid(row=11, sticky=tkinter.W, padx=10, pady=5)
		self.song_comment_textbox.grid(row=11, column=1, padx=10, pady=5)

		self.song_total_tracks_label.grid(row=12, sticky=tkinter.W, padx=10, pady=5)
		self.song_total_tracks_textbox.grid(row=12, column=1, padx=10, pady=5)

		self.song_total_discs_label.grid(row=13, sticky=tkinter.W, padx=10, pady=5)
		self.song_total_discs_textbox.grid(row=13, column=1, padx=10, pady=5)

		self.song_explicit_label.grid(row=14, sticky=tkinter.W, padx=10, pady=5)
		self.song_explicit_checkbox.grid(row=14, column=1, sticky=tkinter.W, padx=5, pady=5)


		# Advanced tab
		self.path_to_converter_lib_text = tkinter.StringVar()
		self.path_to_converter_lib_text.trace('w', self.check_converter_path)

		self.path_to_converter_lib_label = tkinter.Label(self.advanced_tab, text='Path to FFMPEG/avconv: ')
		self.path_to_converter_lib_textbox = tkinter.Entry(self.advanced_tab, textvariable=self.path_to_converter_lib_text)

		self.converter_theme_var = tkinter.StringVar()
		self.converter_theme_var.set(self.themes[0])
		self.converter_theme_label = tkinter.Label(self.advanced_tab, text='Theme: ')
		self.converter_theme_dropdown = tkinter.OptionMenu(self.advanced_tab, self.converter_theme_var, 'default', 'classic', 'clam', 'alt', command=self.update_theme)

		self.dir_found_colour_button = tkinter.Button(self.advanced_tab, text='Directory Found Colour', command=self.get_dir_found_colour)
		self.dir_not_found_colour_button = tkinter.Button(self.advanced_tab, text='Directory Not Found Colour', command=self.get_dir_not_found_colour)


		self.path_to_converter_lib_label.grid(row=0, sticky=tkinter.W, padx=10, pady=10)
		self.path_to_converter_lib_textbox.grid(row=0, column=1, padx=10, pady=10)

		self.converter_theme_label.grid(row=1, sticky=tkinter.W, padx=10, pady=10)
		self.converter_theme_dropdown.grid(row=1, column=1, sticky=tkinter.W, padx=30, pady=10)

		self.dir_found_colour_button.grid(row=2, sticky=tkinter.W, padx=10, pady=10)
		self.dir_not_found_colour_button.grid(row=2, column=1, sticky=tkinter.W, padx=10, pady=10)


		# Adding all of our elements to our Notebook
		self.tabbed_frame.add(self.basic_tab, text='Basic')
		self.tabbed_frame.add(self.metadata_tab, text='Metadata')
		self.tabbed_frame.add(self.advanced_tab, text='Advanced')

		self.tabbed_frame.pack(pady=10)


		# Root window
		self.progress_value = tkinter.IntVar()

		self.conversion_progressbar = tkinter.ttk.Progressbar(self.parent, orient='horizontal', mode='determinate', length=200, variable=self.progress_value)
		self.convert_button = tkinter.Button(self.parent, text='Convert!', command=self.convert_audio)

		self.conversion_progressbar.pack(pady=10)
		self.convert_button.pack(pady=20)

		self.center_window()


	def convert_audio(self):
		inputdir = self.input_dir_textbox.get()
		outputdir = self.output_dir_textbox.get()

		# Resetting conversion progressbar so that it has no progress
		self.conversion_progressbar['value'] = 0

		# Making sure the path actually contains something, otherwise inputdir[-1] will return an error since it's blank
		if len(inputdir) > 0 and len(outputdir) > 0:
			# Replacing home dir shortcut with actual user homedir, if it's in there
			if '~' in inputdir:
				inputdir = inputdir.replace('~', os.path.expanduser('~'))

			if '~' in outputdir:
				outputdir = outputdir.replace('~', os.path.expanduser('~'))

			# Removing a forward slash or a backslash from the input and output directory string, if it exists
			if inputdir.endswith('/') or inputdir.endswith('\\'):
				inputdir = inputdir[:-1]

			if outputdir.endswith('/') or outputdir.endswith('\\'):
				outputdir = outputdir[:-1]


			# Making sure the directory exists
			if os.path.exists(inputdir) and os.path.exists(outputdir):
				# Getting the file name and it's extension
				filename = os.path.basename(inputdir)
				fn, extension = os.path.splitext(filename)

				# Removing the '.' from the file extension, will help eliminate problems later on!
				if extension.startswith('.'):
					extension = extension.replace('.', '')


				# Getting the song metadata
				metadata = self.get_metadata()

				br = metadata['bitrate'] or '128k'
				if 'k' not in br:
					br += 'k'

				# Converting only 1 file
				if len(extension) > 0:
					self.conversion_progressbar['maximum'] = 1

					song = AudioSegment.from_file(str(inputdir))

					if len(self.export_filename_text.get()) is not 0:
						# If there's a filepath for whatever reason in the output filename, remove it
						basefile = os.path.basename(self.export_filename_text.get())

						if os.path.exists(os.path.join(outputdir, basefile + '.' + self.dropdown_option.get())):
							proceed = tkinter.messagebox.askokcancel('Warning', 'The file you\'re trying to convert already exists. Would you like to override it?')

							if not proceed:
								tkinter.messagebox.showinfo('Cancelled', 'Stopped conversion')
								return


						song.export(os.path.join(outputdir, basefile + '.' + self.dropdown_option.get()), format=self.dropdown_option.get(), bitrate=br, tags=metadata)

						if self.delete_original_files_num.get() is 1:
							os.remove(inputdir)

						self.progress_value.set(self.progress_value.get() + 1)
					else:
						if os.path.exists(os.path.join(outputdir, basefile + '.' + self.dropdown_option.get())):
							proceed = tkinter.messagebox.askokcancel('Warning', '%s already exists. Would you like to override it?' % (basefile + '.' + self.dropdown_option.get()))

							if not proceed:
								tkinter.messagebox.showinfo('Cancelled', 'Stopped conversion')
								return


						song.export(os.path.join(outputdir, fn + '.' + self.dropdown_option.get()), format=self.dropdown_option.get(), bitrate=br, tags=metadata)

						if self.delete_original_files_num.get() is 1:
							os.remove(inputdir)

						self.progress_value.set(self.progress_value.get() + 1)
				# Converting a directory
				elif len(extension) <= 0:
					dir_files = [f for f in os.listdir(inputdir) for e in self.extensions if os.path.isfile(os.path.join(str(inputdir), str(f))) and f.endswith(e)]

					dir_files_iter = iter(dir_files)

					# For all the files in my input directory,
					# If any of the files end in a support file extension
					# Convert them
					self.conversion_progressbar['maximum'] = len(dir_files)

					for file in dir_files_iter:
						song = AudioSegment.from_file(os.path.join(str(inputdir), str(file)))

						f, e = os.path.splitext(file)

						if os.path.exists(os.path.join(outputdir, f + '.' + self.dropdown_option.get())):
							proceed = tkinter.messagebox.askokcancel('Warning', '%s already exists. Would you like to skip it?' % (f + '.' + self.dropdown_option.get()))

							if proceed:
								tkinter.messagebox.showinfo('Skipped', 'Skipped %s' % (f + '.' + self.dropdown_option.get()))

								next(dir_files_iter, None)

								continue

						song.export(os.path.join(outputdir, f + '.' + self.dropdown_option.get()), format=self.dropdown_option.get(), bitrate=br, tags=metadata)

						if self.delete_original_files_num.get() is 1:
							os.remove(os.path.join(str(inputdir), str(file)))

						self.progress_value.set(self.progress_value.get() + 1)

				tkinter.messagebox.showinfo('Conversion complete!', 'Converted file(s)')

				if self.close_on_convert_num.get() is 1:
					self.quit()
				else:
					return
		else:
			tkinter.messagebox.showerror('Error', 'Seems like the input or output directory doesn\'t exist...')

			return


	def center_window(self):
		x = (self.window_width - self.width) / 2
		y = (self.window_height - self.height) / 2

		self.parent.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))


	def check_for_input_filename(self, *args):
		inputdir = self.input_dir_text.get()

		if len(inputdir) > 0:
			if '~' in inputdir:
				inputdir = inputdir.replace('~', os.path.expanduser('~'))

			if inputdir.endswith('/') or inputdir.endswith('\\'):
				inputdir = inputdir[:-1]


		if not os.path.exists(inputdir):
			self.input_dir_label.config(fg=self.dir_not_found_colour)

			self.convert_button.config(state='disabled')
		else:
			self.input_dir_label.config(fg=self.dir_found_colour)

			if os.path.isfile(inputdir):
				filename = os.path.basename(inputdir)
				fn, extension = os.path.splitext(filename)

				self.export_filename_text.set(fn)

				self.export_filename_label.config(state='normal')
				self.export_filename_textbox.config(state='normal')

				self.convert_button.config(state='normal')
			elif os.path.dirname(inputdir):
				self.export_filename_text.set('')

				self.export_filename_label.config(state='disabled')
				self.export_filename_textbox.config(state='disabled')

				self.convert_button.config(state='normal')


	def check_for_outputdir_filename(self, *args):
		outputdir = self.output_dir_text.get()

		if len(outputdir) > 0:
			if '~' in outputdir:
				outputdir = outputdir.replace('~', os.path.expanduser('~'))

			if outputdir.endswith('/') or outputdir.endswith('\\'):
				outputdir = outputdir[:-1]


		if not os.path.exists(outputdir):
			self.output_dir_label.config(fg=self.dir_not_found_colour)

			self.convert_button.config(state='disabled')
		else:
			self.output_dir_label.config(fg=self.dir_found_colour)

			self.convert_button.config(state='normal')

			if os.path.isfile(outputdir):
				filename = os.path.basename(outputdir)
				fn, extension = os.path.splitext(filename)

				self.export_filename_text.set(fn)

				self.export_filename_label.config(state='normal')
				self.export_filename_textbox.config(state='normal')

				self.convert_button.config(state='normal')


	def get_metadata(self):
		title = str(self.song_title_text.get())
		artist = str(self.song_artist_text.get())
		album_artist = str(self.song_artist_text.get())
		album = str(self.song_album_text.get())
		genre = str(self.song_artist_text.get())
		year = str(self.song_year_text.get())
		track = str(self.song_track_text.get())
		disc = str(self.song_disc_text.get())
		composers = str(self.song_composer_text.get())
		bitrate = str(self.song_bitrate_text.get())
		comment = str(self.song_comment_text.get())
		total_tracks = str(self.song_total_tracks_text.get())
		total_discs = str(self.song_total_discs_text.get())
		explicit = None
		if explicit is 0:
			explicit = str(False)
		else:
			explicit = str(True)

		return { 'title': title, 'artist': artist, 'album_artist': album_artist, 'album': album, 'genre': genre, 'date': year, 'track': track, 'disc': disc, 'composer': composers, 'bitrate': bitrate, 'comment': comment, 'total_tracks': total_tracks, 'total_discs': total_discs, 'explicit': explicit }


	def get_dir_found_colour(self):
		self.dir_found_colour = tkinter.colorchooser.askcolor()[1]


	def get_dir_not_found_colour(self):
		self.dir_not_found_colour = tkinter.colorchooser.askcolor()[1]


	def update_theme(self, *args):
		self.style.theme_use(self.converter_theme_var.get())


	def check_converter_path(self, *args):
		path = self.path_to_converter_lib_text.get()

		if len(path) > 0:
			if '~' in path:
				path = path.replace('~', os.path.expanduser('~'))

			if path.endswith('/') or path.endswith('\\'):
				path = path[:-1]


		if not os.path.exists(path):
			AudioSegment.converter = self.default_lib

			self.path_to_converter_lib_label.config(fg=self.dir_not_found_colour)
			self.convert_button.config(state='disabled')
		else:
			AudioSegment.converter = path

			self.path_to_converter_lib_label.config(fg=self.dir_found_colour)
			self.convert_button.config(state='normal')


if __name__ == '__main__':
	root = tkinter.Tk()
	app = AudioConverter(root)

	root.minsize(app.width, app.height)

	root.mainloop()
