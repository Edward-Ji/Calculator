import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

kivy.require("1.10.1")
Window.size = (350, 420)
Window.minimum_width, Window.minimum_height = 350, 420

switch = {'×': '*',
          '÷': '/',
          '%': "*0.01"}


class NumberBtn(Button):

    def on_press(self):
        self.background_color = [0.2, 0.2, 0.2, 1]
        return super(NumberBtn, self).on_press()

    def on_touch_up(self, touch):
        self.background_color = [0.3, 0.3, 0.3, 1]
        return super(NumberBtn, self).on_touch_up(touch)


class SpecialBtn(Button):

    def on_press(self):
        self.background_color = [0.75, 0.45, 0, 0.9]
        return super(SpecialBtn, self).on_press()

    def on_touch_up(self, touch):
        self.background_color = [1, 0.6, 0, 0.9]
        return super(SpecialBtn, self).on_touch_up(touch)


class OperatorBtn(ToggleButton):

    def on_touch_up(self, touch):
        if self.state == "down":
            self.background_color = [0.75, 0.45, 0, 0.9]
        else:
            self.background_color = [1, 0.6, 0, 0.9]
        return super(OperatorBtn, self).on_touch_down(touch)


class CalcLayout(BoxLayout):

    error = False
    end = False
    full_exp = []
    last_ope = None
    ans = ''

    def true_exp(self, exp=None):
        if not exp:
            exp = ''.join(self.full_exp) + self.display.text
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
        if char == '.':
            if '.' in self.display.text:
                return
        elif self.display.text == '0':
            self.display.text = ''
        self.clear_btn.text = 'C'
        operators = OperatorBtn.get_widgets("operators")
        if self.end:
            self.end = False
            self.display.text = ''
        for operator_btn in operators:
            if operator_btn.state == "down":
                operator_btn.state = "normal"
                if self.last_ope and not self.full_exp:
                    self.full_exp = [self.ans]
                self.full_exp += (self.display.text, operator_btn.text)
                self.display.text = ''
        else:
            self.display.text += char

    def calc(self):
        if self.error or not self.full_exp:
            return
        if self.end and self.last_ope:
            expression = self.true_exp(self.display.text + ''.join(self.last_ope))
        else:
            expression = self.true_exp()
            try:
                self.last_ope = (self.full_exp[-1], self.display.text)
            except IndexError:
                self.last_ope = None
        print(self.full_exp, expression, self.last_ope)
        try:
            result = eval(expression)
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
            result = str(result)
            self.ans = result
            self.display.text = result
            self.full_exp = []
            self.end = True
        except Exception as e:
            self.error = True
            self.clear_btn.text = "AC"
            self.display.text = e.__class__.__name__

    def clear(self):
        self.display.text = '0'
        self.ans = ''
        if self.clear_btn.text == "AC":
            self.full_exp = []
            self.error = False
            operators = OperatorBtn.get_widgets("operators")
            for operator_btn in operators:
                if operator_btn.state == "down":
                    operator_btn.state = "normal"
        else:
            self.clear_btn.text = "AC"


class CalculatorApp(App):

    def build(self):
        return CalcLayout()


calcApp = CalculatorApp()
calcApp.run()
