from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
# from googlesearching import GoogleSearch
# from stackoverflowparser import StackoverflowParser
import webbrowser
from googlesearch import search
import goslate
selected_language = ""
links_quantity = 5
links = []
answers = []
answer_index = 0	
class GoogleSearch:
	def get_search_links(query: str, quantity = 5, link_must_contain = ""):
		if query == "":
			raise Exception("Empty query Error")
		links = list(search(query=query, num=quantity, stop=quantity))

		def filter():
			for i in links:
				if link_must_contain not in i:
					links.remove(i)
					filter()
		if link_must_contain != "":
			filter()
		return links
import requests
from bs4 import BeautifulSoup
class StackoverflowParser:
	def get_answer(url):
		response = requests.get(url=url)
		soup = BeautifulSoup(response.content, "html.parser")
		first_answer = soup.find("div", class_="answer")
		if first_answer is None:
			return "No answer found"
		else:
			return first_answer.find("div", class_="js-post-body").text
class ProgrammingHelperApp(MDApp):
	def build(self):
		self.theme_cls.primary_pallete = "LightBlue"
		return Builder.load_file("app.kv")
	def select_language(self, language):
		global selected_language
		selected_language = language
	def change_theme(self):
		if self.theme_cls.theme_style=="Dark":
			self.theme_cls.theme_style="Light"
			self.root.ids.question_label.color = self.theme_cls.primary_color
			self.root.ids.answer_tracker.color = self.theme_cls.primary_color
		else:
			self.theme_cls.theme_style="Dark"
	def get_answer(self):
		global answers
		global answer_index
		global links
		question = self.root.ids.question_input.text
		if question != "":
			answer_index = 0
			self.root.ids.answer_toolbar.title = question
			gs=goslate.Goslate()
			tr = gs.translate(question,"en")
			links = GoogleSearch.get_search_links(f"{tr} {selected_language} stackoverflow", links_quantity,"https://stackoverflow")
			answers = []
			for i in links:
				answers.append(StackoverflowParser.get_answer(i))
			self.root.current = 'answer'
			self.show_answer()
	def show_answer(self):
		self.root.ids.answer_tracker.text = f"{answer_index+1}/{len(answers)}"
		self.root.ids.answer_scroll.scroll_y = 1
		try:
			self.root.ids.answer_text.text = f"{answers[answer_index]}"
		except IndexError:
			self.root.ids.answer_text.text = "No answers were found"
	def update_answer_index(self, how_much):
		global answer_index
		if answer_index + how_much >= 0 and answer_index + how_much<len(answers):
			answer_index += how_much
			self.show_answer()
		self.root.ids.answer_tracker.text = f"{answer_index+1}/{len(answers)}"
	def open_answer(self):
		webbrowser.open(links[answer_index])




class LanguageToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.background_down = self.theme_cls.primary_light



ProgrammingHelperApp().run()

