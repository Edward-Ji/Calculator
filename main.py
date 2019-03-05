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
    full_exp = []

    def true_exp(self):
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
        for operator_btn in operators:
            if operator_btn.state == "down":
                operator_btn.state = "normal"
                self.full_exp.append(self.display.text + operator_btn.text)
                self.display.text = ''
        else:
            self.display.text += char

    def calc(self):
        if self.error:
            return
        expression = self.true_exp()
        if not expression:
            return
        try:
            result = eval(expression)
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
            self.display.text = str(result)
            self.full_exp = []
        except Exception as e:
            self.error = True
            self.clear_btn.text = "AC"
            self.display.text = e.__class__.__name__

    def clear(self):
        self.display.text = '0'
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
