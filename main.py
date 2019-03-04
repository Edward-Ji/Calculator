import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

kivy.require("1.10.1")
Window.size = (350, 420)

switch = {'×': '*',
          '÷': '/',
          '%': "*0.01"}


class OperatorBtn(ToggleButton):
    pass


class CalcLayout(BoxLayout):

    error = False
    full_exp = ''

    def true_exp(self):
        exp = self.full_exp
        for pair in switch.items():
            exp = exp.replace(*pair)
        return exp

    def inverse(self):
        if self.error:
            return
        try:
            result = - eval(self.display.text)
            self.display.text = str(result)
        except Exception as e:
            self.error = True
            self.clear_btn.text = "AC"
            self.display.text = e.__class__.__name__

    def add(self, char):
        if self.error:
            return
        if len(self.display.text) >= 10:
            return
        self.clear_btn.text = 'C'
        operators = OperatorBtn.get_widgets("operators")
        for operator_btn in operators:
            if operator_btn.state == "down":
                operator_btn.state = "normal"
                self.full_exp += self.display.text + operator_btn.text
                self.display.text = ''
        else:
            self.display.text += char

    def calc(self):
        if self.error:
            return
        expression = self.true_exp() + self.display.text
        try:
            result = eval(expression)
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
            self.display.text = str(result)
            self.full_exp = ''
        except Exception as e:
            self.error = True
            self.clear_btn.text = "AC"
            self.display.text = e.__class__.__name__

    def clear(self):
        self.display.text = ''
        if self.clear_btn.text == "AC":
            self.full_exp = ''
            self.error = False
        else:
            self.clear_btn.text = "AC"


class CalculatorApp(App):

    def build(self):
        return CalcLayout()


calcApp = CalculatorApp()
calcApp.run()
