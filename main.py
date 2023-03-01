from tkinter import Tk, Label, Canvas, PhotoImage, Button
import math


class PomodoroTimer:
    def __init__(self, short_break_color: str = "#e2979c", long_break_color: str = "#e7305b", work_color: str = "#9bdeac",
                 label_color: str = '#9bdeac', background_color: str = "#f7f5dd", button_color: str = '#9bdeac',
                 button_text_color: str = 'black', FONT_NAME: str = "Courier",
                 work_time: int = 25, short_break: int = 5, long_break: int = 20):
        self.rounds = 0
        self.timer = None
        self.short_break_color = short_break_color
        self.long_break_color = long_break_color
        self.work_color = work_color
        self.label_color = label_color
        self.background_color = background_color
        self.button_color = button_color
        self.button_text_color = button_text_color
        self.work_time = work_time * 60
        self.short_break = short_break * 60
        self.long_break = long_break * 60

        self.master = Tk()
        self.master.title('Pomodoro Timer')
        self.master.config(padx=100, pady=50, background=self.background_color)

        self.timer_label = Label(
            text="Timer", fg=self.label_color, background=self.background_color, font=(FONT_NAME, 35))
        self.timer_label.grid(column=2, row=1)

        self.canvas = Canvas(width=200, height=224,
                             background=self.background_color, highlightthickness=0)
        self.image = PhotoImage(file='./tomato.png')
        self.canvas.create_image(100, 112, image=self.image)
        self.timer_text = self.canvas.create_text(
            100, 130, text='00:00', fill='white',  font=(FONT_NAME, 20, 'bold'))
        self.canvas.grid(column=2, row=2)

        self.start_button = Button(
            background=self.button_color, fg='black', text='Start', width=10, highlightthickness=0, command=self.start)
        self.start_button.grid(column=1, row=4)

        self.stop_button = Button(
            background=self.button_color, fg='black', text='Stop', width=10, highlightthickness=0, command=self.stop, state='disabled')
        self.stop_button.grid(column=2, row=4)

        self.reset_button = Button(
            background=self.button_color, fg='black', text='Reset', width=10, highlightthickness=0, command=self.reset, state='disabled')
        self.reset_button.grid(column=3, row=4)

        self.check_marks = Label(
            text='', background=self.background_color, fg=self.label_color, font=(FONT_NAME, 25))
        self.check_marks.grid(column=2, row=3)

    def __call__(self) -> None:
        self.master.mainloop()

    def start(self):
        self.start_button['state'] = "disabled"
        self.stop_button['state'] = "active"
        self.reset_button['state'] = "active"
        if self.timer:
            self.master.after_cancel(self.timer)
        self.timer_label.config(text='Timer', fg=self.label_color)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.rounds = 0
        self.check_marks.config(text='')

        self.start_timer()

    def stop(self):
        self.master.after_cancel(self.timer)
        self.start_button['state'] = "active"
        self.stop_button['state'] = "disabled"
        self.reset_button['state'] = "active"

    def start_timer(self):

        self.rounds += 1
        if self.rounds % 8 == 0:
            self.timer_label.config(text='Break', fg=self.long_break_color)
            self.counter_start(self.long_break)
        elif self.rounds % 2 == 0:
            self.timer_label.config(text='Break', fg=self.short_break_color)
            self.counter_start(self.short_break)
        else:
            self.timer_label.config(text='Work', fg=self.work_color)
            self.counter_start(self.work_time)

    def counter_start(self, counts: int):
        minutes = counts // 60
        seconds = counts % 60
        self.canvas.itemconfig(
            self.timer_text, text=f"{minutes:02d}:{seconds:02d}")
        if counts > 0:
            self.timer = self.master.after(1000, self.counter_start, counts-1)
        else:
            self.master.lift()
            self.start_timer()

            marks = ""
            work_sessions = math.floor(self.rounds/2)
            for _ in range(work_sessions):
                marks += "✔"
            self.check_marks.config(text=marks)

    def reset(self):
        self.master.after_cancel(self.timer)
        self.timer_label.config(text='Timer', fg=self.label_color)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.check_marks.config(text='')
        self.start_button['state'] = "active"
        self.stop_button['state'] = "disabled"
        self.reset_button['state'] = "disabled"


if __name__ == '__main__':
    app = PomodoroTimer()
    app()
