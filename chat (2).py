import pika
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox

def receiver():

    def chamada(ch, method, propreties, body):
        msg_list.insert(END, "Ele -- "+ body.decode())
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue1')

    if (channel.basic_consume(queue='task_queue1', on_message_callback= chamada, auto_ack=True)):
        msg_list.insert(END,"Aguarde... ")
        time.sleep(2)
        messagebox.showinfo(" Aviso", "O chat está Ativo!")
        msg_list.delete(0,END)

    channel.start_consuming()
    connection.close()

def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue2')

    live = entry_field.get()
    msg_list.insert(END, "Você -- " + live)
    
    channel.basic_publish(exchange='', routing_key='task_queue2', body= live)    
    connection.close()

#instancia da TK (janela)

janela = Tk()
janela.title("Chat 2")
janela.geometry("350x275+700+100")

#BOTAO SAIR DEVE CHAMAR A FUNÇAO CLOSE PARA DESCONECTAR 
def sair():
    msg_list.delete(0,END)
    janela.destroy()
    
botao_sair = Button(janela, text = "Sair", command= sair )
botao_sair.pack(side = TOP, anchor = NE, pady = 5, padx = 5)

#Apresenta o texto na tela  

messages_frame = Frame(janela)       
scrollbar = Scrollbar(messages_frame) 
msg_list = Listbox(messages_frame, height=10, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side= RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

#Recebe os valores do usuario com a caixa de texto

botao_frame = Frame(janela)
lb = Label(botao_frame,text = "Digite sua mensagem: ")
lb.pack(side = LEFT, anchor= S, padx = 5)
entry_field = Entry(botao_frame, textvariable = '')
#entry_field.bind("<Return>", send)
entry_field.pack(side = LEFT, anchor = SE,pady=  5)

#Botões, envia e sair

send_button = Button(botao_frame, text= "Send", command= send)
send_button.pack(side = LEFT, anchor = S, pady = 5, padx = 5)

botao_frame.pack()

receive_thread = Thread(target= receiver)
sender_thread = Thread(target= send)
receive_thread.start()
sender_thread.start()
janela.mainloop()