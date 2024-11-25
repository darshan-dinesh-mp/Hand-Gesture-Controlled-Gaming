from tkinter import *
import cv2 
from PIL import Image, ImageTk 
from tkinter import messagebox, simpledialog
import face_recognition
import pickle
from SignUp import FaceRecognition
from SignIn import SignIn
from game import Game
from hand_module import HandRecognition


width, height = 800, 600

app = Tk() 

app.bind('<Escape>', lambda e: app.quit()) 

label_widget = Label(app) 
label_widget.pack() 

def get_hand():
    messagebox.showinfo("Hand Recognition","Show your hand into the camera. Press OK to continue")
    hand = HandRecognition()
    if hand.run():
        app.destroy()
        game = Game()
        game.start()


def signUp():
    id = simpledialog.askinteger("Input", "Enter User ID:")
    name = simpledialog.askstring("Input", "Enter User Name:")
    age = simpledialog.askinteger("Input", "Enter User Age:")
    problem = simpledialog.askstring("Input", "Enter User Problem:")
    score = simpledialog.askfloat("Input", "Enter User Score:")
    messagebox.showinfo("Photo","Press S once face is postioned")

    signup = FaceRecognition(id,name,age,problem,score)
    signup.detect_and_save_face_encoding()
    messagebox.showinfo("Success","User registered,Sign In to continue")


def signIn():
    signin = SignIn()
    uid = signin.sign_in()
    print(uid)
    try:
        with open(f"details/{uid}.txt", 'r') as file:
            content = file.read()

        messagebox.showinfo("File Content", content)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {id} not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    
    get_hand()
    

app.title('Face Recognition System')
app.geometry('400x300')

button1 = Button(app, text="Sign In", command=lambda: signIn()) 
button1.pack() 
button2 = Button(app, text="Sign Up", command=lambda: signUp()) 
button2.pack() 

app.mainloop() 