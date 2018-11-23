import tkinter as tk

from tkinter import *

import process
import file_io

LARGE_FONT = ("Verdana", 12)


class MainMenu(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.user = file_io.User()

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        # Add Pages here
        for F in (StartPage, PageOne, PageTwo, UserNamePage, GamePlay, LoosingPage, WinningPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="THE HARDEST WORD GAME EVER", font=LARGE_FONT, fg="red")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Play Game",
                           command=lambda: controller.show_frame(UserNamePage), bg="#4885ed", height=2, width=10)
        button.pack(pady=30, padx=30)

        # button2 = tk.Button(self, text="View Scores",
        #                     command=lambda: controller.show_frame(PageTwo), height=2, width=10)
        button2 = tk.Button(self, text="View Scores",
                            command=lambda: file_io.IO.readFromText(self))
        button2.pack(pady=30, padx=30)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(UserNamePage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage), height=2, width=10, bg="#00ffff")
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne), height=2, width=10)
        button2.pack()


class UserNamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="ENTER YOUR NAME", font=LARGE_FONT, fg="red")
        label.pack(pady=10, padx=10)

        e = Entry(self)
        e.pack()

        def e_delete():
            e.delete(first=0, last=22)

        def multiFunction():
            # user = file_io.User()
            controller.user.setName(e.get())
            e_delete()
            controller.user.test()
            controller.show_frame(GamePlay)

        # button = tk.Button(self, text="Continue", command=lambda: controller.show_frame(GamePlay), fg="red")
        button = tk.Button(self, text="Continue", command=multiFunction, fg="red", height=2, width=10)

        button.pack()


class GamePlay(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="GAME PLAY HERE", font=LARGE_FONT, fg="red")
        label.pack(pady=10, padx=10)
        # Instance

        logic = process.logic()
        logic.get_word()
        logic.process_word()
        logic.count_required_points()
        print(logic.blanked)

        # label = tk.Label(self, text=logic.blanked, fg="blue")
        # label.pack()
        v = StringVar()
        Label(self, textvariable=v, font=("Helvetica", 32)).pack(pady=30, padx=30)

        v.set(logic.blanked)

        e = Entry(self, width=20)

        e.pack(pady=30, padx=30)

        triesLeft = StringVar()
        triesLeft.set(logic.triesLeft)

        lettersTested = StringVar()
        lettersTested.set(logic.totalTested)

        def e_delete():
            e.delete(first=0, last=22)

        def rebuild():

            if logic.triesLeft <= 0:
                file_io.IO.saveToText(self, controller.user.name, controller.user.points)
                logic.reset()
                controller.show_frame(LoosingPage)
                rebuild()

            if logic.triesLeft >= 0:
                if e.get() != "":
                    logic.check_letter(e.get())
                e_delete()
                # label = tk.Label(self, text=logic.blanked, fg="blue")
                # label.pack()
                v.set(logic.blanked)
                triesLeft.set(logic.triesLeft)
                logic.tested_letters()
                lettersTested.set(logic.totalTested)

            if logic.points == logic.requiredPoints:
                controller.user.setPoints(logic.points)

                logic.reset()

                controller.show_frame(WinningPage)
                rebuild()

        submitButton = Button(self, text="Submit", command=rebuild, height=2, width=10)
        submitButton.pack(pady=10, padx=10)

        tested = Label(self, textvariable=lettersTested, font=("Helvetica", 20))
        tested.pack()

        triesLeftLable = Label(self, textvariable=triesLeft, font=("Helvetica", 20))
        triesLeftLable.pack()

        quitButton = Button(self, text="Quit", height=2, width=10)
        quitButton.pack(pady=10, padx=10)


class LoosingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="YOU LOOSE! HAHAHAHAHAHA", font=LARGE_FONT, fg="red")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Continue", command=lambda: controller.show_frame(StartPage), fg="red")
        button.pack()


class WinningPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="YOU WIN YAY!", font=LARGE_FONT, fg="red")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Continue", command=lambda: controller.show_frame(GamePlay), fg="red")
        button.pack()
