from tkinter import *
from tkinter import messagebox
import json
import pyttsx3
# import gtts
from difflib import get_close_matches

# instaniate by object of engine class by converting text to speech
engine = pyttsx3.init()

# rate of words spoken per minute
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)

root = Tk()


def wordaudio():
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[0].id)
    engine.say(enterwordentry.get())
    engine.runAndWait()


def meaningaudio():
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(textarea.get(1.0, END))
    engine.runAndWait()


def iexit():
    res = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if res == True:
        root.destroy()
    else:
        pass


def clear():
    textarea.config(state=NORMAL)
    enterwordentry.delete(0, END)
    textarea.delete(1.0, END)
    textarea.config(state=DISABLED)


def search():
    data = json.load(open('data.json'))
    word = enterwordentry.get()
    # returns a string where all characters are lower case
    word = word.lower()

    # if the user types a correct word
    if word in data:
        # accesing meanings
        meaning = data[word]

        # to change the disable to normal in meaning section
        textarea.config(state=NORMAL)

        # auto delete after every searched word
        textarea.delete(1.0, END)

        for item in meaning:
            # accesing bullet symbol
            textarea.insert(END, u'\u2022' + item + '\n\n')
        # to disable the meaning tab
        textarea.config(state=DISABLED)

    # if the user types wrong spelling but a similar word
    # trying to match the closest words to the ones we have searched for  by default n=3 and cutoff =0.6(0.1 to 0.9)
    elif len(get_close_matches(word, data.keys())) > 0:

        # aquires 1st closest word
        close_match = get_close_matches(word, data.keys())[0]

        res = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead?')

        if res == True:
            meaning = data[close_match]

            # auto delete after every searched word
            textarea.delete(1.0, END)

            # to change the disable to normal in meaning section
            textarea.config(state=NORMAL)

            for item in meaning:
                # accesing bullet symbol
                textarea.insert(END, u'\u2022' + item + '\n\n')
                # to disable the meaning tab
                textarea.config(state=DISABLED)

        else:
            # auto delete after every searched word
            textarea.delete(1.0, END)

            messagebox.showinfo('Information', ' Please type a correct word')
            enterwordentry.delete(0, END)

    # if the user type a complete non-sink word
    else:
        messagebox.showerror('Error', ' The word doent exist please double check it.')
        enterwordentry.delete(0, END)


root.geometry('1000x626+100+50')
root.title('Talking Dictionary created by Sai Chaitanya')
root.resizable(0, 0)

bgimage = PhotoImage(file='bg.png')
bgLabel = Label(root, image=bgimage)
bgLabel.place(x=0, y=0)

enterwordLabel = Label(root, text='ENTER WORD', font=('casteller', '29', 'bold'), foreground='pink3', bg='whitesmoke')
enterwordLabel.place(x=530, y=20)

enterwordentry = Entry(root, font=('arial', 23, 'bold'), relief=GROOVE, bd=6, justify=CENTER)
enterwordentry.place(x=510, y=80)

enterwordentry.focus_set()

searchimage = PhotoImage(file='search.png')
searchbutton = Button(root, image=searchimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                      command=search)
searchbutton.place(x=620, y=150)

micimage = PhotoImage(file='mic.png')
micbutton = Button(root, image=micimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                   command=wordaudio)
micbutton.place(x=710, y=153)

meainglabel = Label(root, text='Meaning', font=('casteller', '29', 'bold'), fg='pink3', bg='whitesmoke')
meainglabel.place(x=580, y=240)

textarea = Text(root, font=('arial', 18, 'bold'), height=8, width=34, bd=6, relief=GROOVE, wrap='word')
textarea.place(x=460, y=300)

audioimage = PhotoImage(file='microphone.png')
audiobutton = Button(root, image=audioimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                     command=meaningaudio)
audiobutton.place(x=530, y=555)

clearimage = PhotoImage(file='clear.png')
clearbutton = Button(root, image=clearimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                     command=clear)
clearbutton.place(x=660, y=555)

exitimage = PhotoImage(file='exit.png')
exitbutton = Button(root, image=exitimage, bd=0, bg='whitesmoke', activebackground='whitesmoke', cursor='hand2',
                    command=iexit)
exitbutton.place(x=790, y=555)

root.mainloop()
